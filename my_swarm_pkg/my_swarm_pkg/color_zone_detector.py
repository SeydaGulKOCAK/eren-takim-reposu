#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       color_zone_detector.py                                 ║
║        Kamera ile HSV renk filtresi → /perception/color_zones               ║
╚══════════════════════════════════════════════════════════════════════════════╝

GENEL AÇIKLAMA:
---------------
Drone kamerasından gelen görüntüde kırmızı/mavi/yeşil iniş zonlarını tespit
eder. OpenCV HSV renk uzayı kullanır.

Tespit edilen zone'ların Gazebo'daki gerçek pozisyonunu hesaplamak için:
  1. Drone'un anlık pozisyonunu alır (/{ns}/pose)
  2. Kamera görüntüsünde renk blob merkezini tespit eder
  3. Blob merkezi + irtifa + kamera FOV → NED offseti hesaplar
  4. Offset + drone pozisyonu = zone dünya koordinatı
  5. /perception/color_zones yayınlar (ColorZoneList)

qr_perception.py'deki YAML tabanlı sabit koordinatların yerini alır.

PARAMETRELER:
-------------
  camera_drone_id    : Birincil kamera drone ID (varsayılan: 3)
  backup_drone_id    : Yedek kamera drone ID (varsayılan: 2)
  publish_hz         : Yayın frekansı (varsayılan: 5.0)
  min_area_px        : Minimum blob alanı piksel cinsinden (varsayılan: 500)
  camera_fov_h_deg   : Yatay FOV açısı derece (varsayılan: 60.0)
  img_width          : Görüntü genişliği piksel (varsayılan: 640)
  img_height         : Görüntü yüksekliği piksel (varsayılan: 480)
  zone_radius        : Zone yarıçapı metre (varsayılan: 2.0)

YAYINLANAN:
-----------
  /perception/color_zones  → ColorZoneList (koordinatlar + renkler)

İZLENEN:
---------
  /drone{N}/camera/image_raw  → sensor_msgs/Image
  /drone{N}/pose              → geometry_msgs/PoseStamped (irtifa için)
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

try:
    import cv2
    import numpy as np
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

try:
    from cv_bridge import CvBridge
    _CVBRIDGE_AVAILABLE = True
except ImportError:
    _CVBRIDGE_AVAILABLE = False

from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from swarm_msgs.msg import ColorZone, ColorZoneList

# ── HSV RENK ARALIĞI TANIMLARI ────────────────────────────────────────────────
# OpenCV HSV: H=[0,179], S=[0,255], V=[0,255]

# Kırmızı: iki aralık (0° ve 180° civarı)
RED_LOWER1 = (0,   120, 70)
RED_UPPER1 = (10,  255, 255)
RED_LOWER2 = (160, 120, 70)
RED_UPPER2 = (179, 255, 255)

# Mavi
BLUE_LOWER = (100, 120, 70)
BLUE_UPPER = (130, 255, 255)

# Yeşil
GREEN_LOWER = (40, 80, 70)
GREEN_UPPER = (80, 255, 255)

# Renk listesi: (renk_adı, alt1, üst1, alt2=None, üst2=None)
COLOR_DEFS = [
    ('RED',   RED_LOWER1,  RED_UPPER1,  RED_LOWER2, RED_UPPER2),
    ('BLUE',  BLUE_LOWER,  BLUE_UPPER,  None,       None),
    ('GREEN', GREEN_LOWER, GREEN_UPPER, None,       None),
]


