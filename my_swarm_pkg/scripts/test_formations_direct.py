#!/usr/bin/env python3
"""
TEKNOFEST 2026 — Formasyon Testi (v6 — Doğru Pipeline)
========================================================
PIPELINE:
  Bu script → /{ns}/setpoint_raw → collision_avoidance → /{ns}/setpoint_final
  → drone_interface → MAVROS → ArduPilot

  Çarpışma önleme (APF) collision_avoidance node'unda çalışır.
  Bu script sadece formasyon hedeflerini hesaplayıp setpoint_raw'a yazar.

ARM/GUIDED/TAKEOFF:
  Bunlar servis çağrısı — pipeline'dan geçmez.
  Doğrudan MAVROS servislerine gönderilir.

FORMASYON OFSETLERİ (Şartname Şekil 3):
  OKBASI: Lider ÖNDE (ok ucu >), takipçiler ARKADA yanlarda
  V:      Lider ARKADA (V dibi <), takipçiler ÖNDE yanlarda
  CIZGI:  Yan yana dizilim (---)

KULLANIM:
  # Terminal 1: Launch (Gazebo + SITL + MAVROS + pipeline node'ları)
  cd ~/gz_ws && source install/setup.bash
  ros2 launch my_swarm_pkg swarm_competition.launch.py

  # Terminal 2: Test scripti (EKF mesajları geldikten sonra)
  export ROS_LOCALHOST_ONLY=1
  export FASTRTPS_DEFAULT_PROFILES_FILE=.../fastdds_no_shm.xml
  source ~/gz_ws/install/setup.bash
  python3 ~/gz_ws/src/my_swarm_pkg/scripts/test_formations_direct.py
"""

import math, time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, StreamRate
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import NavSatFix
from swarm_msgs.msg import LocalState

# ══════════════════════════════════════════════════════════════════════════════
# PARAMETRELER
# ══════════════════════════════════════════════════════════════════════════════
HOVER_ALT = 10.0
SPACING   = 5.0

BEST_EFFORT = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST, depth=10)

# ══════════════════════════════════════════════════════════════════════════════
# FORMASYON OFSETLERİ (Şartname Şekil 3)
# ══════════════════════════════════════════════════════════════════════════════
# (ileri, sol) — normalize edilmiş, SPACING ile çarpılınca drone'lar arası
# mesafe tam SPACING metre olur (eşkenar üçgen geometrisi).
#
# Eşkenar üçgen: kenar = SPACING
#   sin(60°) = 0.866 → ileri/geri ofset
#   cos(60°) = 0.5   → sağ/sol ofset
#
# Merkez (ağırlık merkezi) = (0, 0) olacak şekilde normalize edildi.
# Her drone çiftinin arasındaki mesafe = tam SPACING metre.
#
# OKBASI (>):          V (<):             CIZGI (---):
#      [1]                [2]   [3]        [2] [1] [3]
#     / \                  \ /
#   [2]   [3]              [1]
#
SIN60 = 0.866  # sin(60°)

