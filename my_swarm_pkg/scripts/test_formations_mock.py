#!/usr/bin/env python3
"""
2026 TEKNOFEST SÜRÜ İHA — Formasyon Şekil Testi
=================================================
QR navigasyona gerek yok — bu script SADECE formasyon şekillerini test eder.
Dronlar aynı noktada (hover) durur, sırayla OKBASI → V → CIZGI şekline geçer.

Şartname formasyonları:
  OKBASI : Ok başı — lider öne, diğer ikisi sol-arka ve sağ-arka
  V      : V şekli — OKBASI'dan daha geniş açı
  CIZGI  : Çizgi  — 3 drone yan yana, harekete dik

KULLANIM:
  Terminal 1: ros2 launch my_swarm_pkg swarm_competition.launch.py
  Terminal 2: cd ~/gz_ws && source install/setup.bash
              python3 src/my_swarm_pkg/scripts/test_formations_mock.py
"""

import math, time, rclpy
from rclpy.node import Node
from swarm_msgs.msg import SwarmIntent

# ── PARAMETRELER ──────────────────────────────────────────────────────────────
IRTIFA      = 10.0   # metre
SPACING     = 5.0    # drone'lar arası mesafe (şartname örn: 5m)
SURE        = 15.0   # her formasyonda bekleme süresi (saniye)
HOVER_X     = 0.0    # hover noktası (dronlar zaten burada başlıyor)
HOVER_Y     = 0.0


