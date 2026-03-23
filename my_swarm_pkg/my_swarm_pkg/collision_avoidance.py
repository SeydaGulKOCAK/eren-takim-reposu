#!/usr/bin/env python3
"""
collision_avoidance.py  v3 — ORCA (van den Berg et al., 2011)
RVO2 referans implementasyonundan (github.com/snape/RVO2) birebir port.

ORCA: Hiz uzayinda calisir. Her komsu icin yari-duzlem (half-plane) hesaplar,
LP (Linear Program) ile en yakin guvenli hizi bulur.
Matematiksel carpisma-onleme garantisi verir.

Pipeline (degismedi):
  setpoint_raw -> collision_avoidance (ORCA 50Hz) -> setpoint_final -> drone_interface
"""

import math
import os
import time
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
)
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_msgs.msg import Header
from swarm_msgs.msg import LocalState, SwarmIntent, SafetyEvent

# ============================================================================
# PARAMETRELER
# ============================================================================
AGENT_RADIUS: float = 2.3    # [m] guvenlik yaricapi (combined=4.6m < 5m formasyon)
TAU: float = 8.0              # [s] zaman ufku — 8sn ileriye bak
MAX_SPEED: float = 1.5        # [m/s] max hiz — yavas ve guvenli
LOOKAHEAD: float = 1.5        # [s] setpoint = own_pos + v_safe * LOOKAHEAD
HARD_SAFETY_DIST: float = 4.0 # [m] bu mesafe altinda acil kac
SLOWDOWN_DIST: float = 10.0   # [m] bu mesafe altinda hiz azaltmaya basla

CTRL_HZ: float = 50.0
CTRL_DT: float = 1.0 / CTRL_HZ

OSC_WINDOW: int = 20
OSC_THRESH_M: float = 4.0
OSC_COOLDOWN_S: float = 5.0

SP_STALE_S: float = 0.5
POSE_STALE_S: float = 1.0

SWARM_SIZE: int = int(os.environ.get('SWARM_SIZE', '3'))

RVO_EPSILON: float = 1e-5


# ============================================================================
# 2D VEKTOR YARDIMCILARI
# ============================================================================

def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def _det(a, b):
    """2D cross product (determinant)."""
    return a[0] * b[1] - a[1] * b[0]

def _abs_sq(v):
    return v[0] * v[0] + v[1] * v[1]

def _length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

def _normalize(v):
    l = _length(v)
    if l < RVO_EPSILON:
        return (0.0, 0.0)
    return (v[0] / l, v[1] / l)

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def _scale(v, s):
    return (v[0] * s, v[1] * s)

def _variance(vals):
    if len(vals) < 2:
        return 0.0
    mean = sum(vals) / len(vals)
    return sum((v - mean) ** 2 for v in vals) / len(vals)


# ============================================================================
# ORCA LINE: (point, direction) — direction = cizgi yonu (normal degil!)
# ============================================================================

def _linear_program_1(lines, line_no, radius, opt_velocity, direction_opt):
    """
    RVO2 linearProgram1: lines[line_no] uzerinde, onceki tum cizgileri
    saglayan, opt_velocity'ye en yakin noktayi bul.
    Returns (success, result).
    """
    dot_product = _dot(lines[line_no][0], lines[line_no][1])
    discriminant = (dot_product * dot_product + radius * radius
                    - _abs_sq(lines[line_no][0]))

    if discriminant < 0.0:
        return False, (0.0, 0.0)

    sqrt_disc = math.sqrt(discriminant)
    t_left = -dot_product - sqrt_disc
    t_right = -dot_product + sqrt_disc

    for i in range(line_no):
        denominator = _det(lines[line_no][1], lines[i][1])
        numerator = _det(lines[i][1], _sub(lines[line_no][0], lines[i][0]))

        if abs(denominator) <= RVO_EPSILON:
            if numerator < 0.0:
                return False, (0.0, 0.0)
            continue

        t = numerator / denominator

        if denominator >= 0.0:
            t_right = min(t_right, t)
        else:
            t_left = max(t_left, t)

        if t_left > t_right:
            return False, (0.0, 0.0)

    if direction_opt:
        if _dot(opt_velocity, lines[line_no][1]) > 0.0:
            result = _add(lines[line_no][0], _scale(lines[line_no][1], t_right))
        else:
            result = _add(lines[line_no][0], _scale(lines[line_no][1], t_left))
    else:
        t = _dot(lines[line_no][1], _sub(opt_velocity, lines[line_no][0]))
        if t < t_left:
            result = _add(lines[line_no][0], _scale(lines[line_no][1], t_left))
        elif t > t_right:
            result = _add(lines[line_no][0], _scale(lines[line_no][1], t_right))
        else:
            result = _add(lines[line_no][0], _scale(lines[line_no][1], t))

    return True, result


