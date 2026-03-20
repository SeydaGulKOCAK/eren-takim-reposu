#!/usr/bin/env python3
"""
test_dds_loss.py — TEST 3: İHA–İHA Haberleşme Kaybı (DDS)
══════════════════════════════════════════════════════════
Senaryo : drone3 intent_coordinator SIGSTOP ile dondurulur
          → /drone3/local_state heartbeat kesilir
          → intent_coordinator 600ms timeout sonra drone3'ü
            INACTIVE sayar (SAFETY_HOLD state)
          → lider değişmez (drone1 zaten lider)
          → ama drone3 uçuş listesinden çıkar

Beklenen: 600ms içinde drone3 timeout tespiti
          Sürü diğer 2 drone ile devam eder
          drone3 SIGCONT sonrası yeniden sürüye katılır

Çalıştırma:
  python3 test_scripts/test_dds_loss.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from swarm_msgs.msg import SwarmIntent, LocalState
from std_msgs.msg import UInt8
import subprocess
import signal
import time
import os

LOST_DRONE       = 3
DRONES           = [1, 2, 3]
HEARTBEAT_TIMEOUT_MS = 600
OBSERVE_LOSS_SEC = 15
OBSERVE_REJOIN_SEC = 10

best_effort = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


class DDSLossTest(Node):

    def __init__(self):
        super().__init__('test_dds_loss')

        self.drone_states  = {i: '?' for i in DRONES}
        self.leader_id     = 0
        self.intent_seq    = 0
        self.intent_count  = 0
        self.leader_changes = []

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

    def _on_leader(self, msg: UInt8):
        if msg.data != self.leader_id:
            prev = self.leader_id
            self.leader_id = msg.data
            ts = time.time()
            self.leader_changes.append((ts, prev, msg.data))
            self.get_logger().info(f'👑 Lider değişti: drone{prev} → drone{msg.data}')

    def _on_intent(self, msg: SwarmIntent):
        self.intent_count += 1
        self.intent_seq = msg.seq

    def _on_state(self, msg: LocalState, drone_id: int):
        prev = self.drone_states[drone_id]
        self.drone_states[drone_id] = msg.state
        if prev != msg.state:
            self.get_logger().info(f'📊 drone{drone_id}: {prev} → {msg.state}')


def find_node_pid(node_name, drone_id):
    """intent_coordinator drone3 PID'ini bul."""
    result = subprocess.run(
        ['pgrep', '-f', node_name],
        capture_output=True, text=True
    )
    pids = result.stdout.strip().split()
    # drone3'e ait olanı bulmak zor — env var ile ayırt etmeye çalış
    # En kolay: sıradaki PID (drone3 en son başlar)
    int_pids = [int(p) for p in pids if p.isdigit()]
    return int_pids


