#!/usr/bin/env python3
"""
2026 TEKNOFEST SÜRÜ İHA — Doğrudan MAVROS Formasyon Testi
==========================================================
formation_controller / intent pipeline BYPASS eder.
Doğrudan /drone{i}/mavros/setpoint_position/local yazar.

Dronlar:
  1) ARM + GUIDED moduna alınır
  2) 10m irtifaya çıkar (hover)
  3) OKBASI şekli → 10 saniye
  4) V şekli      → 10 saniye
  5) CİZGİ şekli  → 10 saniye

Şartname formasyonları (spacing=5m, yaw=0 = kuzeye/doğuya):
  OKBASI: drone1 öne, drone2/3 sol-arka/sağ-arka
  V     : drone1 öne, drone2/3 daha geniş açıyla
  CIZGI : yan yana çizgi

KULLANIM:
  cd ~/gz_ws && source install/setup.bash
  python3 src/my_swarm_pkg/scripts/test_formations_direct.py
"""

import math, time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# ── PARAMETRELER ──────────────────────────────────────────────────
HOVER_ALT  = 10.0   # hover irtifası (metre)
SPACING    = 5.0    # drone'lar arası mesafe
SURE_HOVER = 8.0    # kalkış hover süresi (sn)
SURE_FORMASYON = 12.0  # her formasyonda bekleme süresi (sn)
YAW        = 0.0    # ileri yön (radyan, 0=doğu/kuzey)

# Merkez pozisyon (home)
CX, CY = 0.0, 0.0

BEST_EFFORT_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


def formasyon_ofsetleri(tip: str, spacing: float, yaw: float) -> list:
    """
    Şartname formasyonları için her drone'un (dx, dy) ofsetini hesapla.
    Returns: [(dx1,dy1), (dx2,dy2), (dx3,dy3)]

    Koordinat: ENU (x=doğu, y=kuzey)
    yaw: sürünün ilerleme yönü (radyan)
    """
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)

    def dondur(lx, ly):
        """Yerel formasyon koordinatını ENU'ya döndür."""
        return (lx * cos_y - ly * sin_y,
                lx * sin_y + ly * cos_y)

    if tip == 'OKBASI':
        # Ok başı: lider öne, diğerleri sol-arka/sağ-arka (dar açı)
        raw = [
            ( 2/3 * spacing,  0.0),           # drone1: öne
            (-1/3 * spacing, -0.5 * spacing),  # drone2: sol-arka
            (-1/3 * spacing,  0.5 * spacing),  # drone3: sağ-arka
        ]
    elif tip == 'V':
        # V şekli: lider öne, diğerleri daha geniş açıyla
        raw = [
            ( 2/3 * spacing,  0.0),
            (-1/3 * spacing, -1.0 * spacing),  # 2x daha geniş
            (-1/3 * spacing,  1.0 * spacing),
        ]
    elif tip == 'CIZGI':
        # Çizgi: yan yana, harekete dik
        raw = [
            (0.0,  0.0),                       # drone1: orta
            (0.0,  1.0 * spacing),             # drone2: sol
            (0.0, -1.0 * spacing),             # drone3: sağ
        ]
    else:
        raw = [(0.0, 0.0)] * 3

    return [dondur(lx, ly) for lx, ly in raw]