class FormasyonTesti(Node):

    def __init__(self):
        super().__init__('formasyon_testi')
        self._pub = self.create_publisher(SwarmIntent, '/swarm/intent', 10)
        self._seq = self._mevcut_seq() + 1
        self.get_logger().info(
            f'\n╔══════════════════════════════════════╗\n'
            f'║  FORMASYON ŞEKİL TESTİ               ║\n'
            f'║  OKBASI → V → CIZGI                  ║\n'
            f'║  İrtifa: {IRTIFA}m | Spacing: {SPACING}m        ║\n'
            f'╚══════════════════════════════════════╝\n'
            f'  Başlangıç seq: {self._seq}'
        )

    def _mevcut_seq(self) -> int:
        """Mevcut /swarm/intent seq'ini oku, üstünden devam et."""
        toplananlar = []
        sub = self.create_subscription(
            SwarmIntent, '/swarm/intent',
            lambda m: toplananlar.append(m.seq), 10
        )
        son = time.time() + 2.0
        while time.time() < son:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.destroy_subscription(sub)
        if toplananlar:
            seq = max(toplananlar)
            self.get_logger().info(f'  Mevcut seq: {seq}')
            return seq
        self.get_logger().info("  Seq okunamadı, 1000'den başlanıyor")
        return 1000

    def _intent_gonder(self, task, formasyon, yaw=0.0,
                       pitch=0.0, maneuver=False, sure=SURE):
        """Intent oluştur ve `sure` saniye boyunca 5 Hz ile yayınla."""
        m = SwarmIntent()
        m.leader_id          = 1
        m.task_id            = task
        m.formation_type     = formasyon
        m.drone_spacing      = float(SPACING)
        m.target_yaw         = float(yaw)
        m.target_pos.x       = float(HOVER_X)
        m.target_pos.y       = float(HOVER_Y)
        m.target_pos.z       = float(IRTIFA)
        m.drone_altitude     = float(IRTIFA)
        m.active_drone_count = 3
        m.maneuver_active    = maneuver
        m.maneuver_pitch_deg = float(pitch)
        m.maneuver_roll_deg  = 0.0
        m.join_drone_id      = 0
        m.detach_drone_id    = 0

        adim = 1.0 / 5.0  # 5 Hz
        for _ in range(int(sure / adim)):
            m.header.stamp = self.get_clock().now().to_msg()
            m.seq = self._seq;  self._seq += 1
            m.qr_seq = self._seq
            self._pub.publish(m)
            time.sleep(adim)

    def calistir(self):
        time.sleep(2.0)

        # ══ ADIM 1: ARM + KALKIŞ ════════════════════════════════════════════
        # Şartname: Sürü OKBASI formasyonunda belirtilen irtifaya çıkar
        self.get_logger().info(
            f'\n[1/4] KALKIŞ — ARM ediliyor, {IRTIFA}m irtifaya çıkılıyor...\n'
            f'      Şartname: Kalkışta OKBASI formasyon'
        )
        self._intent_gonder('IDLE', 'OKBASI', sure=15)  # ARM için 15 sn
        self._intent_gonder('QR_NAVIGATE', 'OKBASI', sure=10)  # kalkış

        # ══ ADIM 2: OKBASI FORMASYONU ════════════════════════════════════════
        # Şartname: Ok başı — lider öne, sol-arka, sağ-arka
        #
        #       ▲ (kuzey)
        #      [1]          rank-0 = drone1, öne  (+2/3 * 5m = +3.33m)
        #   [2]   [3]       rank-1 = sol-arka, rank-2 = sağ-arka
        #
        self.get_logger().info(
            f'\n[2/4] OKBASI FORMASYONU — {SURE} saniye\n'
            f'      Drone1: öne (+3.33m)\n'
            f'      Drone2: sol-arka  (-1.67m, -2.5m)\n'
            f'      Drone3: sağ-arka  (-1.67m, +2.5m)'
        )
        self._intent_gonder('QR_NAVIGATE', 'OKBASI', sure=SURE)
        self.get_logger().info('  ✓ OKBASI tamamlandı')

        # ══ ADIM 3: V FORMASYONU ══════════════════════════════════════════════
        # Şartname: V şekli — OKBASI'dan daha geniş açı
        #
        #       ▲ (kuzey)
        #      [1]          rank-0 = drone1, öne (+3.33m)
        #   [2]       [3]   rank-1 = sol-arka (-1.67m, -5m)  — OKBASI'dan 2x geniş
        #
        self.get_logger().info(
            f'\n[3/4] V FORMASYONU — {SURE} saniye\n'
            f'      Drone1: öne (+3.33m)\n'
            f'      Drone2: sol-arka  (-1.67m, -5m)\n'
            f'      Drone3: sağ-arka  (-1.67m, +5m)\n'
            f'      (OKBASI\'dan 2x daha geniş açı)'
        )
        self._intent_gonder('QR_NAVIGATE', 'V', sure=SURE)
        self.get_logger().info('  ✓ V tamamlandı')

        # ══ ADIM 4: CIZGI FORMASYONU ══════════════════════════════════════════
        # Şartname: Çizgi — 3 drone yan yana, harekete dik
        #
        #   [2]  [1]  [3]   ← yan yana çizgi (hareket yönüne dik)
        #        ▲ (kuzey/ileri)
        #
        self.get_logger().info(
            f'\n[4/4] CIZGI FORMASYONU — {SURE} saniye\n'
            f'      Drone1: orta  (0, 0)\n'
            f'      Drone2: sol   (0, +5m)\n'
            f'      Drone3: sağ   (0, -5m)\n'
            f'      (Yan yana çizgi)'
        )
        self._intent_gonder('QR_NAVIGATE', 'CIZGI', sure=SURE)
        self.get_logger().info('  ✓ CIZGI tamamlandı')

        self.get_logger().info(
            '\n╔══════════════════════════════════════╗\n'
            '║  TÜM FORMASYONLAR TEST EDİLDİ ✓      ║\n'
            '║  OKBASI ✓  |  V ✓  |  CIZGI ✓       ║\n'
            '╚══════════════════════════════════════╝'
        )


def main():
    rclpy.init()
    node = FormasyonTesti()
    try:
        node.calistir()
    except KeyboardInterrupt:
        node.get_logger().info('Durduruldu.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
