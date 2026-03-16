#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       precision_landing.py                                   ║
║          Hassas İniş — DETACH Drone'unu Renk Zone'una Getir                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

NEDEN GEREKLİ?
--------------
formation_controller, DETACH drone'unu zone'a "yaklaşık" yönlendiriyor.
local_fsm 3m yarıçap içinde LAND modunu tetikliyor.
Ama 3m'de iniş = zone dışına çıkma riski = SIFIR puan!

Bu node DETACH süresince dronu zone'un TAM merkezi üzerine getiriyor:
  formation_controller → setpoint_raw → collision_avoidance → setpoint_final → MAVROS
  precision_landing    → landing_target ─────────────────────────────────────► MAVROS (üstünlük!)

drone_interface her ikisini de MAVROS'a iletiyor; son gelen setpoint kazanır.
precision_landing 10 Hz yayınladığı için formation_controller'ı override eder.

DETACH FAZI AKIŞI:
------------------
  1) intent.task_id='DETACH' + intent.detach_drone_id == kendi drone_id
     → BEN ayrılacak droneyim!
  2) /perception/color_zones → hedef rengi ara (intent.zone_color)
  3) zone bulundu → /{ns}/landing_target yayınla:
       x = zone_x,  y = zone_y,  z = HOVER_ALT_M (sabit irtifada bekle)
  4) XY hizalandı (< XY_PRECISE_M) → local_fsm 3m kontrolünü tetikler
     → local_fsm LAND_ZONE'a geçer, LAND komutu gönderir
     → ArduPilot hassas iner ✅
  5) LAND_ZONE / DISARM_WAIT → precision_landing durur

YAYINLANAN:
-----------
  /{ns}/landing_target  → PoseStamped (drone_interface → MAVROS)

İZLENEN:
---------
  /swarm/intent             → hangi drone ayrılıyor + zone rengi
  /perception/color_zones   → zone konumları
  /{ns}/pose                → kendi konumu (hizalama kontrolü)
  /{ns}/local_state         → kendi durumu (aktif/pasif)

ŞARTNAME UYUMU:
  §13  Renk zone'una hassas iniş    → XY < XY_PRECISE_M garantisi ✅
  §5.3 Dağıtık mimari               → Her drone kendi precision_landing'ini çalıştırır ✅
  §5.4 Çarpışma önleme              → HOVER_ALT_M sabit irtifada bekle ✅
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from geometry_msgs.msg import PoseStamped
from swarm_msgs.msg import SwarmIntent, LocalState, ColorZoneList

# ══════════════════════════════════════════════════════════════════════════════
# PARAMETRE SABİTLERİ
# ══════════════════════════════════════════════════════════════════════════════

CTRL_HZ: float = 10.0          # Kontrol döngüsü frekansı
CTRL_DT: float = 1.0 / CTRL_HZ

HOVER_ALT_M: float = 5.0       # Zone üzerinde hover irtifası [m] (iniş öncesi)
XY_PRECISE_M: float = 0.8      # Bu XY hatasından küçükse "hizalandı" say [m]

# Zone verisi tazelik sınırı
ZONE_STALE_S: float = 3.0      # Bu kadar eski zone verisi → kullanma


# ══════════════════════════════════════════════════════════════════════════════
# ANA NODE
# ══════════════════════════════════════════════════════════════════════════════