def _linear_program_2(lines, radius, opt_velocity, direction_opt):
    """
    RVO2 linearProgram2: Tum cizgileri saglayan, opt_velocity'ye en yakin hizi bul.
    Returns (result, fail_line). fail_line == len(lines) ise basarili.
    """
    if direction_opt:
        result = _scale(opt_velocity, radius)
    elif _abs_sq(opt_velocity) > radius * radius:
        result = _scale(_normalize(opt_velocity), radius)
    else:
        result = opt_velocity

    for i in range(len(lines)):
        # Bu cizgi ihlal ediliyor mu?
        if _det(lines[i][1], _sub(lines[i][0], result)) > 0.0:
            temp_result = result
            success, result = _linear_program_1(
                lines, i, radius, opt_velocity, direction_opt)
            if not success:
                result = temp_result
                return result, i

    return result, len(lines)


def _linear_program_3(lines, begin_line, radius, result):
    """
    RVO2 linearProgram3: LP2 basarisiz olunca fallback.
    Kisitlari projekte edip tekrar dener.
    """
    distance = 0.0

    for i in range(begin_line, len(lines)):
        if _det(lines[i][1], _sub(lines[i][0], result)) > distance:
            proj_lines = []

            for j in range(i):
                determinant = _det(lines[i][1], lines[j][1])

                if abs(determinant) <= RVO_EPSILON:
                    if _dot(lines[i][1], lines[j][1]) > 0.0:
                        continue
                    point = _scale(_add(lines[i][0], lines[j][0]), 0.5)
                else:
                    point = _add(
                        lines[i][0],
                        _scale(
                            lines[i][1],
                            _det(lines[j][1],
                                 _sub(lines[i][0], lines[j][0])) / determinant
                        )
                    )

                direction = _normalize(_sub(lines[j][1], lines[i][1]))
                proj_lines.append((point, direction))

            temp_result = result
            dir_for_opt = (-lines[i][1][1], lines[i][1][0])
            result, fail = _linear_program_2(
                proj_lines, radius, dir_for_opt, True)

            if fail < len(proj_lines):
                result = temp_result

            distance = _det(lines[i][1], _sub(lines[i][0], result))

    return result


# ============================================================================
# ORCA CIZGISI HESABI — RVO2 computeNewVelocity'den birebir port
# ============================================================================

def _compute_orca_line(own_vel, rel_pos, rel_vel, combined_radius,
                       inv_tau, inv_dt):
    """
    Tek bir komsu icin ORCA cizgisi hesapla.
    RVO2 Agent::computeNewVelocity fonksiyonundaki agent ORCA lines kismi.

    Returns: (point, direction) — ORCA cizgisi
    """
    dist_sq = _abs_sq(rel_pos)
    combined_r_sq = combined_radius * combined_radius

    if dist_sq > combined_r_sq:
        # Henuz carpisma yok
        w = _sub(rel_vel, _scale(rel_pos, inv_tau))
        w_len_sq = _abs_sq(w)
        dot_pw = _dot(w, rel_pos)

        if dot_pw < 0.0 and dot_pw * dot_pw > combined_r_sq * w_len_sq:
            # Cutoff dairesi uzerine projeksiyon
            w_len = math.sqrt(w_len_sq)
            if w_len < RVO_EPSILON:
                unit_w = (1.0, 0.0)
            else:
                unit_w = (w[0] / w_len, w[1] / w_len)
            direction = (unit_w[1], -unit_w[0])
            u = _scale(unit_w, combined_radius * inv_tau - w_len)
        else:
            # Koni bacagi uzerine projeksiyon
            leg = math.sqrt(max(0.0, dist_sq - combined_r_sq))

            if _det(rel_pos, w) > 0.0:
                # Sol bacak
                direction = (
                    (rel_pos[0] * leg - rel_pos[1] * combined_radius) / dist_sq,
                    (rel_pos[0] * combined_radius + rel_pos[1] * leg) / dist_sq
                )
            else:
                # Sag bacak (negatif)
                direction = (
                    -(rel_pos[0] * leg + rel_pos[1] * combined_radius) / dist_sq,
                    -(-rel_pos[0] * combined_radius + rel_pos[1] * leg) / dist_sq
                )

            dot_rv_dir = _dot(rel_vel, direction)
            u = _sub(_scale(direction, dot_rv_dir), rel_vel)
    else:
        # Zaten cakisiyor — acil ayirma
        w = _sub(rel_vel, _scale(rel_pos, inv_dt))
        w_len = _length(w)

        if w_len < RVO_EPSILON:
            unit_w = (1.0, 0.0)
        else:
            unit_w = (w[0] / w_len, w[1] / w_len)

        direction = (unit_w[1], -unit_w[0])
        u = _scale(unit_w, combined_radius * inv_dt - w_len)

    # ORCA cizgisi: point = own_vel + u/2 (reciprocal: yarim sorumluluk)
    point = _add(own_vel, _scale(u, 0.5))
    return (point, direction)