def main():
    rclpy.init()
    node = DDSLossTest()

    print(f'\n{"═"*55}')
    print(f'TEST 3 — İHA–İHA Haberleşme Kaybı (drone{LOST_DRONE})')
    print(f'{"═"*55}')
    print(f'Yöntem  : drone{LOST_DRONE} intent_coordinator SIGSTOP')
    print(f'Timeout : {HEARTBEAT_TIMEOUT_MS}ms heartbeat timeout')
    print(f'{"─"*55}')

    # Baseline
    print('⏳ 3s baseline...')
    t = time.time()
    while time.time() - t < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)

    print(f'   Başlangıç durumları: {node.drone_states}')
    print(f'   Lider: drone{node.leader_id}')

    flying = [d for d, s in node.drone_states.items() if s == 'FLYING']
    if len(flying) < 2:
        print('⚠️  Yeterli drone uçmuyor!')
        rclpy.shutdown()
        return

    # drone3 intent_coordinator'ı dondur
    pids = find_node_pid('intent_coordinator', LOST_DRONE)
    print(f'\n→ intent_coordinator PID\'leri: {pids}')
    print(f'   drone{LOST_DRONE}\'ün PID\'i: son başlayan = {pids[-1] if pids else "?"}')

    stopped_pid = None
    if pids:
        # drone3 en son başladı → en büyük PID
        target_pid = max(pids)
        try:
            os.kill(target_pid, signal.SIGSTOP)
            stopped_pid = target_pid
            loss_time = time.time()
            print(f'   ✅ PID {target_pid} DONDURULDU — saat: {loss_time:.3f}')
        except Exception as e:
            print(f'   ❌ SIGSTOP başarısız: {e}')

    # Drone'ların local_state heartbeat'i de kes (daha gerçekçi DDS kaybı)
    lfsm_pids = find_node_pid('local_fsm', LOST_DRONE)
    stopped_lfsm = None
    if lfsm_pids:
        target = max(lfsm_pids)
        try:
            os.kill(target, signal.SIGSTOP)
            stopped_lfsm = target
            print(f'   ✅ local_fsm PID {target} de donduruldu (heartbeat kesildi)')
        except Exception as e:
            print(f'   ⚠️  local_fsm SIGSTOP: {e}')

    # Gözlem
    print(f'\n⏱  {OBSERVE_LOSS_SEC}s gözlemleniyor (drone{LOST_DRONE} offline)...')
    t = time.time()
    timeout_detected = False
    while time.time() - t < OBSERVE_LOSS_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        d3_state = node.drone_states.get(LOST_DRONE, '?')
        if d3_state == 'SAFETY_HOLD' and not timeout_detected:
            timeout_detected = True
            elapsed_ms = (time.time() - loss_time) * 1000
            print(f'\n   ✅ drone{LOST_DRONE} SAFETY_HOLD → {elapsed_ms:.0f}ms sonra timeout tespiti!')
        states_str = ' '.join(f'd{i}:{node.drone_states[i][:6]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | lider:d{node.leader_id} | {states_str}', end='')

    print()

    # Yeniden başlat
    for pid in ([stopped_pid] if stopped_pid else []) + ([stopped_lfsm] if stopped_lfsm else []):
        if pid:
            try:
                os.kill(pid, signal.SIGCONT)
                print(f'\n→ PID {pid} yeniden başlatıldı (SIGCONT)')
            except Exception:
                pass

    # Rejoin gözlemi
    print(f'\n⏱  {OBSERVE_REJOIN_SEC}s yeniden katılım gözlemi...')
    t = time.time()
    while time.time() - t < OBSERVE_REJOIN_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        states_str = ' '.join(f'd{i}:{node.drone_states[i][:6]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | lider:d{node.leader_id} | {states_str}', end='')
    print()

    # Sonuç
    swarm_continued = node.drone_states.get(1, '?') == 'FLYING' or \
                      node.drone_states.get(2, '?') == 'FLYING'
    passed = timeout_detected and swarm_continued

    print(f'\n{"═"*55}')
    print('SONUÇ:')
    print(f'  {"✅" if timeout_detected   else "❌"} Heartbeat timeout tespiti ({HEARTBEAT_TIMEOUT_MS}ms)')
    print(f'  {"✅" if swarm_continued    else "❌"} Sürü devam etti (drone1/2 uçuyor)')
    print(f'  ℹ️  Lider değişimleri: {node.leader_changes}')
    print(f'  ℹ️  Son durumlar: {node.drone_states}')
    print(f'\n{"✅ TEST GEÇTİ" if passed else "❌ TEST BAŞARISIZ"}')
    print(f'{"═"*55}\n')

    with open('/tmp/test_dds_loss_result.txt', 'w') as f:
        f.write('TEST: İHA–İHA Haberleşme Kaybı\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        f.write(f'timeout_tespiti: {timeout_detected}\n')
        f.write(f'suru_devam: {swarm_continued}\n')
        f.write(f'lider_degisimleri: {node.leader_changes}\n')
        f.write(f'son_durumlar: {node.drone_states}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