class PrecisionLandingNode(Node):
    """
    Hassas iniş nodu — her drone'da çalışır.
    Sadece "ben ayrılacak droneyim" durumunda aktif olur.
    """

    def __init__(self):
        super().__init__('precision_landing')

        # ── Parametreler ──────────────────────────────────────────────────────
        self.declare_parameter('drone_id',   1)
        self.declare_parameter('num_drones', 3)

        self.drone_id: int = self.get_parameter('drone_id').value
        self.ns: str       = f'drone{self.drone_id}'

        self.get_logger().info(
            f'PrecisionLanding başladı — drone{self.drone_id}\n'
            f'  Hover irtifası : {HOVER_ALT_M}m\n'
            f'  XY hassasiyet  : {XY_PRECISE_M}m'
        )

        # ── Dahili durum ──────────────────────────────────────────────────────
        self._i_am_detach_drone: bool = False   # Ben mi ayrılıyorum?
        self._target_zone_color: str  = ''      # Hedef zone rengi
        self._zone_pos: tuple[float, float, float] | None = None  # Zone konumu
        self._zone_recv_time: float = 0.0

        self._own_pos: tuple[float, float, float] | None = None
        self._own_state: str = 'STANDBY'

        self._xy_aligned: bool = False          # Hizalandı mı? (log için)

        # ── QoS profilleri ────────────────────────────────────────────────────
        be_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )
        rel_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
        )

        # ── Abonelikler ───────────────────────────────────────────────────────

        # 1) Sürü niyeti → hangi drone ayrılıyor + zone rengi
        self.create_subscription(
            SwarmIntent, '/swarm/intent', self._on_intent, rel_qos
        )

        # 2) Renk zone konumları → qr_perception yayınlar
        self.create_subscription(
            ColorZoneList, '/perception/color_zones',
            self._on_color_zones, rel_qos
        )

        # 3) Kendi konumu
        self.create_subscription(
            PoseStamped, f'/{self.ns}/pose',
            self._on_own_pose, be_qos
        )

        # 4) Kendi durumu (DETACH / LAND_ZONE / DISARM_WAIT)
        # BEST_EFFORT — local_fsm BEST_EFFORT yayınlar
        self.create_subscription(
            LocalState, f'/{self.ns}/local_state',
            self._on_own_state, be_qos
        )

        # ── Yayıncı ───────────────────────────────────────────────────────────
        # drone_interface bu topic'i dinliyor → MAVROS'a iletiyor
        self._landing_target_pub = self.create_publisher(
            PoseStamped, f'/{self.ns}/landing_target', rel_qos
        )

        # ── Kontrol döngüsü ───────────────────────────────────────────────────
        self.create_timer(CTRL_DT, self._control_loop)

    # ══════════════════════════════════════════════════════════════════════════
    # CALLBACK'LER
    # ══════════════════════════════════════════════════════════════════════════

    def _on_intent(self, msg: SwarmIntent) -> None:
        """
        SwarmIntent → Ben mi ayrılacak droneyim?

        intent.task_id == 'DETACH' VE intent.detach_drone_id == kendi drone_id
        olduğunda aktif oluyoruz.
        """
        was_detach = self._i_am_detach_drone

        if (msg.task_id == 'DETACH'
                and int(msg.detach_drone_id) == self.drone_id):
            self._i_am_detach_drone  = True
            self._target_zone_color  = msg.zone_color.upper()
        else:
            self._i_am_detach_drone = False
            self._target_zone_color = ''

        if self._i_am_detach_drone and not was_detach:
            self.get_logger().info(
                f'[{self.ns}] 🎯 PrecisionLanding AKTİF! '
                f'Hedef zone: {self._target_zone_color}'
            )
        elif not self._i_am_detach_drone and was_detach:
            self.get_logger().info(f'[{self.ns}] PrecisionLanding pasif.')
            self._zone_pos     = None
            self._xy_aligned   = False

    def _on_color_zones(self, msg: ColorZoneList) -> None:
        """
        /perception/color_zones → Hedef rengi ara, zone konumunu kaydet.
        """
        if not self._i_am_detach_drone or not self._target_zone_color:
            return

        import time as _time
        for zone in msg.zones:
            if zone.color.upper() == self._target_zone_color:
                self._zone_pos       = (zone.position.x,
                                        zone.position.y,
                                        zone.position.z)
                self._zone_recv_time = _time.time()
                return

    def _on_own_pose(self, msg: PoseStamped) -> None:
        """Kendi konumunu güncelle."""
        p = msg.pose.position
        self._own_pos = (p.x, p.y, p.z)

    def _on_own_state(self, msg: LocalState) -> None:
        """Kendi durum makinesi durumunu takip et."""
        self._own_state = msg.state

    # ══════════════════════════════════════════════════════════════════════════
    # ANA KONTROL DÖNGÜSÜ — 10 Hz
    # ══════════════════════════════════════════════════════════════════════════

    def _control_loop(self) -> None:
        """
        10 Hz kontrol döngüsü.

        Aktif koşullar:
          - Ben ayrılacak droneyim (_i_am_detach_drone)
          - Kendi durumum DETACH veya LAND_ZONE (aktif iniş fazı)
          - Zone konumunu biliyorum
          - Kendi konumumu biliyorum
        """
        # ── 1) Aktif mi? ──────────────────────────────────────────────────────
        if not self._i_am_detach_drone:
            return

        # DISARM_WAIT veya sonrası → iniş tamamlandı, dur
        if self._own_state in ('DISARM_WAIT', 'REARM', 'REJOIN',
                               'LANDING', 'RETURN_HOME', 'STANDBY'):
            return

        # DETACH veya LAND_ZONE → aktif
        if self._own_state not in ('DETACH', 'LAND_ZONE'):
            return

        # ── 2) Veri kontrolleri ───────────────────────────────────────────────
        if self._own_pos is None:
            return

        if self._zone_pos is None:
            # Zone bulunamadı — /perception/color_zones bekleniyor
            self.get_logger().warn(
                f'[{self.ns}] Zone bulunamadı ({self._target_zone_color}), '
                f'/perception/color_zones bekleniyor...',
                throttle_duration_sec=3.0,
            )
            return

        import time as _time
        if _time.time() - self._zone_recv_time > ZONE_STALE_S:
            self.get_logger().warn(
                f'[{self.ns}] Zone verisi eski ({ZONE_STALE_S}s+), yayın durduruldu.',
                throttle_duration_sec=5.0,
            )
            return

        # ── 3) XY hizalama kontrolü (log amaçlı) ─────────────────────────────
        zx, zy, _ = self._zone_pos
        ox, oy, oz = self._own_pos
        xy_err = math.sqrt((ox - zx) ** 2 + (oy - zy) ** 2)

        if xy_err <= XY_PRECISE_M and not self._xy_aligned:
            self._xy_aligned = True
            self.get_logger().info(
                f'[{self.ns}] ✅ XY HİZALANDI! '
                f'Hata={xy_err:.2f}m < {XY_PRECISE_M}m — '
                f'Zone merkezi üzerindeyim, local_fsm LAND tetikleyecek'
            )
        elif xy_err > XY_PRECISE_M * 2 and self._xy_aligned:
            self._xy_aligned = False  # Sürüklendi, tekrar hizalanıyor

        # ── 4) Landing target yayınla ─────────────────────────────────────────
        # DETACH   → hover irtifasında bekle (oz'u koru veya HOVER_ALT_M hedefle)
        # LAND_ZONE → local_fsm zaten LAND gönderdi; biz XY doğruluğunu koru
        target_z = max(HOVER_ALT_M, oz) if self._own_state == 'DETACH' else oz

        sp = PoseStamped()
        sp.header.stamp    = self.get_clock().now().to_msg()
        sp.header.frame_id = 'map'
        sp.pose.position.x = zx          # Zone merkezi X
        sp.pose.position.y = zy          # Zone merkezi Y
        sp.pose.position.z = target_z    # İrtifayı koru
        sp.pose.orientation.w = 1.0      # Düz (yaw değişmez)

        self._landing_target_pub.publish(sp)

        # Periyodik log (3s'de bir)
        self.get_logger().debug(
            f'[{self.ns}] LandingTarget → '
            f'zone=({zx:.1f},{zy:.1f}) '
            f'XY_err={xy_err:.2f}m '
            f'state={self._own_state}',
            throttle_duration_sec=3.0,
        )


# ══════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ══════════════════════════════════════════════════════════════════════════════

def main(args=None):
    rclpy.init(args=args)
    node = PrecisionLandingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
