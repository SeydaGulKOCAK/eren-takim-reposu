#!/usr/bin/env python3
"""
test_battery.py — TEST 4: Batarya Kritik Seviye Failsafe
══════════════════════════════════════════════════════════
Senaryo : safety_monitor simülasyon bataryası çok yavaş biter
          (0.01%/s → 8500s gerekir). Bu test SafetyEvent direkt
          yayınlayarak local_fsm tepkisini doğrular.

          2. yöntem: SIM_BATT_VOLTAGE=10V (Pixhawk seviyesi) da test edilir.

Beklenen: SafetyEvent(BATTERY_CRITICAL) →
          local_fsm SAFETY_HOLD → RTL

Çalıştırma:
  python3 test_scripts/test_battery.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from swarm_msgs.msg import LocalState, SafetyEvent
from mavros_msgs.msg import State
from mavros_msgs.srv import ParamSetV2
from rcl_interfaces.msg import ParameterValue
import time

DRONES    = [1, 2, 3]
TEST_DRONE = 1
MAVROS_NS  = f'/drone{TEST_DRONE}/mavros'
OBSERVE_SEC = 10

best_effort = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


class BatteryTest(Node):

    def __init__(self):
        super().__init__('test_battery')

        self.drone_states  = {i: '?' for i in DRONES}
        self.mavros_modes  = {i: '?' for i in DRONES}
        self.safety_event_received = False
        self.rtl_triggered = False

        # SafetyEvent publisher (safety_monitor yerine biz tetikleyeceğiz)
        self.safety_pub = self.create_publisher(
            SafetyEvent, '/safety/event', 10
        )

        # Sonuç dinleyiciler
        for i in DRONES:
            self.create_subscription(
                LocalState, f'/drone{i}/local_state',
                lambda msg, di=i: self._on_state(msg, di),
                best_effort
            )
            self.create_subscription(
                State, f'/drone{i}/mavros/state',
                lambda msg, di=i: self._on_mavros(msg, di),
                10
            )

        self.create_subscription(
            SafetyEvent, '/safety/event',
            self._on_safety_event, 10
        )

        # MAVROS param servisi (Pixhawk batarya simülasyonu)
        self.param_cli = self.create_client(
            ParamSetV2, f'{MAVROS_NS}/param/set'
        )

    def _on_state(self, msg: LocalState, drone_id: int):
        prev = self.drone_states[drone_id]
        self.drone_states[drone_id] = msg.state
        if prev != msg.state:
            self.get_logger().info(f'📊 drone{drone_id}: {prev} → {msg.state}')
            if msg.state == 'SAFETY_HOLD':
                self.get_logger().info(f'✅ drone{drone_id} SAFETY_HOLD!')

    def _on_mavros(self, msg: State, drone_id: int):
        prev = self.mavros_modes[drone_id]
        self.mavros_modes[drone_id] = msg.mode
        if prev != msg.mode:
            self.get_logger().info(f'🔄 drone{drone_id} Pixhawk: {prev} → {msg.mode}')
            if msg.mode == 'RTL':
                self.rtl_triggered = True

    def _on_safety_event(self, msg: SafetyEvent):
        if not self.safety_event_received:
            self.safety_event_received = True
            self.get_logger().info(f'✅ SafetyEvent alındı: type={msg.event_type} drone_id={msg.drone_id}')

    def send_battery_critical(self, drone_id: int):
        msg = SafetyEvent()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.event_type  = 'BATTERY_CRITICAL'
        msg.drone_id    = drone_id
        msg.severity    = 1.0
        msg.description = f'Test: simulated battery critical (drone{drone_id})'
        self.safety_pub.publish(msg)

    def set_sim_batt(self, voltage: float):
        if not self.param_cli.wait_for_service(timeout_sec=3.0):
            return False
        req = ParamSetV2.Request()
        req.param_id = 'SIM_BATT_VOLTAGE'
        req.value = ParameterValue(type=3, double_value=voltage)
        future = self.param_cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        try:
            return future.result().success
        except Exception:
            return False


def main():
    rclpy.init()
    node = BatteryTest()

    print(f'\n{"═"*55}')
    print('TEST 4 — Batarya Kritik Seviye Failsafe')
    print(f'{"═"*55}')
    print('Yöntem A: SafetyEvent direkt yayınla → local_fsm tepkisi')
    print('Yöntem B: SIM_BATT_VOLTAGE=10V → Pixhawk batarya uyarısı')
    print(f'{"─"*55}')

    # Baseline
    print('⏳ 3s baseline...')
    t = time.time()
    while time.time() - t < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)
    print(f'   Başlangıç: {node.drone_states}')

    flying = [d for d, s in node.drone_states.items() if s == 'FLYING']
    if not flying:
        print('⚠️  Drone uçmuyor!')
        rclpy.shutdown()
        return

    # ── YÖNTEM A: SafetyEvent direkt ──────────────────────────
    print(f'\n[YÖNTEM A] SafetyEvent → BATTERY_CRITICAL → drone{TEST_DRONE}')
    node.send_battery_critical(TEST_DRONE)
    print(f'   SafetyEvent gönderildi → {OBSERVE_SEC}s gözlemleniyor...')

    t = time.time()
    while time.time() - t < OBSERVE_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        states_str = ' '.join(f'd{i}:{node.drone_states[i][:8]}' for i in DRONES)
        modes_str  = ' '.join(f'd{i}:{node.mavros_modes[i][:6]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | FSM: {states_str} | Pix: {modes_str}', end='')
    print()

    yontem_a_ok = (
        node.safety_event_received and
        node.drone_states.get(TEST_DRONE) == 'SAFETY_HOLD'
    )

    # ── YÖNTEM B: SIM_BATT_VOLTAGE (Pixhawk seviyesi) ──────────
    print(f'\n[YÖNTEM B] SIM_BATT_VOLTAGE=10.0V → drone{TEST_DRONE}')
    ok = node.set_sim_batt(10.0)
    print(f'   Param set: {"✅ OK" if ok else "⚠️ Servis yok (MAVROS param aktif olmayabilir)"}')

    t = time.time()
    while time.time() - t < OBSERVE_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        print(f'\r   {elapsed:5.1f}s | Pixhawk modu: {node.mavros_modes.get(TEST_DRONE, "?")}    ', end='')
    print()

    # Sıfırla
    node.set_sim_batt(12.6)
    print('   Batarya sıfırlandı (12.6V)')

    # Sonuç
    passed = yontem_a_ok
    print(f'\n{"═"*55}')
    print('SONUÇ:')
    print(f'  {"✅" if node.safety_event_received    else "❌"} SafetyEvent alındı')
    print(f'  {"✅" if node.drone_states.get(TEST_DRONE)=="SAFETY_HOLD" else "❌"} SAFETY_HOLD durumu')
    print(f'  {"✅" if node.rtl_triggered             else "ℹ️"} RTL modu (opsiyonel)')
    print(f'  ℹ️  Son FSM durumları: {node.drone_states}')
    print(f'\n{"✅ TEST GEÇTİ" if passed else "❌ TEST BAŞARISIZ"}')
    print(f'{"═"*55}\n')

    with open('/tmp/test_battery_result.txt', 'w') as f:
        f.write('TEST: Batarya Kritik Seviye\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        f.write(f'safety_event_alindi: {node.safety_event_received}\n')
        f.write(f'safety_hold: {node.drone_states.get(TEST_DRONE)}\n')
        f.write(f'rtl_tetiklendi: {node.rtl_triggered}\n')
        f.write(f'son_durumlar: {node.drone_states}\n')
        f.write(f'son_pixhawk_modlari: {node.mavros_modes}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
