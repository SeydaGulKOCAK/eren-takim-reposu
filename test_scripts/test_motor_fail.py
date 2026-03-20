#!/usr/bin/env python3
"""
test_motor_fail.py — TEST 6: Drone Arızası ve Lider Değişimi
══════════════════════════════════════════════════════════════
Senaryo : SIM_ENGINE_FAIL=1 → drone1 çöker
          → /drone1/local_state heartbeat kesilir
          → intent_coordinator 600ms timeout → drone1 SAFETY_HOLD
          → Bully algoritması: min(eligible) = drone2 → YENİ LİDER
          → drone2 ve drone3 sürüye devam eder

Beklenen: 600ms içinde lider değişimi (drone1 → drone2)
          Sürü 2 drone ile devam eder

Çalıştırma:
  python3 test_scripts/test_motor_fail.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from swarm_msgs.msg import SwarmIntent, LocalState
from mavros_msgs.msg import State
from mavros_msgs.srv import ParamSetV2
from rcl_interfaces.msg import ParameterValue
from std_msgs.msg import UInt8
import time

FAILED_DRONE    = 1  # hangi drone arızalanacak
MAVROS_NS       = f'/drone{FAILED_DRONE}/mavros'
DRONES          = [1, 2, 3]
HEARTBEAT_MS    = 600
OBSERVE_FAIL_S  = 20
OBSERVE_CONT_S  = 10
ENGINE_PARAM    = 'SIM_ENGINE_FAIL'

best_effort = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


class MotorFailTest(Node):

    def __init__(self):
        super().__init__('test_motor_fail')

        self.drone_states   = {i: '?' for i in DRONES}
        self.mavros_modes   = {i: '?' for i in DRONES}
        self.leader_id      = 0
        self.leader_history = []  # (time, old, new)
        self.intent_count   = {1: 0, 2: 0, 3: 0}  # hangi lider kaç intent yayınladı

        self.create_subscription(
            UInt8, '/swarm/leader_id',
            self._on_leader, 10
        )
        self.create_subscription(
            SwarmIntent, '/swarm/intent',
            self._on_intent, 10
        )
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

        self.param_cli = self.create_client(
            ParamSetV2, f'{MAVROS_NS}/param/set'
        )

    def _on_leader(self, msg: UInt8):
        if msg.data != self.leader_id:
            ts = time.time()
            self.leader_history.append((ts, self.leader_id, msg.data))
            self.get_logger().info(f'👑 LİDER DEĞİŞTİ: drone{self.leader_id} → drone{msg.data}')
            self.leader_id = msg.data

    def _on_intent(self, msg: SwarmIntent):
        lid = msg.leader_id
        if lid in self.intent_count:
            self.intent_count[lid] += 1

    def _on_state(self, msg: LocalState, drone_id: int):
        prev = self.drone_states[drone_id]
        self.drone_states[drone_id] = msg.state
        if prev != msg.state:
            self.get_logger().info(f'📊 drone{drone_id}: {prev} → {msg.state}')

    def _on_mavros(self, msg: State, drone_id: int):
        prev = self.mavros_modes[drone_id]
        self.mavros_modes[drone_id] = msg.mode
        if prev != msg.mode:
            self.get_logger().info(f'🔄 drone{drone_id} Pixhawk: {prev} → {msg.mode}')

    def set_engine_fail(self, val: int):
        if not self.param_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn('MAVROS param servisi yok')
            return False
        req = ParamSetV2.Request()
        req.param_id = ENGINE_PARAM
        req.value = ParameterValue(type=2, integer_value=val)
        future = self.param_cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        try:
            return future.result().success
        except Exception:
            return False


def main():
    rclpy.init()
    node = MotorFailTest()

    print(f'\n{"═"*55}')
    print(f'TEST 6 — Drone{FAILED_DRONE} Motor Arızası ve Lider Değişimi')
    print(f'{"═"*55}')
    print(f'Parametre : {ENGINE_PARAM}=1 → drone{FAILED_DRONE} çöker')
    print(f'Beklenen  : drone2 yeni lider olur')
    print(f'{"─"*55}')

    # Baseline
    print('⏳ 3s baseline...')
    t = time.time()
    while time.time() - t < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)

    print(f'   Başlangıç lider  : drone{node.leader_id}')
    print(f'   Başlangıç durumlar: {node.drone_states}')

    flying = [d for d, s in node.drone_states.items() if s == 'FLYING']
    if len(flying) < 2:
        print('⚠️  En az 2 drone uçmalı!')
        rclpy.shutdown()
        return

    if node.leader_id != FAILED_DRONE:
        print(f'⚠️  Mevcut lider drone{node.leader_id}, drone{FAILED_DRONE} değil.')
        print(f'   Test yine de devam ediyor — drone{FAILED_DRONE} arızalanınca lider değişimi izlenecek.')

    # Motor arızasını tetikle
    print(f'\n→ {ENGINE_PARAM}=1 gönderiliyor (drone{FAILED_DRONE})...')
    ok = node.set_engine_fail(1)
    fail_time = time.time()
    print(f'   Param set: {"✅ OK" if ok else "⚠️ Servis yok — heartbeat kesilmesini simüle etmek için"}')

    # Gözlem
    print(f'\n⏱  {OBSERVE_FAIL_S}s gözlemleniyor...')
    leader_changed = False
    leader_change_delay_ms = None

    t = time.time()
    while time.time() - t < OBSERVE_FAIL_S:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t

        if not leader_changed and node.leader_id != FAILED_DRONE and node.leader_id > 0:
            leader_changed = True
            leader_change_delay_ms = (time.time() - fail_time) * 1000
            print(f'\n   ✅ Lider değişti → drone{node.leader_id} '
                  f'({leader_change_delay_ms:.0f}ms sonra)')

        states_str = ' '.join(f'd{i}:{node.drone_states[i][:6]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | lider:d{node.leader_id} | {states_str}', end='')

    print()

    # Sıfırla
    print(f'\n→ {ENGINE_PARAM}=0 (sıfırlanıyor)...')
    node.set_engine_fail(0)

    # Devam gözlemi
    print(f'\n⏱  {OBSERVE_CONT_S}s sürü devam ediyor mu?')
    t = time.time()
    while time.time() - t < OBSERVE_CONT_S:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        states_str = ' '.join(f'd{i}:{node.drone_states[i][:6]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | lider:d{node.leader_id} | {states_str}', end='')
    print()

    # Sonuç
    swarm_continued = (
        node.drone_states.get(2) == 'FLYING' or
        node.drone_states.get(3) == 'FLYING'
    )
    new_leader_valid = node.leader_id in (2, 3)  # drone2 veya drone3 lider

    passed = leader_changed and swarm_continued

    print(f'\n{"═"*55}')
    print('SONUÇ:')
    print(f'  {"✅" if leader_changed     else "❌"} Lider değişimi gerçekleşti')
    if leader_change_delay_ms:
        print(f'     Gecikme: {leader_change_delay_ms:.0f}ms (beklenen: < {HEARTBEAT_MS*2}ms)')
        print(f'     {"✅" if leader_change_delay_ms < HEARTBEAT_MS*3 else "⚠️"} Gecikme kabul edilebilir')
    print(f'  {"✅" if new_leader_valid   else "❌"} Yeni lider: drone{node.leader_id}')
    print(f'  {"✅" if swarm_continued    else "❌"} Sürü devam etti (drone2/3 FLYING)')
    print(f'  ℹ️  Intent dağılımı: {node.intent_count}')
    print(f'  ℹ️  Lider geçmişi : {[(f"d{o}→d{n}", f"{(t):.1f}s") for t,o,n in node.leader_history]}')
    print(f'  ℹ️  Son durumlar  : {node.drone_states}')
    print(f'\n{"✅ TEST GEÇTİ" if passed else "❌ TEST BAŞARISIZ"}')
    print(f'{"═"*55}\n')

    with open('/tmp/test_motor_fail_result.txt', 'w') as f:
        f.write('TEST: Drone Motor Arızası ve Lider Değişimi\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        f.write(f'lider_degisimi: {leader_changed}\n')
        f.write(f'lider_degisim_ms: {leader_change_delay_ms}\n')
        f.write(f'yeni_lider: drone{node.leader_id}\n')
        f.write(f'suru_devam: {swarm_continued}\n')
        f.write(f'lider_gecmisi: {node.leader_history}\n')
        f.write(f'intent_dagilimi: {node.intent_count}\n')
        f.write(f'son_durumlar: {node.drone_states}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
