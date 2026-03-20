#!/usr/bin/env python3
"""
test_gcs_loss.py — TEST 2: YKİ (GCS) Bağlantı Kaybı
══════════════════════════════════════════════════════
Senaryo : mission_fsm heartbeat kesilir (process durdurulur)
Beklenen: safety_monitor 3s timeout sonra WARNING loglar
          intent_coordinator yayınlamaya devam eder (GCS'den bağımsız)
          drone'lar otonom uçuşa devam eder → sistem §5.3 dağıtıklık

NOT: Bu test GCS'nin kritik olmadığını kanıtlar.
     intent_coordinator GCS olmadan çalışır.

Çalıştırma:
  python3 test_scripts/test_gcs_loss.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from swarm_msgs.msg import SwarmIntent, LocalState
import subprocess
import signal
import time
import os

OBSERVE_BEFORE_SEC = 5
OBSERVE_AFTER_SEC  = 20
DRONES = [1, 2, 3]

best_effort = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)


class GCSLossTest(Node):

    def __init__(self):
        super().__init__('test_gcs_loss')

        self.intent_count_before = 0
        self.intent_count_after  = 0
        self.phase = 'before'
        self.drone_states = {i: '?' for i in DRONES}
        self.last_intent_ts = None

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

    def _on_intent(self, msg: SwarmIntent):
        self.last_intent_ts = time.time()
        if self.phase == 'before':
            self.intent_count_before += 1
        else:
            self.intent_count_after += 1

    def _on_state(self, msg: LocalState, drone_id: int):
        self.drone_states[drone_id] = msg.state


def find_mission_fsm_pid():
    result = subprocess.run(
        ['pgrep', '-f', 'mission_fsm'],
        capture_output=True, text=True
    )
    pids = result.stdout.strip().split()
    return [int(p) for p in pids if p.isdigit()]


def main():
    rclpy.init()
    node = GCSLossTest()

    print(f'\n{"═"*55}')
    print('TEST 2 — YKİ (GCS) Bağlantı Kaybı')
    print(f'{"═"*55}')

    # Baseline
    print(f'⏳ {OBSERVE_BEFORE_SEC}s baseline ölçümü...')
    t = time.time()
    while time.time() - t < OBSERVE_BEFORE_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)

    print(f'   Baseline intent sayısı : {node.intent_count_before}')
    print(f'   Drone durumları        : {node.drone_states}')
    flying = [d for d, s in node.drone_states.items() if s == 'FLYING']
    if not flying:
        print(f'⚠️  Hiç uçan drone yok! Önce [s] ile kalkış yap.')
        rclpy.shutdown()
        return

    # mission_fsm'i durdur
    pids = find_mission_fsm_pid()
    print(f'\n→ mission_fsm PID(ler): {pids}')
    stopped_pids = []
    for pid in pids:
        try:
            os.kill(pid, signal.SIGSTOP)
            stopped_pids.append(pid)
            print(f'   PID {pid} DURDURULDU (SIGSTOP)')
        except ProcessLookupError:
            print(f'   PID {pid} bulunamadı')

    if not stopped_pids:
        print('⚠️  mission_fsm PID bulunamadı. xterm penceresini manuel kapat.')

    node.phase = 'after'
    print(f'\n⏱  {OBSERVE_AFTER_SEC}s gözlemleniyor (GCS kapalı)...')
    t = time.time()
    last_intent_age = 0.0
    while time.time() - t < OBSERVE_AFTER_SEC:
        rclpy.spin_once(node, timeout_sec=0.1)
        elapsed = time.time() - t
        if node.last_intent_ts:
            last_intent_age = time.time() - node.last_intent_ts
        states_str = ' '.join(f'd{i}:{node.drone_states[i][:4]}' for i in DRONES)
        print(f'\r   {elapsed:5.1f}s | intent/s: {node.intent_count_after/(elapsed+0.01):.1f} | '
              f'son_intent: {last_intent_age:.1f}s önce | {states_str}', end='')

    print()

    # mission_fsm'i yeniden başlat
    for pid in stopped_pids:
        try:
            os.kill(pid, signal.SIGCONT)
            print(f'\n→ PID {pid} yeniden başlatıldı (SIGCONT)')
        except Exception:
            pass

    # Sonuç
    intent_hz_after = node.intent_count_after / OBSERVE_AFTER_SEC
    swarm_continued = intent_hz_after > 1.0  # 2 Hz bekliyoruz, 1 Hz minimum
    still_flying    = all(node.drone_states[i] == 'FLYING' for i in flying)

    print(f'\n{"═"*55}')
    print('SONUÇ:')
    print(f'  {"✅" if swarm_continued else "❌"} Intent yayını devam etti  ({intent_hz_after:.1f} Hz)')
    print(f'  {"✅" if still_flying   else "❌"} Drone\'lar uçmaya devam etti')
    print(f'  ℹ️  GCS kapalıyken intent sayısı: {node.intent_count_after}')
    print(f'  ℹ️  Son drone durumları: {node.drone_states}')

    passed = swarm_continued and still_flying
    result_str = "✅ TEST GEÇTİ — Sistem GCS'siz otonom çalıştı" if passed else "❌ TEST BAŞARISIZ"
    print(f'\n{result_str}')
    print(f'{"═"*55}\n')

    with open('/tmp/test_gcs_loss_result.txt', 'w') as f:
        f.write('TEST: YKİ Bağlantı Kaybı\n')
        f.write(f'SONUÇ: {"GEÇTİ" if passed else "BAŞARISIZ"}\n')
        f.write(f'intent_hz_gcs_kapali: {intent_hz_after:.2f}\n')
        f.write(f'drone_durumlari: {node.drone_states}\n')
        f.write(f'otonom_devam: {swarm_continued}\n')
        f.write(f'ucus_devam: {still_flying}\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