OFFSETS = {
    'OKBASI': {
        # Ok başı: Lider ÖNDE, takipçiler ARKADA yanlarda
        # Eşkenar üçgen, ucu ileri bakıyor  >
        1: (+SIN60 * 2/3,  0.0),    # lider: önde
        2: (-SIN60 * 1/3, -0.5),    # sol-arka
        3: (-SIN60 * 1/3, +0.5),    # sağ-arka
    },
    'V': {
        # V formasyonu: Lider ARKADA, takipçiler ÖNDE yanlarda
        # Eşkenar üçgen, açık tarafı ileri bakıyor  <
        1: (-SIN60 * 2/3,  0.0),    # lider: arkada (V'nin dibi)
        2: (+SIN60 * 1/3, -0.5),    # sol-ön (V'nin sol kolu)
        3: (+SIN60 * 1/3, +0.5),    # sağ-ön (V'nin sağ kolu)
    },
    'CIZGI': {
        # Çizgi: Yan yana dizilim
        # Mesafe: drone1↔drone2 = SPACING, drone1↔drone3 = SPACING
        1: ( 0.0,  0.0),   # orta
        2: ( 0.0, -1.0),   # sol (1*SPACING = 5m)
        3: ( 0.0, +1.0),   # sağ (1*SPACING = 5m)
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# GPS YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════

def gps_to_meter(lat1, lon1, lat2, lon2):
    """İki GPS noktası arası metre cinsinden (dx_east, dy_north)."""
    R = 6371000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    avg_lat = math.radians((lat1 + lat2) / 2)
    dy = dlat * R
    dx = dlon * R * math.cos(avg_lat)
    return dx, dy


def meter_to_gps(lat_ref, lon_ref, dx_east, dy_north):
    """Metre ofsetini GPS koordinatına çevir."""
    R = 6371000.0
    new_lat = lat_ref + math.degrees(dy_north / R)
    new_lon = lon_ref + math.degrees(dx_east / (R * math.cos(math.radians(lat_ref))))
    return new_lat, new_lon


# ══════════════════════════════════════════════════════════════════════════════
# ANA NODE
# ══════════════════════════════════════════════════════════════════════════════

class Test(Node):
    def __init__(self):
        super().__init__('ftest')
        self.poses = {}     # local position {drone_id: PoseStamped}
        self.states = {}    # MAVROS state {drone_id: State}
        self.gps = {}       # GPS koordinatları {drone_id: (lat, lon, alt)}
        self.hedefler = {}  # formasyon hedefleri {drone_id: (x, y, z) local frame}
        self.pubs_raw = {}  # setpoint_raw publisher'ları (pipeline'a girer)
        self.pubs_local_state = {}  # LocalState publisher'ları
        self._state_seq = 0
        self.yayinla_aktif = False

        for i in range(1, 4):
            ns = f'drone{i}'

            # ── PIPELINE TOPIC: setpoint_raw ────────────────────────────────
            # Bu topic'e yazılan veri şu yoldan geçer:
            #   setpoint_raw → collision_avoidance → setpoint_final → drone_interface → MAVROS
            # Yani çarpışma önleme OTOMATİK devreye girer!
            self.pubs_raw[i] = self.create_publisher(
                PoseStamped, f'/{ns}/setpoint_raw', 10)

            # ── KRİTİK: collision_avoidance komşuları FLYING state'de görmeli ──
            # Yoksa APF devreye GİRMEZ (pass-through yapar)
            self.pubs_local_state[i] = self.create_publisher(
                LocalState, f'/drone{i}/local_state', 10)

            # ── Okuma: State, Pozisyon, GPS ─────────────────────────────────
            self.create_subscription(
                State, f'/{ns}/mavros/state',
                lambda m, i=i: self.states.update({i: m}), BEST_EFFORT)
            self.create_subscription(
                PoseStamped, f'/{ns}/mavros/local_position/pose',
                lambda m, i=i: self.poses.update({i: m}), BEST_EFFORT)
            self.create_subscription(
                NavSatFix, f'/{ns}/mavros/global_position/global',
                lambda m, i=i: self.gps.update({i: (m.latitude, m.longitude, m.altitude)}),
                BEST_EFFORT)

        self.create_timer(0.05, self._yayinla)  # 20Hz
        self.create_timer(0.1, self._yayinla_local_state)  # 10Hz

    # ══════════════════════════════════════════════════════════════════════════
    # LOCAL STATE YAYINLAMA (10Hz) — collision_avoidance için FLYING state
    # ══════════════════════════════════════════════════════════════════════════

    def _yayinla_local_state(self):
        """
        Her drone için FLYING state yayınla.
        collision_avoidance bu mesajı görünce komşuyu 'aktif' sayar
        ve APF itici kuvvet hesaplar. Bu olmadan CA pass-through yapar!
        """
        if not self.yayinla_aktif:
            return
        self._state_seq += 1
        for i in range(1, 4):
            msg = LocalState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.drone_id = i
            msg.state = 'FLYING'
            msg.seq = self._state_seq
            self.pubs_local_state[i].publish(msg)

    # ══════════════════════════════════════════════════════════════════════════
    # SETPOINT YAYINLAMA (20Hz) — setpoint_raw'a yazar
    # ══════════════════════════════════════════════════════════════════════════

    def _yayinla(self):
        """
        20Hz timer callback.
        Hedef pozisyonları setpoint_raw topic'ine yazar.
        collision_avoidance node'u bu topic'i dinler, APF uygular,
        setpoint_final'a yazar. drone_interface de MAVROS'a gönderir.
        """
        if not self.yayinla_aktif:
            return
        for i in range(1, 4):
            if i not in self.hedefler:
                continue
            x, y, z = self.hedefler[i]
            msg = PoseStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'map'
            msg.pose.position.x = float(x)
            msg.pose.position.y = float(y)
            msg.pose.position.z = float(z)
            msg.pose.orientation.w = 1.0
            self.pubs_raw[i].publish(msg)

    # ══════════════════════════════════════════════════════════════════════════
    # YARDIMCI METODLAR
    # ══════════════════════════════════════════════════════════════════════════

    def _spin_sure(self, sn):
        t = time.time()
        while time.time() - t < sn:
            rclpy.spin_once(self, timeout_sec=0.05)

    def _servis(self, srv_type, topic, req, timeout=5.0):
        cli = self.create_client(srv_type, topic)
        if not cli.wait_for_service(timeout_sec=timeout):
            return None
        fut = cli.call_async(req)
        t = time.time()
        while time.time() - t < timeout:
            rclpy.spin_once(self, timeout_sec=0.05)
            if fut.done():
                return fut.result()
        return None

    # ══════════════════════════════════════════════════════════════════════════
    # FORMASYON HESAPLAMA
    # ══════════════════════════════════════════════════════════════════════════

    def formasyon_uygula(self, tip):
        """
        GPS tabanlı formasyon hesaplama.

        1) Tüm dronların GPS ortalaması = merkez
        2) Formasyon ofseti → hedef GPS
        3) Hedef GPS - kendi GPS = metre ofset
        4) Mevcut local pozisyon + ofset = hedef local pozisyon
        5) Bu hedef setpoint_raw'a yazılır → collision_avoidance → MAVROS
        """
        if len(self.gps) < 3:
            self.get_logger().error('GPS verisi eksik!')
            return

        # 1) Merkez GPS
        avg_lat = sum(g[0] for g in self.gps.values()) / 3
        avg_lon = sum(g[1] for g in self.gps.values()) / 3
        self.get_logger().info(f'  GPS merkez: ({avg_lat:.6f}, {avg_lon:.6f})')

        # Dronelar arası mevcut mesafeler
        for a in range(1, 4):
            for b in range(a + 1, 4):
                if a in self.gps and b in self.gps:
                    dx, dy = gps_to_meter(
                        self.gps[a][0], self.gps[a][1],
                        self.gps[b][0], self.gps[b][1])
                    dist = math.sqrt(dx * dx + dy * dy)
                    self.get_logger().info(
                        f'  drone{a}<->drone{b} mesafe: {dist:.1f}m')

        # 2-4) Her drone'un hedef pozisyonunu hesapla
        offsets = OFFSETS[tip]
        for i in range(1, 4):
            fwd, left = offsets[i]
            dx_east  = fwd * SPACING
            dy_north = left * SPACING

            hedef_lat, hedef_lon = meter_to_gps(avg_lat, avg_lon, dx_east, dy_north)

            my_lat, my_lon, my_alt = self.gps[i]
            lokal_dx, lokal_dy = gps_to_meter(my_lat, my_lon, hedef_lat, hedef_lon)

            p = self.poses.get(i)
            if p:
                cur_x = p.pose.position.x
                cur_y = p.pose.position.y
            else:
                cur_x, cur_y = 0.0, 0.0

            self.hedefler[i] = (cur_x + lokal_dx, cur_y + lokal_dy, HOVER_ALT)
            self.get_logger().info(
                f'  drone{i}: hedef=({cur_x+lokal_dx:.1f}, {cur_y+lokal_dy:.1f}) '
                f'[ofset: dx={lokal_dx:.1f}m dy={lokal_dy:.1f}m]')

    # ══════════════════════════════════════════════════════════════════════════
    # ANA ÇALIŞTIRMA SEKVANSI
    # ══════════════════════════════════════════════════════════════════════════

    def calistir(self):
        # ── 1) Stream rate ──────────────────────────────────────────────────
        self.get_logger().info('=== STREAM RATE ===')
        for i in range(1, 4):
            req = StreamRate.Request()
            req.stream_id = 0
            req.message_rate = 10
            req.on_off = True
            self._servis(StreamRate, f'/drone{i}/mavros/set_stream_rate', req)
        self.get_logger().info('  Tum stream rate: 10Hz')

        # ── 2) Pozisyon + GPS oku ───────────────────────────────────────────
        self.get_logger().info('=== POZISYON + GPS OKUMA (15sn) ===')
        self._spin_sure(15.0)

        for i in range(1, 4):
            p = self.poses.get(i)
            g = self.gps.get(i)
            local_str = f'x={p.pose.position.x:.2f} y={p.pose.position.y:.2f} z={p.pose.position.z:.2f}' if p else 'YOK'
            gps_str = f'lat={g[0]:.6f} lon={g[1]:.6f}' if g else 'YOK'
            self.get_logger().info(f'  drone{i}: local=[{local_str}] gps=[{gps_str}]')

        if len(self.gps) < 3:
            self.get_logger().error('GPS alinamadi!')
            return

        # Baslangic mesafeleri
        self.get_logger().info('\n=== BASLANGIC MESAFELERI ===')
        for a in range(1, 4):
            for b in range(a + 1, 4):
                if a in self.gps and b in self.gps:
                    dx, dy = gps_to_meter(
                        self.gps[a][0], self.gps[a][1],
                        self.gps[b][0], self.gps[b][1])
                    dist = math.sqrt(dx * dx + dy * dy)
                    durum = "TEHLIKE! APF aktif olacak" if dist < 8.0 else "OK"
                    self.get_logger().info(
                        f'  drone{a}<->drone{b}: {dist:.1f}m [{durum}]')

        # ── 3) ARM + GUIDED + TAKEOFF ──────────────────────────────────────
        # Bunlar MAVROS servisleri — pipeline'dan gecmez
        self.get_logger().info('\n=== ARM + GUIDED + TAKEOFF ===')
        for i in range(1, 4):
            req = SetMode.Request()
            req.custom_mode = 'GUIDED'
            self._servis(SetMode, f'/drone{i}/mavros/set_mode', req)
        self.get_logger().info('  GUIDED OK')
        self._spin_sure(0.5)

        for i in range(1, 4):
            req = CommandBool.Request()
            req.value = True
            self._servis(CommandBool, f'/drone{i}/mavros/cmd/arming', req)
        self.get_logger().info('  ARM OK')
        self._spin_sure(0.5)

        for i in range(1, 4):
            req = CommandTOL.Request()
            req.altitude = HOVER_ALT
            self._servis(CommandTOL, f'/drone{i}/mavros/cmd/takeoff', req)
        self.get_logger().info(f'  TAKEOFF {HOVER_ALT}m OK')

        # ── 4) Kalkis bekle — setpoint GONDERME ───────────────────────────
        # drone_interface altitude gate: z < 9m ise setpoint engeller
        # Bu dogru davranis — TAKEOFF sırasında setpoint göndermemeliyiz
        self.get_logger().info('\n=== KALKIS BEKLENIYOR (25sn) ===')
        self.get_logger().info('  Setpoint gonderilmiyor — TAKEOFF iptal olmasin!')
        t0 = time.time()
        while time.time() - t0 < 25.0:
            rclpy.spin_once(self, timeout_sec=0.1)
            elapsed = time.time() - t0
            if int(elapsed) % 5 == 0 and int(elapsed * 10) % 50 == 0:
                for i in range(1, 4):
                    p = self.poses.get(i)
                    if p:
                        self.get_logger().info(
                            f'  drone{i}: z={p.pose.position.z:.1f}m')

        # ── 5) Setpoint aktif — hover ─────────────────────────────────────
        # Artık dronelar 10m'de — setpoint_raw'a yazmaya baslayabiliriz
        # collision_avoidance APF uygulayacak, drone_interface MAVROS'a gonderecek
        self.get_logger().info('\n=== SETPOINT AKTIF (pipeline: setpoint_raw -> CA -> drone_interface -> MAVROS) ===')
        for i in range(1, 4):
            p = self.poses.get(i)
            if p:
                self.hedefler[i] = (
                    p.pose.position.x, p.pose.position.y, HOVER_ALT)
        self.yayinla_aktif = True
        self._spin_sure(3.0)

        # ── 6) FORMASYONLAR ───────────────────────────────────────────────
        for tip in ['OKBASI', 'V', 'CIZGI']:
            self.get_logger().info(f'\n{"="*50}')
            self.get_logger().info(f'=== {tip} FORMASYONU ===')
            self.get_logger().info(f'{"="*50}')

            self.formasyon_uygula(tip)

            self.get_logger().info(f'  Gecis yapiliyor (20sn)...')
            self._spin_sure(20.0)

            # Formasyon sonrasi mesafeler
            self.get_logger().info(f'  {tip} — Drone mesafeleri:')
            for a in range(1, 4):
                for b in range(a + 1, 4):
                    if a in self.gps and b in self.gps:
                        dx, dy = gps_to_meter(
                            self.gps[a][0], self.gps[a][1],
                            self.gps[b][0], self.gps[b][1])
                        dist = math.sqrt(dx * dx + dy * dy)
                        self.get_logger().info(
                            f'    drone{a}<->drone{b}: {dist:.1f}m')

            self.get_logger().info(
                f'  {tip} TAMAM — EKRAN GORUNTSU AL! (15sn bekleniyor)')
            self._spin_sure(15.0)

        self.get_logger().info('\n=== TUM FORMASYONLAR TAMAMLANDI ===')


def main():
    rclpy.init()
    node = Test()
    try:
        node.calistir()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
