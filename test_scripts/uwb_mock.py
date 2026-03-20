#!/usr/bin/env python3
"""
uwb_mock.py — UWB Simülasyon Test Scripti
==========================================

AMAÇ:
  Fiziksel Nooploop donanımı olmadan UWB entegrasyonunu test eder.
  Mevcut GPS konumunu okuyup /mavros/vision_pose/pose'a yayınlar.
  Bu, UWB donanımının yapacağı şeyin birebir simülasyonudur.

TEST ADIMLARI:
  1) Normal launch ile 3 drone'u kaldır
  2) Bu scripti çalıştır:
       python3 test_scripts/uwb_mock.py
  3) GPS'i kes (MAVProxy terminalinde):
       param set SIM_GPS_DISABLE 1
  4) Drone'lar hover'da kalıyorsa → UWB entegrasyonu çalışıyor ✅
  5) GPS'i geri aç:
       param set SIM_GPS_DISABLE 0

NOT:
  ArduPilot parametrelerini Mission Planner'da önceden ayarla:
    EK3_SRC1_POSXY = 6
    EK3_SRC1_VELXY = 6
    VISO_TYPE      = 1
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import PoseStamped


DRONE_IDS = [1, 2, 3]


class UwbMock(Node):

    def __init__(self):
        super().__init__('uwb_mock')

        best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self._pubs = {}

        for drone_id in DRONE_IDS:
            ns = f'drone{drone_id}'

            self._pubs[drone_id] = self.create_publisher(
                PoseStamped,
                f'/{ns}/mavros/vision_pose/pose',
                10
            )

            self.create_subscription(
                PoseStamped,
                f'/{ns}/mavros/local_position/pose',
                lambda msg, did=drone_id: self._relay(msg, did),
                best_effort_qos
            )

        self.get_logger().info(
            '📡 UWB Mock başlatıldı\n'
            f'   Drone\'lar : {DRONE_IDS}\n'
            '   GPS konumu → vision_pose/pose aktarılıyor\n'
            '   GPS\'i kesmek için MAVProxy\'de:\n'
            '     param set SIM_GPS_DISABLE 1'
        )

    def _relay(self, msg: PoseStamped, drone_id: int):
        """GPS konumunu UWB pozisyonu olarak vision_pose'a ilet."""
        msg.header.frame_id = 'map'
        self._pubs[drone_id].publish(msg)


def main():
    rclpy.init()
    node = UwbMock()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('⛔ UWB Mock durduruluyor...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