class FormasyonTest(Node):

    def __init__(self):
        super().__init__('formasyon_direct_test')
        self._states = {i: None for i in range(1, 4)}
        self._pubs = {}

        for i in range(1, 4):
            ns = f'drone{i}'
            # Setpoint publisher
            self._pubs[i] = self.create_publisher(
                PoseStamped,
                f'/{ns}/mavros/setpoint_position/local', 10
            )
            # State subscriber (MAVROS)
            self.create_subscription(
                State,
                f'/{ns}/mavros/state',
                lambda m, i=i: self._states.update({i: m}),
                BEST_EFFORT_QOS
            )

        self.get_logger().info(
            '\n╔════════════════════════════════════════╗\n'
            '║  DOĞRUDAN FORMASYON TESTİ              ║\n'
            '║  MAVROS setpoint_position/local         ║\n'
            '║  OKBASI → V → CIZGI                    ║\n'
            '╚════════════════════════════════════════╝'
        )

    def _setpoint_gonder(self, drone_id: int, x: float, y: float, z: float):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.pose.orientation.w = 1.0
        self._pubs[drone_id].publish(msg)

    def _formasyon_gonder(self, tip: str, cx: float, cy: float,
                          alt: float, yaw: float, sure: float):
        """Belirtilen formasyonu `sure` saniye boyunca 10 Hz ile yayınla."""
        ofsetler = formasyon_ofsetleri(tip, SPACING, yaw)
        adim = 0.1  # 10 Hz
        n = int(sure / adim)
        for _ in range(n):
            for i in range(1, 4):
                dx, dy = ofsetler[i - 1]
                self._setpoint_gonder(i, cx + dx, cy + dy, alt)
            rclpy.spin_once(self, timeout_sec=adim)

    def arm_ve_guided(self):
        """Tüm dronları ARM + GUIDED moda al."""
        for i in range(1, 4):
            ns = f'drone{i}/mavros'
            # SetMode: GUIDED
            set_mode = self.create_client(SetMode, f'/{ns}/set_mode')
            arm_cli  = self.create_client(CommandBool, f'/{ns}/cmd/arming')

            if not set_mode.wait_for_service(timeout_sec=5.0):
                self.get_logger().error(f'drone{i} SetMode servisi yok!')
                continue
            if not arm_cli.wait_for_service(timeout_sec=5.0):
                self.get_logger().error(f'drone{i} Arming servisi yok!')
                continue

            # GUIDED mod
            req = SetMode.Request()
            req.custom_mode = 'GUIDED'
            set_mode.call_async(req)
            time.sleep(0.3)

            # ARM
            arm_req = CommandBool.Request()
            arm_req.value = True
            arm_cli.call_async(arm_req)
            self.get_logger().info(f'drone{i}: GUIDED + ARM gönderildi')
            time.sleep(0.2)

    def calistir(self):
        # State'leri al
        self.get_logger().info('MAVROS durumları kontrol ediliyor...')
        t = time.time()
        while time.time() - t < 4:
            rclpy.spin_once(self, timeout_sec=0.1)

        for i, s in self._states.items():
            if s:
                self.get_logger().info(
                    f'drone{i}: connected={s.connected} armed={s.armed} mode={s.mode}')
            else:
                self.get_logger().warn(f'drone{i}: MAVROS state yok!')

        # ARM + GUIDED
        self.get_logger().info('\n[1/5] ARM + GUIDED moduna alınıyor...')
        self.arm_ve_guided()
        time.sleep(2.0)

        # TAKEOFF: setpoint öncesi ~50 paket gönder (OFFBOARD ön koşulu)
        self.get_logger().info(f'[2/5] KALKIŞ: {HOVER_ALT}m irtifaya çıkılıyor...')
        for _ in range(50):
            for i in range(1, 4):
                self._setpoint_gonder(i, CX, CY, HOVER_ALT)
            rclpy.spin_once(self, timeout_sec=0.05)

        # Hover
        self._formasyon_gonder('OKBASI', CX, CY, HOVER_ALT, YAW, SURE_HOVER)
        self.get_logger().info(f'  → {HOVER_ALT}m irtifada hover yapılıyor')

        # OKBASI
        self.get_logger().info('\n[3/5] OKBASI FORMASYONU...')
        self.get_logger().info(
            f'  drone1: (+{2/3*SPACING:.1f}m, 0)  — ÖNE\n'
            f'  drone2: (-{1/3*SPACING:.1f}m, -{0.5*SPACING:.1f}m) — SOL-ARKA\n'
            f'  drone3: (-{1/3*SPACING:.1f}m, +{0.5*SPACING:.1f}m) — SAĞ-ARKA'
        )
        self._formasyon_gonder('OKBASI', CX, CY, HOVER_ALT, YAW, SURE_FORMASYON)
        self.get_logger().info('  ✓ OKBASI tamamlandı')

        # V
        self.get_logger().info('\n[4/5] V FORMASYONU...')
        self.get_logger().info(
            f'  drone1: (+{2/3*SPACING:.1f}m, 0)  — ÖNE\n'
            f'  drone2: (-{1/3*SPACING:.1f}m, -{SPACING:.1f}m) — SOL-ARKA (geniş)\n'
            f'  drone3: (-{1/3*SPACING:.1f}m, +{SPACING:.1f}m) — SAĞ-ARKA (geniş)'
        )
        self._formasyon_gonder('V', CX, CY, HOVER_ALT, YAW, SURE_FORMASYON)
        self.get_logger().info('  ✓ V tamamlandı')

        # CIZGI
        self.get_logger().info('\n[5/5] CIZGI FORMASYONU...')
        self.get_logger().info(
            f'  drone2: (0, +{SPACING:.1f}m) — SOL\n'
            f'  drone1: (0,     0)  — ORTA\n'
            f'  drone3: (0, -{SPACING:.1f}m) — SAĞ'
        )
        self._formasyon_gonder('CIZGI', CX, CY, HOVER_ALT, YAW, SURE_FORMASYON)
        self.get_logger().info('  ✓ CIZGI tamamlandı')

        self.get_logger().info(
            '\n╔════════════════════════════════════════╗\n'
            '║  TÜM FORMASYONLAR TAMAMLANDI ✓         ║\n'
            '║  OKBASI ✓ | V ✓ | CIZGI ✓             ║\n'
            '╚════════════════════════════════════════╝'
        )


def main():
    rclpy.init()
    node = FormasyonTest()
    try:
        node.calistir()
    except KeyboardInterrupt:
        node.get_logger().info('Durduruldu.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
