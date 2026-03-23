#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         qr_perception.py                                    ║
║         Mock QR Algılama Nodu — Şartname Şekil 2 JSON Formatı               ║
╚══════════════════════════════════════════════════════════════════════════════╝

GENEL AÇIKLAMA:
---------------
Gerçek kamera olmadan QR algılamayı simüle eder.
Kamera drone'u bir QR'a trigger_radius kadar yaklaşınca YAML'daki
'content' alanı okunur (Şekil 2 JSON formatı ile birebir) ve QRResult yayınlanır.

Şekil 2 JSON yapısı:
  {
    "qr_id": 1,
    "gorev": {
      "formasyon":          {"aktif": true,  "tip": "OKBASI"},
      "manevra_pitch_roll": {"aktif": false, "pitch_deg": "0", "roll_deg": "0"},
      "irtifa_degisim":     {"aktif": true,  "deger": 20},
      "bekleme_suresi_s":   3
    },
    "suruden_ayrilma": {
      "aktif": false,
      "ayrilacak_drone_id": null,
      "hedef_renk": null,
      "bekleme_suresi_s": null
    },
    "sonraki_qr": {"team_1": 4, "team_2": 4, "team_3": 4}
  }

TEAM ID HARİTALAMA:
-------------------
  ROS parametre 'team_id' (örn: 'team1') → YAML anahtar 'team_1'
  Dönüşüm: team_id.replace('team', 'team_')
  Örn: 'team1' → 'team_1', 'team2' → 'team_2', 'team3' → 'team_3'

VERİ AKIŞI:
-----------
  /drone{i}/pose       →  10Hz yakınlık kontrolü
  /drone{i}/local_state →  failover izleme
                                ↓
                       qr_perception (BU NODE)
                          ↓              ↓
                   /qr/result      /perception/color_zones
                          ↓
                  intent_coordinator

BAŞLATMA:
---------
  ros2 run my_swarm_pkg qr_perception --ros-args -p team_id:=team1

TEST:
-----
  ros2 topic pub /drone1/pose geometry_msgs/msg/PoseStamped \
      "{pose: {position: {x: 10.0, y: 20.0, z: 15.0}}}" --once
  ros2 topic echo /qr/result
