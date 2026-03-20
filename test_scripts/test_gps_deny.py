#!/usr/bin/env python3
"""
test_gps_deny.py — TEST 5: GPS Sinyal Kaybı (GPS-Denied)
══════════════════════════════════════════════════════════
Senaryo : SIM_GPS_DISABLE=1 → Pixhawk GPS verisi kesilir
          uwb_mock.py çalışıyorsa: vision_pose aktif → hover sürer
          uwb_mock.py yoksa     : EKF konumsuz → position hold bozulur

Beklenen: GPS kapalıyken drone hover modunda kalır
          (ArduPilot EK3_SRC1_POSXY=6 ile UWB/ExtNav kullanılır)

NOT: Bu test uwb_mock.py ile birlikte çalıştırılmalıdır:
  Terminal 1: python3 test_scripts/uwb_mock.py
  Terminal 2: python3 test_scripts/test_gps_deny.py

Çalıştırma:
  python3 test_scripts/test_gps_deny.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import ParamSetV2
from rcl_interfaces.msg import ParameterValue
from swarm_msgs.msg import LocalState
import time
import math

TEST_DRONE  = 1
MAVROS_NS   = f'/drone{TEST_DRONE}/mavros'
DRONES      = [1, 2, 3]
OBSERVE_SEC = 20
GPS_PARAM   = 'SIM_GPS_DISABLE'
MAX_DRIFT_M = 2.0  # GPS kapalıyken izin verilen maksimum drift

best_effort = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


class GPSDenyTest(Node):

    def __init__(self):
        super().__init__('test_gps_deny')

        self.poses   = {i: None for i in DRONES}
        self.modes   = {i: '?'  for i in DRONES}
        self.states  = {i: '?'  for i in DRONES}
        self.ref_pos = None  # GPS kesildiğindeki referans konum

        for i in DRONES:
            self.create_subscription(
                PoseStamped, f'/drone{i}/pose',
                lambda msg, di=i: self._on_pose(msg, di),
                best_effort
            )
            self.create_subscription(
                State, f'/drone{i}/mavros/state',
                lambda msg, di=i: self._on_mode(msg, di),
                10
            )
            self.create_subscription(
                LocalState, f'/drone{i}/local_state',
                lambda msg, di=i: self._on_state(msg, di),
                best_effort
            )

        self.param_cli = self.create_client(
            ParamSetV2, f'{MAVROS_NS}/param/set'
        )

    def _on_pose(self, msg: PoseStamped, drone_id: int):
        self.poses[drone_id] = msg.pose.position

    def _on_mode(self, msg: State, drone_id: int):
        self.modes[drone_id] = msg.mode

    def _on_state(self, msg: LocalState, drone_id: int):
        self.states[drone_id] = msg.state

    def drift_from_ref(self) -> float:
        p = self.poses.get(TEST_DRONE)
        r = self.ref_pos
        if p is None or r is None:
            return 0.0
        return math.sqrt((p.x - r.x)**2 + (p.y - r.y)**2 + (p.z - r.z)**2)

    def set_gps(self, val: int):
        if not self.param_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn('MAVROS param servisi yok')
            return False
        req = ParamSetV2.Request()
        req.param_id = GPS_PARAM
        req.value = ParameterValue(type=2, integer_value=val)
        future = self.param_cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        try:
            return future.result().success
        except Exception:
            return False


def main():
    rclpy.init()
    node = GPSDenyTest()

    print(f'\n{"═"*55}')
    print('TEST 5 — GPS Sinyal Kaybı (GPS-Denied)')
    print(f'{"═"*55}')
    print('NOT: uwb_mock.py ayrı terminalde çalışmalı!')
    print(f'{"─"*55}')

    # Baseline
    print('⏳ 3s baseline...')
    t = time.time()
    while time.time() - t < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)

    p = node.poses.get(TEST_DRONE)
    print(f'   Konum  : {f"({p.x:.1f},{p.y:.1f},{p.z:.1f})" if p else "yok!"}')
    print(f'   Durum  : {node.states.get(TEST_DRONE)}')
    print(f'   Mod    : {node.modes.get(TEST_DRONE)}')

    if node.states.get(TEST_DRONE) != 'FLYING':
        print('⚠️  Drone uçmuyor!')
        rclpy.shutdown()
        return

    if node.poses.get(TEST_DRONE) is None:
        print('⚠️  Konum verisi yok! drone_interface çalışıyor mu?')
        rclpy.shutdown()
        return

    # GPS kes
    print(f'\n→ {GPS_PARAM}=1 (GPS kapatılıyor)...')
    ok = node.set_gps(1)
    print(f'   Param set: {"✅ OK" if ok else "⚠️ Servis yok"}')
    node.ref_pos = node.poses.get(TEST_DRONE)
    gps_off_time = time.time()
    print(f'   Referans konum: ({node.ref_pos.x:.2f}, {node.ref_pos.y:.2f}, {node.ref_pos.z:.2f})')

    # Gözlem
    print(f'\n⏱  {OBSERVE_SEC}s gözlemleniyor (GPS kapalı)...')
    max_drift = 0.0
    mode_changes = []
    last_mode = node.modes.get(TEST_DRONE, '?')

    t = time.time()
    while time.time() - t < OBSERVE_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        drift = node.drift_from_ref()
        if drift > max_drift:
            max_drift = drift
        cur_mode = node.modes.get(TEST_DRONE, '?')
        if cur_mode != last_mode:
            mode_changes.append((elapsed, last_mode, cur_mode))
            last_mode = cur_mode
        print(f'\r   {elapsed:5.1f}s | drift: {drift:5.2f}m | mod: {cur_mode:10s} | fsm: {node.states.get(TEST_DRONE):12s}', end='')

    print()

    # GPS aç
    print(f'\n→ {GPS_PARAM}=0 (GPS yeniden açılıyor)...')
    node.set_gps(0)

    # Sonuç
    hover_maintained = max_drift < MAX_DRIFT_M
    mode_stable      = len(mode_changes) == 0 or all(c[2] in ('GUIDED', 'POSHOLD') for c in mode_changes)

    passed = hover_maintained and mode_stable

    print(f'\n{"═"*55}')
    print('SONUÇ:')
    print(f'  {"✅" if hover_maintained else "❌"} Hover sürdü (maks drift: {max_drift:.2f}m < {MAX_DRIFT_M}m)')
    print(f'  {"✅" if mode_stable      else "⚠️"} Mod kararlı kaldı')
    print(f'  ℹ️  Mod değişimleri: {mode_changes}')
    print(f'  ℹ️  Son FSM: {node.states.get(TEST_DRONE)}, Pixhawk: {node.modes.get(TEST_DRONE)}')
    print()
    if not ok:
        print('  ⚠️  NOT: MAVROS param servisi yanıt vermedi.')
        print('         MAVProxy ile: "param set SIM_GPS_DISABLE 1" kullan.')
    print(f'\n{"✅ TEST GEÇTİ" if passed else "❌ TEST BAŞARISIZ"}')
    print(f'{"═"*55}\n')

    with open('/tmp/test_gps_deny_result.txt', 'w') as f:
        f.write('TEST: GPS Sinyal Kaybı\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        f.write(f'maks_drift_m: {max_drift:.3f}\n')
        f.write(f'hover_surdu: {hover_maintained}\n')
        f.write(f'mod_degisimleri: {mode_changes}\n')
        f.write(f'son_fsm: {node.states.get(TEST_DRONE)}\n')
        f.write(f'son_pixhawk: {node.modes.get(TEST_DRONE)}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
