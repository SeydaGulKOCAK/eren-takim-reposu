#!/usr/bin/env python3
"""
TEKNOFEST 2026 — Çarpışma Önleme (APF) Testi v3
==================================================
PIPELINE ÜZERİNDEN çalışır:
  Bu script → /{ns}/setpoint_raw → collision_avoidance → /{ns}/setpoint_final
  → drone_interface → MAVROS → ArduPilot

  APF hesaplaması collision_avoidance node'unda yapılır.
  Bu script sadece hedef konumları setpoint_raw'a yazar.

SENARYO 1: Drone1 ↔ Drone3 karşı karşıya uçuş (Y ekseni)
SENARYO 2: 3 drone aynı noktaya

KULLANIM:
  # Terminal 1: Launch (Gazebo + SITL + MAVROS + pipeline node'ları)
  ros2 launch my_swarm_pkg swarm_competition.launch.py

  # Terminal 2: Test
  python3 ~/gz_ws/src/my_swarm_pkg/scripts/test_collision_avoidance.py
"""

import math, time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, StreamRate
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from swarm_msgs.msg import LocalState

HOVER_ALT = 10.0

BEST_EFFORT = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST, depth=10)


class CollisionTest(Node):
    def __init__(self):
        super().__init__('collision_test')
        self.poses = {}
        self.states = {}
        self.hedefler = {}
        self.pubs_raw = {}       # pipeline'a setpoint_raw
        self.pubs_state = {}     # LocalState FLYING yayını
        self.yayinla_aktif = False
        self.min_mesafe = 999.0
        self._state_seq = 0

        for i in range(1, 4):
            ns = f'drone{i}'
            # Pipeline'a setpoint_raw gönder → collision_avoidance işleyecek
            self.pubs_raw[i] = self.create_publisher(
                PoseStamped, f'/{ns}/setpoint_raw', 10)
            # LocalState FLYING yayını — collision_avoidance komşu olarak tanısın
            self.pubs_state[i] = self.create_publisher(
                LocalState, f'/{ns}/local_state', 10)
            self.create_subscription(
                State, f'/{ns}/mavros/state',
                lambda m, i=i: self.states.update({i: m}), BEST_EFFORT)
            # drone_interface global frame'de yayınlar (HOME offset ekli)
            self.create_subscription(
                PoseStamped, f'/{ns}/pose',
                lambda m, i=i: self._pose_cb(i, m), BEST_EFFORT)

        self.create_timer(0.05, self._yayinla)       # 20Hz setpoint_raw
        self.create_timer(0.1, self._yayinla_state)   # 10Hz LocalState

    def _pose_cb(self, drone_id, msg):
        self.poses[drone_id] = msg
        if len(self.poses) >= 2 and self.yayinla_aktif:
            for a in self.poses:
                for b in self.poses:
                    if a >= b:
                        continue
                    pa = self.poses[a].pose.position
                    pb = self.poses[b].pose.position
                    dist = math.sqrt(
                        (pa.x-pb.x)**2 + (pa.y-pb.y)**2 + (pa.z-pb.z)**2)
                    if dist < self.min_mesafe:
                        self.min_mesafe = dist
                        if dist < 5.0:
                            self.get_logger().warn(
                                f'  !! MIN MESAFE: drone{a}<->drone{b} = {dist:.2f}m !!')

    def _yayinla_state(self):
        """Tüm dronelar için FLYING state yayınla — collision_avoidance komşuları tanısın."""
        self._state_seq += 1
        for i in range(1, 4):
            msg = LocalState()
            msg.drone_id = i
            msg.state = 'FLYING'
            self.pubs_state[i].publish(msg)

    def _yayinla(self):
        """Hedefleri setpoint_raw olarak yayınla — collision_avoidance APF uygulayacak."""
        if not self.yayinla_aktif:
            return
        for i in range(1, 4):
            if i not in self.hedefler:
                continue

            tx, ty, tz = self.hedefler[i]

            msg = PoseStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'map'
            msg.pose.position.x = float(tx)
            msg.pose.position.y = float(ty)
            msg.pose.position.z = float(tz)
            msg.pose.orientation.w = 1.0
            self.pubs_raw[i].publish(msg)

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

    def _mesafe_goster(self):
        for a in range(1, 4):
            for b in range(a+1, 4):
                if a in self.poses and b in self.poses:
                    pa = self.poses[a].pose.position
                    pb = self.poses[b].pose.position
                    dist = math.sqrt(
                        (pa.x-pb.x)**2 + (pa.y-pb.y)**2 + (pa.z-pb.z)**2)
                    self.get_logger().info(f'    drone{a}<->drone{b}: {dist:.2f}m')

    def calistir(self):
        # Stream rate
        self.get_logger().info('=== STREAM RATE ===')
        for i in range(1, 4):
            req = StreamRate.Request()
            req.stream_id = 0
            req.message_rate = 10
            req.on_off = True
            self._servis(StreamRate, f'/drone{i}/mavros/set_stream_rate', req)

        # Pozisyon oku
        self.get_logger().info('=== POZISYON OKUMA (15sn) ===')
        self._spin_sure(15.0)
        for i in range(1, 4):
            p = self.poses.get(i)
            if p:
                self.get_logger().info(
                    f'  drone{i}: x={p.pose.position.x:.2f} '
                    f'y={p.pose.position.y:.2f} z={p.pose.position.z:.2f}')

        # ARM + GUIDED + TAKEOFF
        self.get_logger().info('\n=== ARM + GUIDED + TAKEOFF ===')
        for i in range(1, 4):
            req = SetMode.Request(); req.custom_mode = 'GUIDED'
            self._servis(SetMode, f'/drone{i}/mavros/set_mode', req)
        self._spin_sure(0.5)
        for i in range(1, 4):
            req = CommandBool.Request(); req.value = True
            self._servis(CommandBool, f'/drone{i}/mavros/cmd/arming', req)
        self._spin_sure(0.5)
        for i in range(1, 4):
            req = CommandTOL.Request(); req.altitude = HOVER_ALT
            self._servis(CommandTOL, f'/drone{i}/mavros/cmd/takeoff', req)
        self.get_logger().info(f'  TAKEOFF {HOVER_ALT}m')

        # Kalkış bekle
        self.get_logger().info('\n=== KALKIS BEKLENIYOR (25sn) ===')
        self._spin_sure(25.0)

        # Mevcut pozisyonlar
        pos = {}
        for i in range(1, 4):
            p = self.poses.get(i)
            if p:
                pos[i] = (p.pose.position.x, p.pose.position.y)
                self.get_logger().info(
                    f'  drone{i}: ({pos[i][0]:.1f}, {pos[i][1]:.1f}, z={p.pose.position.z:.1f})')
        self._mesafe_goster()

        # Yerinde tut — pipeline üzerinden
        for i in range(1, 4):
            if i in pos:
                self.hedefler[i] = (pos[i][0], pos[i][1], HOVER_ALT)
        self.yayinla_aktif = True
        self._spin_sure(3.0)

        # ═══════════════════════════════════════════════════════════
        # SENARYO: DRONE1 ↔ DRONE3 — TAM KAFA KAFAYA
        # ═══════════════════════════════════════════════════════════
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('  DRONE1 ↔ DRONE3: KAFA KAFAYA CARPISMA TESTİ')
        self.get_logger().info('  Drone1 → Drone3 pozisyonuna')
        self.get_logger().info('  Drone3 → Drone1 pozisyonuna')
        self.get_logger().info('  Drone2 → yerinde bekliyor')
        self.get_logger().info('='*60)

        self.min_mesafe = 999.0

        # Drone1 ve Drone3 yer degistirsin (birbirinin pozisyonuna)
        self.hedefler[1] = (pos[3][0], pos[3][1], HOVER_ALT)
        self.hedefler[3] = (pos[1][0], pos[1][1], HOVER_ALT)
        # drone2 yerinde kalsin

        self.get_logger().info(f'  Drone1 simdi: ({pos[1][0]:.1f},{pos[1][1]:.1f}) → hedef: ({pos[3][0]:.1f},{pos[3][1]:.1f})')
        self.get_logger().info(f'  Drone3 simdi: ({pos[3][0]:.1f},{pos[3][1]:.1f}) → hedef: ({pos[1][0]:.1f},{pos[1][1]:.1f})')
        self.get_logger().info('')

        for t in range(20):
            self._spin_sure(2.0)
            # Drone1-Drone3 mesafesini ozel goster
            if 1 in self.poses and 3 in self.poses:
                pa = self.poses[1].pose.position
                pb = self.poses[3].pose.position
                dist_13 = math.sqrt(
                    (pa.x-pb.x)**2 + (pa.y-pb.y)**2 + (pa.z-pb.z)**2)
                self.get_logger().info(
                    f'  t={t*2+2:2d}sn | D1↔D3: {dist_13:.2f}m | '
                    f'D1: ({pa.x:.1f},{pa.y:.1f}) D3: ({pb.x:.1f},{pb.y:.1f}) | '
                    f'MIN: {self.min_mesafe:.2f}m')

        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info(f'  SENARYO 1 SONUC — Min mesafe: {self.min_mesafe:.2f}m')
        if self.min_mesafe > 2.0:
            self.get_logger().info('  ✓ CARPISMA ONLENDI!')
        elif self.min_mesafe > 1.0:
            self.get_logger().info('  △ YAKIN GECIS!')
        else:
            self.get_logger().info('  ✗ CARPISMA!')
        self.get_logger().info('='*60)

        # Guncelle pozisyonlari
        for i in range(1, 4):
            p = self.poses.get(i)
            if p:
                pos[i] = (p.pose.position.x, p.pose.position.y)

        # ═══════════════════════════════════════════════════════════
        # SENARYO 2: CAPRAZ GECIS
        # Drone1 → sağa (x+15), Drone3 → sola (x-15)
        # Yolları ortada kesişiyor
        # ═══════════════════════════════════════════════════════════
        self.get_logger().info('\n' + '='*60)
        self.get_logger().info('  SENARYO 2: CAPRAZ GECIS')
        self.get_logger().info('  Drone1 → saga (x+15)')
        self.get_logger().info('  Drone3 → sola (x-15)')
        self.get_logger().info('  Drone2 → yerinde bekliyor')
        self.get_logger().info('='*60)

        self.min_mesafe = 999.0

        self.hedefler[1] = (pos[1][0] + 15.0, pos[3][1], HOVER_ALT)
        self.hedefler[3] = (pos[3][0] - 15.0, pos[1][1], HOVER_ALT)

        self.get_logger().info(f'  Drone1: ({pos[1][0]:.1f},{pos[1][1]:.1f}) → ({self.hedefler[1][0]:.1f},{self.hedefler[1][1]:.1f})')
        self.get_logger().info(f'  Drone3: ({pos[3][0]:.1f},{pos[3][1]:.1f}) → ({self.hedefler[3][0]:.1f},{self.hedefler[3][1]:.1f})')
        self.get_logger().info('')

        for t in range(15):
            self._spin_sure(2.0)
            self._mesafe_goster()

        self.get_logger().info('')
        self.get_logger().info('='*60)
        self.get_logger().info(f'  SENARYO 2 SONUC — Min mesafe: {self.min_mesafe:.2f}m')
        if self.min_mesafe > 2.0:
            self.get_logger().info('  ✓ CARPISMA ONLENDI!')
        elif self.min_mesafe > 1.0:
            self.get_logger().info('  △ YAKIN GECIS!')
        else:
            self.get_logger().info('  ✗ CARPISMA!')
        self.get_logger().info('='*60)

        self.get_logger().info('\n=== TEST TAMAMLANDI ===')


def main():
    rclpy.init()
    node = CollisionTest()
    try:
        node.calistir()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
