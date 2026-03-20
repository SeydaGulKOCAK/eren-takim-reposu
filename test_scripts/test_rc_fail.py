#!/usr/bin/env python3
"""
test_rc_fail.py — TEST 1: RC Kumanda Sinyali Kaybı
══════════════════════════════════════════════════
Senaryo : SIM_RC_FAIL=1 → Pixhawk RC loss algılar
Beklenen: drone1 non-AUTONOMOUS moda geçer →
          drone_interface pilot_override=True yayınlar →
          local_fsm PILOT_OVERRIDE durumuna girer →
          ArduPilot RTL moduna geçer

Çalıştırma:
  source ~/eren-takim-reposu/install/setup.bash
  python3 test_scripts/test_rc_fail.py

Ön koşul: 3 drone uçuyor olmalı ([s] ile kalkış yapılmış)
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from mavros_msgs.msg import State
from mavros_msgs.srv import ParamSetV2
from rcl_interfaces.msg import ParameterValue
from std_msgs.msg import Bool
from swarm_msgs.msg import LocalState
import time
import sys

DRONE_NS   = 'drone1'
MAVROS_NS  = f'/{DRONE_NS}/mavros'
TEST_NAME  = 'RC Kumanda Kaybı'
RC_FAIL_PARAM = 'SIM_RC_FAIL'
OBSERVE_SEC   = 15  # gözlem süresi


class RCFailTest(Node):

    def __init__(self):
        super().__init__('test_rc_fail')
        self.result = {}

        best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        # drone_interface'den gelen pilot_override sinyali
        self.create_subscription(
            Bool, f'/{DRONE_NS}/pilot_override',
            self._on_override, 10
        )

        # local_fsm'den gelen durum
        self.create_subscription(
            LocalState, f'/{DRONE_NS}/local_state',
            self._on_local_state, best_effort
        )

        # MAVROS'tan Pixhawk modu
        self.create_subscription(
            State, f'{MAVROS_NS}/state',
            self._on_mavros_state, 10
        )

        # MAVROS param servisi
        self.param_cli = self.create_client(
            ParamSetV2, f'{MAVROS_NS}/param/set'
        )

        self.override_received  = False
        self.rtl_mode_confirmed = False
        self.fsm_state          = '?'
        self.mavros_mode        = '?'

    def _on_override(self, msg: Bool):
        if msg.data and not self.override_received:
            self.override_received = True
            self.get_logger().info(f'✅ pilot_override=True alındı!')
            self.result['pilot_override'] = True

    def _on_local_state(self, msg: LocalState):
        self.fsm_state = msg.state
        if msg.state in ('PILOT_OVERRIDE', 'SAFETY_HOLD'):
            self.get_logger().info(f'✅ local_fsm durumu: {msg.state}')
            self.result['fsm_state'] = msg.state

    def _on_mavros_state(self, msg: State):
        if msg.mode != self.mavros_mode:
            self.mavros_mode = msg.mode
            self.get_logger().info(f'🔄 Pixhawk modu: {msg.mode}')
            self.result['pixhawk_mode'] = msg.mode
            if msg.mode == 'RTL':
                self.rtl_mode_confirmed = True
                self.get_logger().info(f'✅ RTL modu onaylandı!')

    def set_param(self, val: int):
        if not self.param_cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('❌ MAVROS param servisi hazır değil!')
            return False
        req = ParamSetV2.Request()
        req.param_id = RC_FAIL_PARAM
        req.value = ParameterValue(type=2, integer_value=val)
        future = self.param_cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        try:
            res = future.result()
            return res.success
        except Exception as e:
            self.get_logger().error(f'Param set hatası: {e}')
            return False


def main():
    rclpy.init()
    node = RCFailTest()

    print(f'\n{"═"*55}')
    print(f'TEST 1 — {TEST_NAME}')
    print(f'{"═"*55}')
    print(f'Drone    : {DRONE_NS}')
    print(f'Parametre: {RC_FAIL_PARAM}=1')
    print(f'Süre     : {OBSERVE_SEC}s gözlem')
    print(f'{"─"*55}')

    # 2s dinle (baseline)
    print('⏳ Başlangıç durumu okunuyor...')
    t = time.time()
    while time.time() - t < 2.0:
        rclpy.spin_once(node, timeout_sec=0.1)

    print(f'   Başlangıç FSM   : {node.fsm_state}')
    print(f'   Başlangıç Modu  : {node.mavros_mode}')

    if node.fsm_state not in ('FLYING', 'IDLE'):
        print(f'⚠️  Drone uçmuyor (state={node.fsm_state}). Önce kalkış yap!')
        rclpy.shutdown()
        sys.exit(1)

    # RC_FAIL tetikle
    print(f'\n→ {RC_FAIL_PARAM}=1 gönderiliyor...')
    ok = node.set_param(1)
    print(f'   Param set: {"✅ OK" if ok else "⚠️ Servis yanıt vermedi (MAVROS param bölümü aktif olmayabilir)"}')

    # Gözlem
    print(f'\n⏱  {OBSERVE_SEC}s gözlemleniyor...')
    t = time.time()
    while time.time() - t < OBSERVE_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        print(f'\r   {elapsed:5.1f}s | FSM: {node.fsm_state:20s} | Pixhawk: {node.mavros_mode:15s}', end='')

    print()

    # Sıfırla
    print(f'\n→ {RC_FAIL_PARAM}=0 (sıfırlanıyor)...')
    node.set_param(0)

    # Sonuç
    print(f'\n{"═"*55}')
    print('SONUÇ:')
    passed = node.override_received or node.rtl_mode_confirmed or \
             node.result.get('fsm_state') in ('PILOT_OVERRIDE', 'SAFETY_HOLD')
    items = [
        ('pilot_override=True alındı', node.override_received),
        ('Pixhawk RTL modu',           node.rtl_mode_confirmed),
        ('FSM PILOT_OVERRIDE/SAFETY',  node.result.get('fsm_state') in ('PILOT_OVERRIDE','SAFETY_HOLD')),
        ('Son Pixhawk modu',           node.mavros_mode),
        ('Son FSM durumu',             node.fsm_state),
    ]
    for label, val in items:
        if isinstance(val, bool):
            print(f'  {"✅" if val else "❌"} {label}')
        else:
            print(f'  ℹ️  {label}: {val}')
    print(f'\n{"✅ TEST GEÇTİ" if passed else "❌ TEST BAŞARISIZ"}')
    print(f'{"═"*55}\n')

    # Log dosyasına yaz
    with open('/tmp/test_rc_fail_result.txt', 'w') as f:
        f.write(f'TEST: {TEST_NAME}\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        for k, v in node.result.items():
            f.write(f'  {k}: {v}\n')
        f.write(f'son_fsm: {node.fsm_state}\n')
        f.write(f'son_pixhawk_modu: {node.mavros_mode}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