"""

import os
import math
import yaml

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image as RosImage
from swarm_msgs.msg import LocalState, QRResult, ColorZone, ColorZoneList, SwarmIntent
from std_msgs.msg import Bool
from swarm_msgs.srv import SetQRMap

try:
    from ament_index_python.packages import get_package_share_directory
    _AMENT_AVAILABLE = True
except ImportError:
    _AMENT_AVAILABLE = False

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

try:
    from cv_bridge import CvBridge
    _CVBRIDGE_AVAILABLE = True
except ImportError:
    _CVBRIDGE_AVAILABLE = False

try:
    import pyzbar.pyzbar as pyzbar
    _PYZBAR_AVAILABLE = True
except ImportError:
    _PYZBAR_AVAILABLE = False

try:
    import numpy as _np
    _NP_AVAILABLE = True
except ImportError:
    _NP_AVAILABLE = False

try:
    from gz.transport13 import Node as GzNode
    from gz.msgs10.image_pb2 import Image as GzImage
    _GZ_TRANSPORT_AVAILABLE = True
except ImportError:
    _GZ_TRANSPORT_AVAILABLE = False

import time as _time
import threading as _threading

# Hibrit tarama faz süreleri [s]
_LEADER_TIMEOUT_S    = 1.5   # Leader okuyamazsa → nearest drone
_NEAREST_TIMEOUT_S   = 1.5   # Nearest okuyamazsa → all scan
_PROXIMITY_FALLBACK_S = 3.0  # ALL_SCAN fazında bu kadar sonra proximity fallback devreye girer

# ── ADAPTİF ZOOM PARAMETRELERİ ────────────────────────────────────────────
# Referans: 640px kamerada 1.2m QR → yükseklik arttıkça piksel boyutu düşer
# zoom = altitude / _ZOOM_REF_ALT  (clamp: [_ZOOM_MIN, _ZOOM_MAX])
_ZOOM_REF_ALT = 5.0   # Bu yükseklikte zoom=1x (QR zaten büyük)
_ZOOM_MIN     = 2.0    # Minimum zoom (düşük irtifada bile 2x)
_ZOOM_MAX     = 8.0    # Maximum zoom (çok yüksekte pikselasyon sınırı)

# Kamera failover'ı tetikleyen yerel durumlar
_FAILOVER_STATES = frozenset({'DETACH', 'SAFETY_HOLD', 'PILOT_OVERRIDE'})
_RECOVERY_STATE  = 'REJOIN'


class QRPerception(Node):
    """Mock QR algılama nodu — Şekil 2 JSON formatı."""

    def __init__(self):
        super().__init__('qr_perception')

        # ── PARAMETRELER ─────────────────────────────────────────────────
        self.declare_parameter('team_id',                'team1')
        self.declare_parameter('camera_drone_id',        1)
        self.declare_parameter('backup_camera_drone_id', 2)
        self.declare_parameter('num_drones',             3)
        self.declare_parameter('trigger_radius',         5.0)
        self.declare_parameter('qr_map_file',            '')
        self.declare_parameter('use_camera',             True)

        self._team_id        = self.get_parameter('team_id').value
        self._primary_cam_id = self.get_parameter('camera_drone_id').value
        self._backup_cam_id  = self.get_parameter('backup_camera_drone_id').value
        self._num_drones     = self.get_parameter('num_drones').value
        self._trigger_radius = self.get_parameter('trigger_radius').value
        qr_map_file          = self.get_parameter('qr_map_file').value
        self._use_camera     = self.get_parameter('use_camera').value

        # 'team1' → 'team_1' (YAML anahtar uyumu)
        self._team_key = self._team_id.replace('team', 'team_')

        # Aktif kamera drone (failover için)
        self._camera_drone_id: int  = self._primary_cam_id
        self._failover_active: bool = False

        # ── HİBRİT TARAMA DURUMU ─────────────────────────────────────────
        # Faz sırası: IDLE → LEADER → NEAREST → ALL_SCAN
        self._leader_id:        int       = self._primary_cam_id  # SwarmIntent'ten güncellenir
        self._scan_phase:       str       = 'ALL_SCAN'
        self._scan_phase_start: float     = 0.0
        self._active_cams:      set[int]  = set(range(1, self._num_drones + 1))
        self._trigger_active:   bool      = False   # trigger gelene kadar decode yapma
        self._target_qr_seq:    int       = 0       # SwarmIntent'ten hedef QR seq

        # ── QR HARİTASI ──────────────────────────────────────────────────
        if not qr_map_file:
            if _AMENT_AVAILABLE:
                pkg = get_package_share_directory('my_swarm_pkg')
                qr_map_file = os.path.join(pkg, 'config', 'qr_map.yaml')
            else:
                qr_map_file = os.path.join(
                    os.path.dirname(__file__), '..', '..', 'config', 'qr_map.yaml')

        self._qr_nodes:   dict = {}
        self._color_zones: list = []
        self._load_qr_map(qr_map_file)

        # ── DURUM ────────────────────────────────────────────────────────
        self._drone_poses:  dict[int, PoseStamped | None] = {
            i: None for i in range(1, self._num_drones + 1)
        }
        self._drone_states: dict[int, str] = {
            i: 'STANDBY' for i in range(1, self._num_drones + 1)
        }
        self._read_qr_ids: set[int] = set()   # aynı QR iki kez okunmaz

        # ── cv_bridge ────────────────────────────────────────────────────
        self._bridge = CvBridge() if _CVBRIDGE_AVAILABLE else None

        # ── QoS ─────────────────────────────────────────────────────────
        be_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # ── PUBLISHER'LAR ────────────────────────────────────────────────
        self._qr_pub   = self.create_publisher(QRResult,      '/qr/result',               10)
        self._map_ready_pub = self.create_publisher(Bool, '/swarm/qr_map_ready', 10)
        self._zone_pub = self.create_publisher(ColorZoneList, '/perception/color_zones',  10)

        # ── ABONELİKLER ─────────────────────────────────────────────────
        for i in range(1, self._num_drones + 1):
            self.create_subscription(
                PoseStamped, f'/drone{i}/pose',
                lambda msg, did=i: self._on_pose(msg, did), be_qos)
            self.create_subscription(
                LocalState, f'/drone{i}/local_state',
                lambda msg, did=i: self._on_local_state(msg, did), be_qos)

        # ── KAMERA ABONELİKLERİ ─────────────────────────────────────────
        # Öncelik: GZ transport (doğrudan, thread'de) > ROS2 image_raw (cv_bridge)
        self._gz_camera_active = False
        _cam_ok = _CV2_AVAILABLE and _PYZBAR_AVAILABLE and _NP_AVAILABLE

        if self._use_camera and _cam_ok and _GZ_TRANSPORT_AVAILABLE:
            # GZ transport — ayrı thread'de frame buffer'a alır,
            # ROS2 timer ile process eder (spin ile çakışmaz)
            self._gz_lock = _threading.Lock()
            self._gz_frame_buffer: dict[int, tuple] = {}  # drone_id → (gray, time)

            def _gz_thread_fn():
                gz_node = GzNode()
                for cam_id in range(1, self._num_drones + 1):
                    gz_node.subscribe(
                        GzImage,
                        f'/drone{cam_id}/camera/image',
                        lambda msg, did=cam_id: self._gz_buffer_frame(msg, did),
                    )
                self.get_logger().info(
                    f'   GZ kamera thread başladı — {self._num_drones} kamera')
                import signal
                signal.sigwait({signal.SIGTERM})  # Thread sonsuza kadar yaşar

            self._gz_thread = _threading.Thread(
                target=_gz_thread_fn, daemon=True)
            self._gz_thread.start()
            self._gz_camera_active = True

            # 5 Hz timer — buffer'daki en yeni frame'i process et
            self.create_timer(0.2, self._gz_poll_frames)
            self.get_logger().info(
                f'   Kamera QR modu: AKTIF (GZ transport thread + pyzbar)')

        elif self._use_camera and _cam_ok and _CVBRIDGE_AVAILABLE:
            # Fallback: ROS2 image_raw (ros_gz_bridge gerektirir)
            cam_qos = QoSProfile(
                reliability=QoSReliabilityPolicy.RELIABLE,
                history=QoSHistoryPolicy.KEEP_LAST,
                depth=1,
            )
            for cam_id in range(1, self._num_drones + 1):
                self.create_subscription(
                    RosImage,
                    f'/drone{cam_id}/camera/image_raw',
                    lambda msg, did=cam_id: self._on_camera_image(msg, did),
                    cam_qos,
                )
            self.get_logger().info(
                f'   Kamera QR modu: AKTIF (ROS2 image_raw + cv_bridge)')
        else:
            missing = []
            if not _CV2_AVAILABLE:           missing.append('opencv-python')
            if not _PYZBAR_AVAILABLE:        missing.append('pyzbar')
            if not _NP_AVAILABLE:            missing.append('numpy')
            if not _GZ_TRANSPORT_AVAILABLE:  missing.append('gz.transport13')
            if not _CVBRIDGE_AVAILABLE:      missing.append('cv_bridge')
            if missing:
                self.get_logger().warn(
                    f'   Kamera QR modu: KAPALI — eksik: {", ".join(missing)}'
                )

        # ── HİBRİT TARAMA ABONELİKLERİ ──────────────────────────────────
        # QR trigger (waypoint_navigator'dan) — RELIABLE QoS eşleşmesi
        trigger_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.create_subscription(Bool, '/qr/trigger', self._on_qr_trigger, trigger_qos)
        # Lider ID (SwarmIntent'ten)
        self.create_subscription(SwarmIntent, '/swarm/intent', self._on_swarm_intent, 10)

        # ── RUNTIME QR MAP GÜNCELLEME (JÜRİ KOORDİNATI) ──────────────
        self.create_service(SetQRMap, '/swarm/set_qr_map',
                          self._on_set_qr_map)

        # ── TIMER'LAR ────────────────────────────────────────────────────
        # Proximity fallback KAPALI — sadece kamera (pyzbar) ile QR okunur
        # self.create_timer(0.1,  self._check_qr_proximity)   # DEVRE DIŞI
        self.create_timer(0.5,  self._advance_scan_phase)   # 2 Hz — faz ilerletme
        self.create_timer(1.0,  self._publish_color_zones)  # 1 Hz
        # Startup'ta YAML haritası yüklendiyse 2s sonra ready sinyali gönder
        if self._qr_nodes:
            self._startup_ready_timer = self.create_timer(2.0, self._publish_startup_ready)

        self.get_logger().info(
            f'\nqr_perception hazir!\n'
            f'   Takim ID     : {self._team_id}  (YAML key: {self._team_key})\n'
            f'   Kamera drone : drone{self._camera_drone_id}\n'
            f'   Gorsel QR    : {"AKTIF (pyzbar)" if (self._use_camera and _PYZBAR_AVAILABLE and _CVBRIDGE_AVAILABLE) else "KAPALI (proximity yedek)"}\n'
            f'   Yedek        : drone{self._backup_cam_id}\n'
            f'   QR düğüm     : {len(self._qr_nodes)}\n'
            f'   Renk zone    : {len(self._color_zones)}\n'
            f'   Trig. radius : {self._trigger_radius:.1f} m\n'
            f'   Rota         : '
            + ' → '.join(str(k) for k in sorted(self._qr_nodes.keys()))
        )

    # ── YAML YÜKLEME ─────────────────────────────────────────────────────

    def _load_qr_map(self, filepath: str):
        """YAML'dan QR haritasını yükle (Şekil 2 formatı)."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            self._qr_nodes    = data.get('qr_nodes',    {})
            self._color_zones = data.get('color_zones', [])

            if 'trigger_radius' in data:
                self._trigger_radius = float(data['trigger_radius'])

            # Doğrulama
            for qr_id, node in self._qr_nodes.items():
                if 'position' not in node:
                    self.get_logger().warn(f'⚠️  QR{qr_id}: position eksik!')
                if 'content' not in node:
                    self.get_logger().warn(f'⚠️  QR{qr_id}: content eksik!')
                else:
                    c = node['content']
                    if 'sonraki_qr' not in c:
                        self.get_logger().warn(f'⚠️  QR{qr_id}: content.sonraki_qr eksik!')
                    elif self._team_key not in c['sonraki_qr']:
                        self.get_logger().warn(
                            f'⚠️  QR{qr_id}: sonraki_qr["{self._team_key}"] eksik!')

            self.get_logger().info(f'📂 QR haritası yüklendi: {filepath}')

        except FileNotFoundError:
            self.get_logger().error(f'❌ Dosya bulunamadı: {filepath}')
        except yaml.YAMLError as e:
            self.get_logger().error(f'❌ YAML parse hatası: {e}')
        except Exception as e:
            self.get_logger().error(f'❌ Yükleme hatası: {e}')

    # ── CALLBACK'LER ─────────────────────────────────────────────────────

    def _publish_startup_ready(self):
        """Startup YAML yüklemesinden sonra bir kez qr_map_ready yayınla."""
        msg = Bool()
        msg.data = True
        self._map_ready_pub.publish(msg)
        self.get_logger().info('✅ QR haritası HAZIR sinyali gönderildi (YAML startup).')
        self._startup_ready_timer.cancel()

    # ── RUNTIME QR MAP GÜNCELLEME ────────────────────────────────────────

    def _on_set_qr_map(self, request, response):
        """
        Jüri tarafından runtime'da QR koordinatlarını yükle (yarışma günü).
        
        request.qr_positions: geometry_msgs/Point[] array
        request.qr_ids:       uint32[] array
        request.next_qr_ids:  uint32[] array (same length as qr_ids)
        
        Builds runtime QR map structure matching YAML format.
        """
        try:
            if len(request.qr_positions) != len(request.qr_ids):
                response.success = False
                response.message = (
                    f"Position/ID count mismatch: {len(request.qr_positions)} vs {len(request.qr_ids)}"
                )
                self.get_logger().warn(f'⚠️ SetQRMap: {response.message}')
                return response
            
            if len(request.qr_ids) != len(request.next_qr_ids):
                response.success = False
                response.message = (
                    f"ID/next_qr_id count mismatch: {len(request.qr_ids)} vs {len(request.next_qr_ids)}"
                )
                self.get_logger().warn(f'⚠️ SetQRMap: {response.message}')
                return response
            
            # ── Yeni QR haritası oluştur ─────────────────────────────────
            new_qr_nodes = {}
            for idx, qr_id in enumerate(request.qr_ids):
                qr_id_int = int(qr_id)
                pos = request.qr_positions[idx]
                next_id = int(request.next_qr_ids[idx])
                
                # Team key'leri oluştur (all teams same next QR)
                sonraki_qr = {
                    'team_1': next_id,
                    'team_2': next_id,
                    'team_3': next_id,
                }
                
                # Şekil 2 uyumlu content yapısı (default)
                content = {
                    'qr_id': qr_id_int,
                    'gorev': {
                        'formasyon':          {'aktif': True,  'tip': 'OKBASI'},
                        'manevra_pitch_roll': {'aktif': False, 'pitch_deg': '0', 'roll_deg': '0'},
                        'irtifa_degisim':     {'aktif': True,  'deger': 20},
                        'bekleme_suresi_s':   3
                    },
                    'suruden_ayrilma': {
                        'aktif': False,
                        'ayrilacak_drone_id': None,
                        'hedef_renk': None,
                        'bekleme_suresi_s': None
                    },
                    'sonraki_qr': sonraki_qr
                }
                
                new_qr_nodes[qr_id_int] = {
                    'id': qr_id_int,
                    'position': {
                        'x': float(pos.x),
                        'y': float(pos.y),
                        'z': float(pos.z)
                    },
                    'content': content
                }
            
            # ── Eski haritayı değiştir ───────────────────────────────────
            self._qr_nodes = new_qr_nodes
            self._read_qr_ids.clear()  # Reset okunan QR'ları
            
            response.success = True
            response.message = (
                f"✅ {len(new_qr_nodes)} QR waypoint'i runtime yüklendi. Rota: " +
                ' → '.join(str(k) for k in sorted(new_qr_nodes.keys()))
            )
            
            # ── QR HARİTASI HAZIR TOPIC'İ YAYINLA ───────────────────────
            ready_msg = Bool()
            ready_msg.data = True
            self._map_ready_pub.publish(ready_msg)
            
            self.get_logger().info(
                f'\n╔══ 🎯 JÜRİ QR HARİTASI GÜNCELLENDI ══\n'
                f'║  Waypoint sayısı : {len(new_qr_nodes)}\n'
                f'║  Rota            : ' + ' → '.join(str(k) for k in sorted(new_qr_nodes.keys())) + f'\n'
                f'║  Team ID         : {self._team_id}\n'
                f'╚{"═"*40}'
            )
            
            return response
            
        except Exception as e:
            response.success = False
            response.message = f"SetQRMap error: {str(e)}"
            self.get_logger().error(f'❌ {response.message}')
            return response


    # ── HİBRİT TARAMA CALLBACK'LERİ ──────────────────────────────────────

    def _on_swarm_intent(self, msg: SwarmIntent) -> None:
        """Lider drone ID'sini ve hedef QR seq'i takip et."""
        self._leader_id = int(msg.leader_id)
        self._target_qr_seq = int(msg.qr_seq)

    def _on_qr_trigger(self, msg: Bool) -> None:
        """
        waypoint_navigator QR bölgesine girince True gönderir.
        True → decode aktif, False → decode pasif.
        """
        self._trigger_active = msg.data
        if msg.data:
            self.get_logger().info(
                f'📸 QR trigger AKTİF — hedef QR#{self._target_qr_seq} '
                f'(active_cams={self._active_cams})'
            )
        else:
            self.get_logger().info('📸 QR trigger KAPANDI — decode pasif')

    def _get_nearest_drone_to_target_qr(self) -> int:
        """
        Mevcut hedefe (centroide en yakın okunmamış QR) en yakın flying drone'u döndür.
        Bulunamazsa leader_id döndür.
        """
        # Centroid hesapla
        flying = [
            p for i, p in self._drone_poses.items()
            if p is not None and self._drone_states.get(i, '') in (
                'FLYING', 'DETACH', 'REJOIN', 'LAND_ZONE'
            )
        ]
        if not flying:
            return self._leader_id

        cx = sum(p.pose.position.x for p in flying) / len(flying)
        cy = sum(p.pose.position.y for p in flying) / len(flying)

        # Centroide en yakın okunmamış QR
        target_pos = None
        min_d_qr = float('inf')
        for qr_id, qr_data in self._qr_nodes.items():
            if qr_id in self._read_qr_ids:
                continue
            pos = qr_data.get('position', {})
            dx = cx - float(pos.get('x', 0.0))
            dy = cy - float(pos.get('y', 0.0))
            d  = math.sqrt(dx * dx + dy * dy)
            if d < min_d_qr:
                min_d_qr   = d
                target_pos = (float(pos.get('x', 0.0)), float(pos.get('y', 0.0)))

        if target_pos is None:
            return self._leader_id

        # Bu QR'a en yakın drone (leader hariç)
        best_id = self._leader_id
        best_d  = float('inf')
        for did, pose in self._drone_poses.items():
            if pose is None or did == self._leader_id:
                continue
            if self._drone_states.get(did, '') not in ('FLYING', 'DETACH', 'REJOIN'):
                continue
            dx = pose.pose.position.x - target_pos[0]
            dy = pose.pose.position.y - target_pos[1]
            d  = math.sqrt(dx * dx + dy * dy)
            if d < best_d:
                best_d  = d
                best_id = did
        return best_id

    def _advance_scan_phase(self) -> None:
        """
        2 Hz timer — hibrit tarama faz ilerletme.
        LEADER → NEAREST → ALL_SCAN
        """
        if self._scan_phase == 'IDLE':
            return

        elapsed = _time.time() - self._scan_phase_start

        if self._scan_phase == 'LEADER' and elapsed >= _LEADER_TIMEOUT_S:
            nearest = self._get_nearest_drone_to_target_qr()
            self._scan_phase       = 'NEAREST'
            self._scan_phase_start = _time.time()
            self._active_cams      = {nearest}
            self.get_logger().warn(
                f'⚠️  LEADER ({_LEADER_TIMEOUT_S}s) okuyamadı → '
                f'NEAREST: drone{nearest} kamerası aktif'
            )

        elif self._scan_phase == 'NEAREST' and elapsed >= _NEAREST_TIMEOUT_S:
            all_ids = set(range(1, self._num_drones + 1))
            self._scan_phase       = 'ALL_SCAN'
            self._scan_phase_start = _time.time()
            self._active_cams      = all_ids
            self.get_logger().warn(
                f'⚠️  NEAREST ({_NEAREST_TIMEOUT_S}s) okuyamadı → '
                f'ALL_SCAN: tüm kameralar aktif {sorted(all_ids)}'
            )

    _cam_log_count: int = 0

    def _gz_buffer_frame(self, gz_msg, drone_id: int) -> None:
        """GZ transport callback (ayrı thread) — frame'i buffer'a yaz."""
        try:
            w, h = gz_msg.width, gz_msg.height
            data = gz_msg.data
            channels = len(data) // (w * h) if w * h > 0 else 3

            if channels == 3:
                img = _np.frombuffer(data, dtype=_np.uint8).reshape(h, w, 3)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            elif channels == 4:
                img = _np.frombuffer(data, dtype=_np.uint8).reshape(h, w, 4)
                gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
            else:
                gray = _np.frombuffer(data, dtype=_np.uint8).reshape(h, w)

            with self._gz_lock:
                self._gz_frame_buffer[drone_id] = (gray, _time.time())
        except Exception:
            pass  # Thread'de hata yutulur, poll timer loglar

    def _gz_poll_frames(self) -> None:
        """5 Hz ROS2 timer — buffer'daki frame'leri process et."""
        with self._gz_lock:
            frames = dict(self._gz_frame_buffer)

        for drone_id, (gray, ts) in frames.items():
            # 1 saniyeden eski frame'i atla
            if _time.time() - ts > 1.0:
                continue
            if drone_id not in self._active_cams:
                continue

            self._cam_log_count += 1
            if self._cam_log_count <= 5 or self._cam_log_count % 100 == 0:
                self.get_logger().info(
                    f'📸 GZ frame #{self._cam_log_count} — drone{drone_id} '
                    f'({gray.shape[1]}x{gray.shape[0]})')

            self._process_gray_image(gray, drone_id)

            # Process edilen frame'i buffer'dan sil
            with self._gz_lock:
                self._gz_frame_buffer.pop(drone_id, None)

    def _on_camera_image(self, msg: RosImage, drone_id: int) -> None:
        """ROS2 image_raw callback (cv_bridge → grayscale → pyzbar)."""
        self._cam_log_count += 1
        if self._cam_log_count <= 5 or self._cam_log_count % 200 == 0:
            self.get_logger().info(
                f'📸 Kamera frame #{self._cam_log_count} — drone{drone_id} '
                f'({msg.width}x{msg.height})')

        if drone_id not in self._active_cams:
            return
        if not (_CV2_AVAILABLE and _CVBRIDGE_AVAILABLE and _PYZBAR_AVAILABLE):
            return
        if self._bridge is None:
            return
        try:
            cv_img = self._bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().warn(
                f'Goruntu donusum hatasi: {e}', throttle_duration_sec=5.0)
            return
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        self._process_gray_image(gray, drone_id)

    def _get_drone_altitude(self, drone_id: int) -> float:
        """Drone'un mevcut irtifasını döndür (pose z). Bilinmiyorsa 15.0 varsayılan."""
        pose = self._drone_poses.get(drone_id)
        if pose is not None:
            return abs(pose.pose.position.z)
        return 15.0  # varsayılan orta irtifa

    def _calc_zoom_factor(self, altitude: float) -> float:
        """
        İrtifaya göre adaptif zoom faktörü hesapla.
          10m → 2.0x    15m → 3.0x    20m → 4.0x    25m → 5.0x
        """
        zoom = altitude / _ZOOM_REF_ALT
        return max(_ZOOM_MIN, min(_ZOOM_MAX, zoom))

    def _find_qr_contour_crop(self, gray):
        """
        Beyaz dikdörtgen bölgeleri (QR kağıt) contour ile bul,
        crop edip decode et. Gazebo render'da en güvenilir yöntem.
        """
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        h, w = gray.shape
        candidates = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < 400:
                continue
            x, y, bw, bh = cv2.boundingRect(c)
            aspect = min(bw, bh) / max(bw, bh) if max(bw, bh) > 0 else 0
            if aspect > 0.5:
                candidates.append((area, x, y, bw, bh))

        candidates.sort(reverse=True)

        for area, x, y, bw, bh in candidates[:5]:
            pad = max(bw, bh) // 4
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + bw + pad)
            y2 = min(h, y + bh + pad)
            crop = gray[y1:y2, x1:x2]

            for z in [3, 4, 5, 6]:
                crop_up = cv2.resize(
                    crop, (crop.shape[1] * z, crop.shape[0] * z),
                    interpolation=cv2.INTER_CUBIC)
                r = pyzbar.decode(crop_up)
                if r:
                    return r
                _, bn = cv2.threshold(
                    crop_up, 0, 255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                r = pyzbar.decode(bn)
                if r:
                    return r
        return []

    def _process_gray_image(self, gray, drone_id: int) -> None:
        """
        Ortak pyzbar decode pipeline.
        1) Contour-based crop + zoom (en güvenilir)
        2) Parçalı tile tarama (fallback)

        Sadece trigger aktifken çalışır — yolda geçerken yanlış QR okumayı önler.
        """
        # Trigger aktif değilse decode yapma
        if not self._trigger_active:
            return

        # Kontrast artır (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        h, w = gray.shape
        altitude = self._get_drone_altitude(drone_id)
        zoom = self._calc_zoom_factor(altitude)
        zoom_int = max(2, int(round(zoom)))

        # 1) CONTOUR-BASED: QR'ı beyaz bölge olarak bul, crop et, decode et
        decoded_list = self._find_qr_contour_crop(gray)

        # 2) Fallback: parçalı tile tarama
        if not decoded_list:
            decoded_list = self._scan_tiles(gray, drone_id, zoom_int + 1)

        if not decoded_list:
            self._cam_log_count += 1
            if self._cam_log_count <= 10 or self._cam_log_count % 50 == 0:
                self.get_logger().info(
                    f'🔍 drone{drone_id} kamera — QR bulunamadı '
                    f'(gray {h}x{w}, alt={altitude:.0f}m, '
                    f'zoom={zoom_int}x)'
                )

        for obj in decoded_list:
            try:
                import json as _json
                data = _json.loads(obj.data.decode('utf-8'))
                qr_id = int(data.get('qr_id', 0))
            except Exception:
                continue

            if qr_id == 0 or qr_id in self._read_qr_ids:
                continue

            # Hedef QR filtresi — sadece hedef QR seq'ini kabul et
            if self._target_qr_seq > 0 and qr_id != self._target_qr_seq:
                self.get_logger().warn(
                    f'⚠️  QR{qr_id} okundu ama hedef QR#{self._target_qr_seq} '
                    f'— yoksayıldı (yolda geçiş)')
                continue

            self.get_logger().info(
                f'📷 [KAMERA] QR{qr_id} okundu — drone{drone_id} '
                f'(alt={altitude:.0f}m, zoom={zoom_int}x, faz={self._scan_phase})'
            )
            # Başarılı decode — kameralar açık kalsın sonraki QR'lar için

            # YAML pozisyonunu koru, içeriği kameradan al
            if qr_id in self._qr_nodes:
                qr_data = dict(self._qr_nodes[qr_id])
                qr_data['content'] = data
            else:
                qr_data = {
                    'content':  data,
                    'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
                }

            self._publish_qr_result(qr_id, qr_data)
            self._read_qr_ids.add(qr_id)

    def _scan_tiles(self, gray, drone_id: int, tile_zoom: int = 3):
        """
        Frame'i 3x3 overlapping tile'lara böl, her birini tile_zoom x büyütüp tara.
        %50 overlap — QR bir tile sınırına denk gelse bile komşu tile yakalar.

        tile_zoom: adaptif — yüksek irtifada daha agresif büyütme.
        """
        h, w = gray.shape
        tile_h = h // 2   # %50 overlap için tile boyutu = frame/2
        tile_w = w // 2
        step_h = h // 3   # 3 adım = 3x3 grid
        step_w = w // 3

        for row in range(3):
            for col in range(3):
                y0 = min(row * step_h, h - tile_h)
                x0 = min(col * step_w, w - tile_w)
                tile = gray[y0:y0 + tile_h, x0:x0 + tile_w]

                # Adaptif tile zoom — irtifa arttıkça daha fazla büyütme
                tile_up = cv2.resize(tile, (tile_w * tile_zoom, tile_h * tile_zoom),
                                     interpolation=cv2.INTER_LANCZOS4)
                decoded = pyzbar.decode(tile_up)
                if decoded:
                    return decoded
                # Threshold ile tekrar dene
                _, tile_bin = cv2.threshold(tile_up, 0, 255,
                                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                decoded = pyzbar.decode(tile_bin)
                if decoded:
                    return decoded

        return []

    def _on_pose(self, msg: PoseStamped, drone_id: int):
        self._drone_poses[drone_id] = msg

    def _on_local_state(self, msg: LocalState, drone_id: int):
        """Failover: primary kamera drone tehlikedeyse yedek devralır."""
        old_state = self._drone_states.get(drone_id, 'STANDBY')
        self._drone_states[drone_id] = msg.state

        if (drone_id == self._primary_cam_id
                and old_state not in _FAILOVER_STATES
                and msg.state in _FAILOVER_STATES
                and not self._failover_active):
            self._failover_active = True
            self._camera_drone_id = self._backup_cam_id
            self.get_logger().warn(
                f'⚠️  KAMERA FAILOVER: drone{self._primary_cam_id} → {msg.state}\n'
                f'   Yedek aktif: drone{self._backup_cam_id}')

        if (drone_id == self._primary_cam_id
                and self._failover_active
                and msg.state == _RECOVERY_STATE):
            self._failover_active = False
            self._camera_drone_id = self._primary_cam_id
            self.get_logger().info(
                f'✅ Kamera primary\'e döndü: drone{self._primary_cam_id}')

    # ── QR YAKIŞLIK KONTROLÜ (10 Hz) ────────────────────────────────────

    def _check_qr_proximity(self):
        """
        Proximity fallback — SADECE ALL_SCAN fazında ve _PROXIMITY_FALLBACK_S
        geçtikten sonra devreye girer.  Kamera (pyzbar) her zaman önceliklidir.

        Akış:  LEADER kamera (1.5s) → NEAREST kamera (1.5s) → ALL kamera + proximity
        """
        # ── Proximity sadece ALL_SCAN fazında son çare ──────────────────
        if self._scan_phase != 'ALL_SCAN':
            return
        elapsed_all = _time.time() - self._scan_phase_start
        if elapsed_all < _PROXIMITY_FALLBACK_S:
            return  # ALL_SCAN fazında kameralar hâlâ deniyor

        # ── Centroid hesapla ────────────────────────────────────────────
        flying_poses = [
            p for i, p in self._drone_poses.items()
            if p is not None and self._drone_states.get(i, '') in (
                'FLYING', 'DETACH', 'REJOIN', 'LAND_ZONE', 'RETURN_HOME'
            )
        ]
        if flying_poses:
            cx = sum(p.pose.position.x for p in flying_poses) / len(flying_poses)
            cy = sum(p.pose.position.y for p in flying_poses) / len(flying_poses)
        else:
            cam_pose = self._drone_poses.get(self._camera_drone_id)
            if cam_pose is None:
                return
            cx = cam_pose.pose.position.x
            cy = cam_pose.pose.position.y

        for qr_id, qr_data in self._qr_nodes.items():
            if qr_id in self._read_qr_ids:
                continue

            qpos = qr_data.get('position', {})
            dx   = cx - float(qpos.get('x', 0.0))
            dy   = cy - float(qpos.get('y', 0.0))
            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= self._trigger_radius:
                self.get_logger().warn(
                    f'⚠️  [PROXIMITY FALLBACK] QR{qr_id} — kamera okuyamadı, '
                    f'YAML fallback! mesafe={dist:.2f}m')
                self._publish_qr_result(qr_id, qr_data)
                self._read_qr_ids.add(qr_id)
                # Fallback başarılı → taramayı kapat
                self._scan_phase  = 'IDLE'
                self._active_cams = set()

    # ── QR SONUCU YAYINLAMA ──────────────────────────────────────────────

    def _publish_qr_result(self, qr_id: int, qr_data: dict):
        """
        Şekil 2 JSON yapısını parse et → QRResult mesajı yayınla.

        YAML content:
          gorev.formasyon          → formation_active, formation_type
          gorev.manevra_pitch_roll → maneuver_active, pitch_deg, roll_deg
          gorev.irtifa_degisim     → altitude_active, altitude
          gorev.bekleme_suresi_s   → wait_seconds
          suruden_ayrilma          → detach_active, detach_drone_id, zone_color,
                                     detach_wait_seconds
          sonraki_qr[team_key]     → next_qr_id
        """
        content = qr_data.get('content', {})
        if not content:
            self.get_logger().warn(f'[QR{qr_id}] content alanı boş → DROP')
            return

        # ── sonraki_qr ────────────────────────────────────────────────
        sonraki_qr = content.get('sonraki_qr', {})
        if self._team_key not in sonraki_qr:
            self.get_logger().warn(
                f'[QR{qr_id}] sonraki_qr["{self._team_key}"] yok → DROP')
            return
        next_qr_id = int(sonraki_qr[self._team_key])

        # ── gorev alanları ────────────────────────────────────────────
        gorev     = content.get('gorev', {})
        frm       = gorev.get('formasyon',          {})
        maneuver  = gorev.get('manevra_pitch_roll',  {})
        irtifa    = gorev.get('irtifa_degisim',      {})
        bekleme   = gorev.get('bekleme_suresi_s',     3)

        # ── suruden_ayrilma ──────────────────────────────────────────
        ayrilma   = content.get('suruden_ayrilma', {})

        # ── MESAJ ────────────────────────────────────────────────────
        msg = QRResult()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.team_id = self._team_id
        msg.qr_id   = int(qr_id)

        # Formasyon
        msg.formation_active = bool(frm.get('aktif', False))
        msg.formation_type   = str(frm.get('tip',   'OKBASI'))
        msg.drone_spacing    = 5.0   # sabit — şartname §5.2.1 (intent_coordinator default ile tutarlı)

        # İrtifa
        msg.altitude_active  = bool(irtifa.get('aktif', False))
        msg.altitude         = float(irtifa.get('deger', 15.0))

        # Manevra
        msg.maneuver_active  = bool(maneuver.get('aktif', False))
        msg.pitch_deg        = float(maneuver.get('pitch_deg', '0'))
        msg.roll_deg         = float(maneuver.get('roll_deg',  '0'))

        # Sürüden ayrılma
        msg.detach_active   = bool(ayrilma.get('aktif', False))
        msg.detach_drone_id = int(ayrilma.get('ayrilacak_drone_id') or 0)
        msg.zone_color      = str(ayrilma.get('hedef_renk') or '')

        # Zamanlama
        msg.next_qr_id   = next_qr_id
        msg.wait_seconds = float(bekleme)

        # Bu QR'ın konumu
        qpos = qr_data.get('position', {})
        msg.qr_position.x = float(qpos.get('x', 0.0))
        msg.qr_position.y = float(qpos.get('y', 0.0))
        msg.qr_position.z = float(qpos.get('z', 0.0))

        # Sonraki QR konumu (next_qr_id=0 → HOME)
        if next_qr_id != 0 and next_qr_id in self._qr_nodes:
            npos = self._qr_nodes[next_qr_id].get('position', {})
            msg.next_qr_position.x = float(npos.get('x', 0.0))
            msg.next_qr_position.y = float(npos.get('y', 0.0))
            msg.next_qr_position.z = float(npos.get('z', 0.0))

        self._qr_pub.publish(msg)

        # ── LOG ──────────────────────────────────────────────────────
        ayrilma_str = (f'drone{msg.detach_drone_id}→{msg.zone_color}'
                       if msg.detach_active else '—')
        home_str    = ' ← SON QR → 🏠 HOME!' if next_qr_id == 0 else ''
        self.get_logger().info(
            f'\n╔══ 📷 QR{qr_id} OKUNDU [drone{self._camera_drone_id}] ══\n'
            f'║  Formasyon  : {msg.formation_type} '
            f'[{"✅" if msg.formation_active else "—"}]\n'
            f'║  İrtifa     : {msg.altitude}m '
            f'[{"✅" if msg.altitude_active else "—"}]\n'
            f'║  Manevra    : pitch={msg.pitch_deg}° roll={msg.roll_deg}° '
            f'[{"✅" if msg.maneuver_active else "—"}]\n'
            f'║  Ayırma     : {ayrilma_str} '
            f'[{"✅" if msg.detach_active else "—"}]\n'
            f'║  Sonraki QR : {next_qr_id}{home_str}\n'
            f'║  Bekle      : {msg.wait_seconds}s\n'
            f'╚{"═"*40}'
        )

    # ── RENK ZONE YAYINI (1 Hz) ──────────────────────────────────────────

    def _publish_color_zones(self):
        """1 Hz: tüm renk bölgelerini /perception/color_zones'a yayınla."""
        if not self._color_zones:
            return

        msg = ColorZoneList()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        for z in self._color_zones:
            zone           = ColorZone()
            zone.position.x = float(z.get('x',      0.0))
            zone.position.y = float(z.get('y',      0.0))
            zone.position.z = float(z.get('z',      0.0))
            zone.color      = str(z.get('color',   'RED'))
            zone.radius     = float(z.get('radius',  3.0))
            msg.zones.append(zone)

        self._zone_pub.publish(msg)

    # ── YARDIMCI ─────────────────────────────────────────────────────────

    def reset_qr_memory(self):
        """Okunan QR'ları sıfırla (mission_fsm RESET komutu için)."""
        self._read_qr_ids.clear()
        self.get_logger().info('🔄 QR belleği sıfırlandı.')

    def get_unread_qr_ids(self) -> list[int]:
        """Henüz okunmamış QR ID'lerini döndür (test)."""
        return [q for q in self._qr_nodes if q not in self._read_qr_ids]


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main(args=None):
    rclpy.init(args=args)
    node = QRPerception()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('⛔ qr_perception durduruluyor...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