# ============================================================================
# ANA NODE
# ============================================================================

class CollisionAvoidanceNode(Node):

    def __init__(self):
        self.ns = os.environ.get('DRONE_NS', 'drone1')
        self.drone_id = int(os.environ.get('DRONE_ID', '1'))
        self.swarm_size = SWARM_SIZE

        super().__init__(
            f'collision_avoidance_{self.drone_id}',
            namespace=self.ns,
        )

        self.get_logger().info(
            f'CollisionAvoidance ORCA v3 basladi — ns={self.ns}, '
            f'id={self.drone_id}, swarm={self.swarm_size}'
        )

        # Dahili durum
        self._own_pose = None
        self._own_pose_time = 0.0
        self._own_vel = (0.0, 0.0, 0.0)
        self._setpoint_raw = None
        self._sp_raw_time = 0.0

        self._neighbor_poses = {}
        self._neighbor_pose_times = {}
        self._neighbor_vels = {}
        self._neighbor_states = {}
        self._detach_drone_id = 0

        # Osilasyon tespiti
        self._sp_hist_x = deque(maxlen=OSC_WINDOW)
        self._sp_hist_y = deque(maxlen=OSC_WINDOW)
        self._last_osc_event_time = 0.0
        self._last_sp_final = None

        # Debug
        self._dbg_closest_dist = float('inf')
        self._dbg_active = 0

        # QoS
        be_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST, depth=1)
        rel_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST, depth=10)

        # Abonelikler
        self.create_subscription(
            PoseStamped, f'/{self.ns}/setpoint_raw',
            self._on_sp_raw, 10)
        self.create_subscription(
            PoseStamped, f'/{self.ns}/pose',
            self._on_own_pose, be_qos)
        self.create_subscription(
            TwistStamped, f'/{self.ns}/velocity',
            self._on_own_vel, be_qos)

        for i in range(1, self.swarm_size + 1):
            if i == self.drone_id:
                continue
            self.create_subscription(
                PoseStamped, f'/drone{i}/pose',
                lambda m, u=i: self._on_n_pose(m, u), be_qos)
            self.create_subscription(
                TwistStamped, f'/drone{i}/velocity',
                lambda m, u=i: self._on_n_vel(m, u), be_qos)
            self.create_subscription(
                LocalState, f'/drone{i}/local_state',
                lambda m, u=i: self._on_n_state(m, u), be_qos)

        self.create_subscription(
            SwarmIntent, '/swarm/intent', self._on_intent, 10)

        # Yayincilar
        self._pub_final = self.create_publisher(
            PoseStamped, f'/{self.ns}/setpoint_final', 10)
        self._pub_safety = self.create_publisher(
            SafetyEvent, '/safety/event', rel_qos)

        self.create_timer(CTRL_DT, self._control_loop)

        self.get_logger().info(
            f'ORCA params: R={AGENT_RADIUS}m TAU={TAU}s '
            f'MAX_SPD={MAX_SPEED}m/s LOOK={LOOKAHEAD}s')

    # === Callback'ler ========================================================

    def _on_sp_raw(self, m):
        p = m.pose.position
        self._setpoint_raw = (p.x, p.y, p.z)
        self._sp_raw_time = time.time()

    def _on_own_pose(self, m):
        p = m.pose.position
        self._own_pose = (p.x, p.y, p.z)
        self._own_pose_time = time.time()

    def _on_own_vel(self, m):
        v = m.twist.linear
        self._own_vel = (v.x, v.y, v.z)

    def _on_n_pose(self, m, uid):
        p = m.pose.position
        self._neighbor_poses[uid] = (p.x, p.y, p.z)
        self._neighbor_pose_times[uid] = time.time()

    def _on_n_vel(self, m, uid):
        v = m.twist.linear
        self._neighbor_vels[uid] = (v.x, v.y, v.z)

    def _on_n_state(self, m, uid):
        self._neighbor_states[uid] = m.state

    def _on_intent(self, m):
        self._detach_drone_id = int(m.detach_drone_id)

    # === Osilasyon Tespiti ===================================================

    def _check_oscillation(self, sp):
        self._sp_hist_x.append(sp[0])
        self._sp_hist_y.append(sp[1])
        if self._own_pose[2] < 3.0 or len(self._sp_hist_x) < OSC_WINDOW:
            return
        var_x = _variance(list(self._sp_hist_x))
        var_y = _variance(list(self._sp_hist_y))
        std_xy = math.sqrt((var_x + var_y) / 2.0)
        if std_xy < OSC_THRESH_M:
            return
        now = time.time()
        if now - self._last_osc_event_time < OSC_COOLDOWN_S:
            return
        self._last_osc_event_time = now
        evt = SafetyEvent()
        evt.header = Header()
        evt.header.stamp = self.get_clock().now().to_msg()
        evt.header.frame_id = self.ns
        evt.drone_id = self.drone_id
        evt.event_type = 'OSCILLATION'
        evt.description = (
            f'drone{self.drone_id} osilasyon: std={std_xy:.3f}m')
        evt.severity = min(1.0, float(std_xy / (OSC_THRESH_M * 3.0)))
        self._pub_safety.publish(evt)
        self.get_logger().warn(f'OSILASYON: std={std_xy:.3f}m')

    # === Ana Kontrol Dongusu — 50 Hz ========================================

    def _control_loop(self):
        now = time.time()

        if self._setpoint_raw is None:
            return
        if now - self._sp_raw_time > SP_STALE_S:
            return
        if self._own_pose is None:
            self._publish(self._setpoint_raw)
            return

        own_pos = self._own_pose
        own_vel_2d = (self._own_vel[0], self._own_vel[1])
        sp_raw = self._setpoint_raw

        # Aktif komsu var mi?
        active = [u for u, s in self._neighbor_states.items()
                  if s not in ('DISARM_WAIT', 'LANDING', '')]
        if not active:
            self._publish(sp_raw)
            return

        # Tercih edilen hiz: hedefe dogru
        dx = sp_raw[0] - own_pos[0]
        dy = sp_raw[1] - own_pos[1]
        dist_to_tgt = math.sqrt(dx * dx + dy * dy)

        if dist_to_tgt > 0.1:
            speed = min(MAX_SPEED, dist_to_tgt / LOOKAHEAD)
            v_pref = (dx / dist_to_tgt * speed, dy / dist_to_tgt * speed)
        else:
            v_pref = (0.0, 0.0)

        # ORCA cizgilerini hesapla
        orca_lines = []
        closest = float('inf')
        act_count = 0
        inv_tau = 1.0 / TAU
        inv_dt = 1.0 / CTRL_DT

        for uid, npos in self._neighbor_poses.items():
            if now - self._neighbor_pose_times.get(uid, 0.0) > POSE_STALE_S:
                continue
            state = self._neighbor_states.get(uid, '')
            if state in ('DISARM_WAIT', 'LANDING'):
                continue

            rel_pos = (npos[0] - own_pos[0], npos[1] - own_pos[1])
            d = _length(rel_pos)
            closest = min(closest, d)
            act_count += 1

            nvel = self._neighbor_vels.get(uid, (0.0, 0.0, 0.0))
            rel_vel = (self._own_vel[0] - nvel[0], self._own_vel[1] - nvel[1])

            combined_r = 2.0 * AGENT_RADIUS
            line = _compute_orca_line(
                own_vel_2d, rel_pos, rel_vel, combined_r, inv_tau, inv_dt)
            orca_lines.append(line)

        self._dbg_closest_dist = closest
        self._dbg_active = act_count

        # LP coz: guvenli hiz bul
        result, fail_line = _linear_program_2(
            orca_lines, MAX_SPEED, v_pref, False)

        if fail_line < len(orca_lines):
            result = _linear_program_3(
                orca_lines, fail_line, MAX_SPEED, result)

        v_safe = result

        # === HIZ SINIRLA — yakinlastikca yavaşla ===
        # ArduPilot aninda duramaz. 4m/s'de frenleme ~4m.
        # Cozum: mesafe azaldikca max hizi dusur.
        #   8m  → 4.0 m/s (tam hiz)
        #   4m  → 2.0 m/s
        #   2m  → 1.0 m/s
        if closest < SLOWDOWN_DIST:
            max_allowed = MAX_SPEED * (closest / SLOWDOWN_DIST)
            max_allowed = max(0.3, max_allowed)  # minimum 0.3 m/s
            spd = _length(v_safe)
            if spd > max_allowed:
                v_safe = _scale(_normalize(v_safe), max_allowed)

        # === HARD SAFETY KATMANI ===
        # ORCA'nin ustune son savunma: mesafe < HARD_SAFETY_DIST ise
        # setpoint'i dogrudan komsulardan UZAGA koy.
        # ORCA hiz tabanli ama ArduPilot gecikme yapiyor → hard safety pozisyon tabanli.
        if closest < HARD_SAFETY_DIST:
            escape_x, escape_y = 0.0, 0.0
            for uid, npos in self._neighbor_poses.items():
                if now - self._neighbor_pose_times.get(uid, 0.0) > POSE_STALE_S:
                    continue
                state = self._neighbor_states.get(uid, '')
                if state in ('DISARM_WAIT', 'LANDING'):
                    continue
                dx_n = own_pos[0] - npos[0]
                dy_n = own_pos[1] - npos[1]
                d_n = math.sqrt(dx_n * dx_n + dy_n * dy_n)
                if d_n < HARD_SAFETY_DIST and d_n > 0.01:
                    # Normalize + ters kare: yakinken cok guclu
                    escape_x += (dx_n / d_n) / (d_n * d_n)
                    escape_y += (dy_n / d_n) / (d_n * d_n)

            esc_len = math.sqrt(escape_x * escape_x + escape_y * escape_y)
            if esc_len > 0.01:
                escape_x /= esc_len
                escape_y /= esc_len

            # Setpoint'i dogrudan uzaga koy (hiz hesabi degil, pozisyon!)
            escape_dist = HARD_SAFETY_DIST
            sp_final = (
                own_pos[0] + escape_x * escape_dist,
                own_pos[1] + escape_y * escape_dist,
                sp_raw[2],
            )
            self._check_oscillation(sp_final)
            self._publish(sp_final)
            self.get_logger().warn(
                f'HARD SAFETY! d={closest:.2f}m → setpoint {escape_dist:.1f}m uzaga')
            return

        # Setpoint'e cevir
        sp_final = (
            own_pos[0] + v_safe[0] * LOOKAHEAD,
            own_pos[1] + v_safe[1] * LOOKAHEAD,
            sp_raw[2],
        )

        self._check_oscillation(sp_final)
        self._publish(sp_final)

        # Debug — her saniye log bas
        if int(now) % 1 == 0 and int(now * CTRL_HZ) % int(CTRL_HZ) == 0:
            self.get_logger().warn(
                f'ORCA d={closest:.1f}m n={act_count} '
                f'vpref=({v_pref[0]:.1f},{v_pref[1]:.1f}) '
                f'vsafe=({v_safe[0]:.1f},{v_safe[1]:.1f}) '
                f'states={dict(self._neighbor_states)}')

    # === Setpoint Yayini =====================================================

    def _publish(self, sp):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = float(sp[0])
        msg.pose.position.y = float(sp[1])
        msg.pose.position.z = float(sp[2])
        msg.pose.orientation.w = 1.0
        self._pub_final.publish(msg)
        self._last_sp_final = sp


def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