class ColorZoneDetector(Node):
    """
    Kamera görüntüsünden renk zonu tespiti.
    Her drone'da çalışabilir; sadece aktif kamera drone'u için image subscribe eder.
    """

    def __init__(self):
        super().__init__('color_zone_detector')

        # ── Parametreler ──────────────────────────────────────────────────
        self.declare_parameter('camera_drone_id',  3)
        self.declare_parameter('backup_drone_id',  2)
        self.declare_parameter('publish_hz',       5.0)
        self.declare_parameter('min_area_px',      500)
        self.declare_parameter('camera_fov_h_deg', 60.0)
        self.declare_parameter('img_width',        640)
        self.declare_parameter('img_height',       480)
        self.declare_parameter('zone_radius',      2.0)

        self._cam_id   = self.get_parameter('camera_drone_id').value
        self._bak_id   = self.get_parameter('backup_drone_id').value
        self._pub_hz   = self.get_parameter('publish_hz').value
        self._min_area = self.get_parameter('min_area_px').value
        fov_deg        = self.get_parameter('camera_fov_h_deg').value
        self._img_w    = self.get_parameter('img_width').value
        self._img_h    = self.get_parameter('img_height').value
        self._zone_r   = self.get_parameter('zone_radius').value

        self._fov_h_rad = math.radians(fov_deg)
        self._fov_v_rad = self._fov_h_rad * (self._img_h / self._img_w)

        # ── Durum ─────────────────────────────────────────────────────────
        self._detected_zones: dict[str, tuple[float, float, float]] = {}
        self._drone_alts: dict[int, float] = {}
        self._drone_poses: dict[int, tuple[float, float, float]] = {}
        self._latest_image = None
        self._active_cam_id = self._cam_id

        # ── Yardımcı ──────────────────────────────────────────────────────
        if _CVBRIDGE_AVAILABLE:
            self._bridge = CvBridge()
        else:
            self._bridge = None
            self.get_logger().warn(
                'cv_bridge bulunamadı! Görüntü dönüşümü devre dışı.'
            )

        if not _CV2_AVAILABLE:
            self.get_logger().warn(
                'OpenCV (cv2) bulunamadı! '
                'pip3 install opencv-python ile yükleyin.'
            )

        # ── QoS ──────────────────────────────────────────────────────────
        be_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )
        rel_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
        )

        # ── Publisher ─────────────────────────────────────────────────────
        self._zone_pub = self.create_publisher(
            ColorZoneList, '/perception/color_zones', rel_qos
        )

        # ── Abonelikler ───────────────────────────────────────────────────
        # Birincil ve yedek kamera görüntüsü
        for did in (self._cam_id, self._bak_id):
            self.create_subscription(
                Image,
                f'/drone{did}/camera/image_raw',
                lambda msg, d=did: self._on_image(msg, d),
                be_qos,
            )
            self.create_subscription(
                PoseStamped,
                f'/drone{did}/pose',
                lambda msg, d=did: self._on_pose(msg, d),
                be_qos,
            )

        # ── Timer ─────────────────────────────────────────────────────────
        self.create_timer(1.0 / self._pub_hz, self._detect_and_publish)

        self.get_logger().info(
            f'ColorZoneDetector başladı\n'
            f'  Birincil kamera : drone{self._cam_id}\n'
            f'  Yedek kamera    : drone{self._bak_id}\n'
            f'  Yayın Hz        : {self._pub_hz}\n'
            f'  Min alan        : {self._min_area} px\n'
            f'  FOV (H/V)       : {math.degrees(self._fov_h_rad):.1f}°/'
            f'{math.degrees(self._fov_v_rad):.1f}°\n'
            f'  cv2             : {"OK" if _CV2_AVAILABLE else "YOK"}\n'
            f'  cv_bridge       : {"OK" if _CVBRIDGE_AVAILABLE else "YOK"}'
        )

    # ── Callback'ler ──────────────────────────────────────────────────────────

    def _on_image(self, msg: Image, drone_id: int) -> None:
        """Kamera görüntüsü geldi."""
        if drone_id == self._active_cam_id:
            self._latest_image = msg

    def _on_pose(self, msg: PoseStamped, drone_id: int) -> None:
        """Drone pozisyonu güncelle."""
        p = msg.pose.position
        self._drone_poses[drone_id] = (p.x, p.y, p.z)
        self._drone_alts[drone_id] = p.z

    # ── Ana tespit döngüsü ────────────────────────────────────────────────────

    def _detect_and_publish(self) -> None:
        """Görüntüden renk zonu tespit et → yayınla."""
        # OpenCV yoksa boş yayın
        if not _CV2_AVAILABLE or not _CVBRIDGE_AVAILABLE:
            self._publish_detected()
            return

        img_msg = self._latest_image
        if img_msg is None:
            return

        # Görüntüyü OpenCV'ye çevir
        try:
            cv_img = self._bridge.imgmsg_to_cv2(img_msg, 'bgr8')
        except Exception as e:
            self.get_logger().warn(f'Görüntü dönüşüm hatası: {e}',
                                   throttle_duration_sec=5.0)
            return

        # Kamera droneun pozisyonu
        drone_pos = self._drone_poses.get(self._active_cam_id)
        if drone_pos is None:
            return
        dx, dy, dz = drone_pos

        # HSV dönüşümü
        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        for color_name, lower1, upper1, lower2, upper2 in COLOR_DEFS:
            # Maske oluştur
            mask = cv2.inRange(hsv,
                               np.array(lower1), np.array(upper1))
            if lower2 is not None:
                mask2 = cv2.inRange(hsv,
                                    np.array(lower2), np.array(upper2))
                mask = cv2.bitwise_or(mask, mask2)

            # Morfoloji: gürültü gider
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)

            # Kontur bul
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if not contours:
                continue

            # En büyük konturu al
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            if area < self._min_area:
                continue

            # Blob merkezi (piksel koordinatı)
            M = cv2.moments(largest)
            if M['m00'] == 0:
                continue
            cx_px = M['m10'] / M['m00']
            cy_px = M['m01'] / M['m00']

            # Piksel → normalize koordinat ([-0.5, 0.5])
            nx = (cx_px / w) - 0.5
            ny = (cy_px / h) - 0.5

            # Kamera projeksiyon: offset = normalize * 2 * alt * tan(fov/2)
            # Downward camera: +x görüntü = drone'a göre +y dünya (yaw=0 için)
            # +y görüntü = drone'a göre -x dünya (downward cam, yaw=0 için)
            offset_y = nx * 2.0 * dz * math.tan(self._fov_h_rad / 2.0)
            offset_x = -ny * 2.0 * dz * math.tan(self._fov_v_rad / 2.0)

            world_x = dx + offset_x
            world_y = dy + offset_y
            world_z = 0.0

            self._detected_zones[color_name] = (world_x, world_y, world_z)

            self.get_logger().debug(
                f'{color_name} zone tespit: area={area:.0f}px '
                f'→ ({world_x:.2f}, {world_y:.2f})',
                throttle_duration_sec=2.0,
            )

        self._publish_detected()

    def _publish_detected(self) -> None:
        """Tespit edilen zone'ları yayınla."""
        if not self._detected_zones:
            return

        msg = ColorZoneList()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        for color, (wx, wy, wz) in self._detected_zones.items():
            zone           = ColorZone()
            zone.color     = color
            zone.position.x = wx
            zone.position.y = wy
            zone.position.z = wz
            zone.radius    = self._zone_r
            msg.zones.append(zone)

        self._zone_pub.publish(msg)


# ── Entrypoint ────────────────────────────────────────────────────────────────

def main(args=None):
    rclpy.init(args=args)
    node = ColorZoneDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
