#!/usr/bin/env python3
"""
test_qr_perception.py — qr_perception kamera modunu test et

KULLANIM (3 terminal):

  # Terminal 1 — qr_perception node'u başlat
  source ~/gz_ws/install/setup.bash
  ros2 run my_swarm_pkg qr_perception --ros-args \
      -p camera_drone_id:=3 \
      -p use_camera:=true

  # Terminal 2 — bu test scriptini çalıştır
  cd ~/gz_ws/src/my_swarm_pkg
  python3 scripts/test_qr_perception.py

  # Terminal 3 — sonucu izle
  ros2 topic echo /qr/result

TEST NEDİR:
  1. QR marker PNG'sini okur
  2. ROS sensor_msgs/Image mesajına çevirir
  3. /drone3/camera/image_raw topic'ine yayınlar
  4. qr_perception node'u kamerayı görür, pyzbar ile decode eder
  5. /qr/result topic'ine QRResult yayınlar
"""

import sys
import os
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from swarm_msgs.msg import QRResult

try:
    import cv2
    from cv_bridge import CvBridge
except ImportError:
    print("HATA: pip3 install opencv-python cv_bridge")
    sys.exit(1)


# Test edilecek QR numarası (1-6)
TEST_QR_ID = 1

MODELS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'models'
)


class QRTester(Node):

    def __init__(self):
        super().__init__('qr_tester')
        self._bridge  = CvBridge()
        self._results = []

        # Publisher: kamera görüntüsü
        self._img_pub = self.create_publisher(
            Image, '/drone3/camera/image_raw', 10)

        # Publisher: drone pozisyonu (qr_perception pose takibi için)
        self._pose_pub = self.create_publisher(
            PoseStamped, '/drone3/pose', 10)

        # Subscriber: QR sonucu
        self.create_subscription(
            QRResult, '/qr/result', self._on_result, 10)

        self.get_logger().info(
            f'QR Tester hazir — QR{TEST_QR_ID} test ediliyor...')

    def _on_result(self, msg: QRResult):
        self._results.append(msg)
        print(f'\n{"="*50}')
        print(f'QR{msg.qr_id} ALINDI!')
        print(f'  Formasyon  : {msg.formation_type} (aktif={msg.formation_active})')
        print(f'  Irtifa     : {msg.altitude}m (aktif={msg.altitude_active})')
        print(f'  Manevra    : pitch={msg.pitch_deg} roll={msg.roll_deg}')
        print(f'  Ayrilma    : {msg.zone_color if msg.detach_active else "-"}')
        print(f'  Sonraki QR : {msg.next_qr_id}')
        print(f'  Bekle      : {msg.wait_seconds}s')
        print(f'{"="*50}\n')

    def publish_test_image(self, qr_id: int):
        """QR PNG'yi ROS Image olarak yayınla."""
        png_path = os.path.join(
            MODELS_DIR,
            f'qr_marker_{qr_id}',
            'materials', 'textures',
            f'qr_marker_{qr_id}.png'
        )

        if not os.path.exists(png_path):
            self.get_logger().error(f'PNG bulunamadi: {png_path}')
            self.get_logger().error(
                'Once scripti calistirin: python3 scripts/generate_qr_codes.py')
            return False

        cv_img = cv2.imread(png_path)
        if cv_img is None:
            self.get_logger().error(f'PNG okunamadi: {png_path}')
            return False

        ros_img = self._bridge.cv2_to_imgmsg(cv_img, 'bgr8')
        ros_img.header.stamp = self.get_clock().now().to_msg()
        ros_img.header.frame_id = 'drone3/camera_link'
        self._img_pub.publish(ros_img)
        self.get_logger().info(f'QR{qr_id} goruntusU yayinlandi ({png_path})')
        return True

    def publish_drone_pose(self, x=0.0, y=0.0, z=15.0):
        """Drone pozisyonunu yayınla."""
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.pose.orientation.w = 1.0
        self._pose_pub.publish(msg)


def main():
    rclpy.init()
    node = QRTester()

    print(f'\nqr_perception node calisıyor mu kontrol ediliyor...')
    print(f'(qr_perception baslamamissa baska terminalde baslatın)\n')

    # Pose yayınla (gerekli)
    for _ in range(5):
        node.publish_drone_pose()
        rclpy.spin_once(node, timeout_sec=0.1)

    print(f'QR{TEST_QR_ID} test goruntusU yayinlaniyor...')

    # 5 kez yayınla (node hazır olmayabilir)
    for attempt in range(5):
        node.publish_test_image(TEST_QR_ID)
        node.publish_drone_pose()

        # Sonuç bekle
        deadline = time.time() + 1.0
        while time.time() < deadline:
            rclpy.spin_once(node, timeout_sec=0.05)
            if node._results:
                break

        if node._results:
            print(f'\nTEST BASARILI! QR{TEST_QR_ID} dogru sekilde okundu.')
            break

        print(f'  Deneme {attempt+1}/5 — bekleniyor...')
        time.sleep(0.5)
    else:
        print('\nTEST BASARISIZ!')
        print('Olasi nedenler:')
        print('  1. qr_perception node calismiyor')
        print('     → ros2 run my_swarm_pkg qr_perception --ros-args -p use_camera:=true')
        print('  2. swarm_msgs paketi kurulmamis')
        print('  3. ROS_LOCALHOST_ONLY ayari uyumsuz')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
