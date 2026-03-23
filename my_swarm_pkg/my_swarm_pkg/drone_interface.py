#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          drone_interface.py                                  ║
║                      MAVROS ↔ ROS2 Sistemi Köprüsü                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

GENEL AÇIKLAMA:
---------------
Bu node, ArduPilot uçuş kontrolcüsü (Pixhawk) ile ROS2 yazılım sistemimiz
arasındaki TEK iletişim noktasıdır. "Köprü" görevi görür.

    ┌─────────────┐    MAVROS    ┌──────────────────┐    ROS2    ┌──────────────┐
    │  ArduPilot  │◄────────────►│ drone_interface  │◄──────────►│  Sistemimiz  │
    │  (Pixhawk)  │   protokol  │    (bu dosya)    │  topic'ler │  (diğer node)│
    └─────────────┘             └──────────────────┘            └──────────────┘

NE YAPAR:
---------
  1. Pixhawk'tan GELEN bilgileri (konum, hız, durum) ROS2 topic'lerine yayınlar
  2. ROS2 sisteminden GELEN komutları (setpoint, mod) Pixhawk'a iletir
  3. RC kill-switch veya mod değişimi algılarsa PILOT OVERRIDE yayınlar

KOORDİNAT SİSTEMİ:
------------------
  ArduPilot → NED  (North-East-Down):  X=Kuzey, Y=Doğu,  Z=Aşağı
  ROS2      → ENU  (East-North-Up):    X=Doğu,  Y=Kuzey, Z=Yukarı
  MAVROS bu dönüşümü otomatik yapar, biz ENU kullanırız.

ÇALIŞTIRMA:
-----------
  ros2 run my_swarm_pkg drone_interface --ros-args -p drone_id:=1
  ros2 run my_swarm_pkg drone_interface --ros-args -p drone_id:=2
  ros2 run my_swarm_pkg drone_interface --ros-args -p drone_id:=3

ŞARTNAME KARŞILAŞTIRMASI:
  §5.3  Dağıtık mimari → Her drone kendi drone_interface'ini çalıştırır ✅
  §5.4  Failsafe       → pilot_override ile RC kaybı algılanır ✅
  §5.5.4 Kill-switch   → GUIDED dışı mod = pilot_override=True ✅
"""

import os
import struct
import threading

import serial
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandLong, CommandTOL
from std_msgs.msg import Bool, String


class DroneInterface(Node):
    """
    MAVROS ile ROS2 sistemimiz arasındaki köprü node'u.
    Her drone için ayrı bir örnek çalışır.
    """

    def __init__(self):
        super().__init__('drone_interface')

        # ══════════════════════════════════════════════════════
        # PARAMETRE OKUMA
        # drone_id: Hangi drone? (1, 2 veya 3)
        # launch dosyasından veya -p drone_id:=2 ile verilir
        # ══════════════════════════════════════════════════════
        self.declare_parameter('drone_id', 1)
        self.declare_parameter('takeoff_altitude', 10.0)
        self.declare_parameter('uwb_enabled', False)
        self.declare_parameter('uwb_port', '/dev/ttyUSB1')
        self.drone_id = self.get_parameter('drone_id').value
        self.takeoff_altitude = self.get_parameter('takeoff_altitude').value
        self._uwb_enabled = self.get_parameter('uwb_enabled').value
        self._uwb_port    = self.get_parameter('uwb_port').value

        # Topic prefix oluştur: drone_id=2 → ns='drone2'
        self.ns = f'drone{self.drone_id}'
        self.mavros_ns = f'/{self.ns}/mavros'

        # HOME offset: MAVROS local frame → global frame dönüşümü
        # Launch dosyasından env var olarak gelir
        self._home_x = float(os.environ.get('HOME_X', '0.0'))
        self._home_y = float(os.environ.get('HOME_Y', '0.0'))

        self.get_logger().info(
            f'🔌 drone_interface başlatılıyor...\n'
            f'   Drone ID  : {self.drone_id}\n'
            f'   Topic ns  : /{self.ns}/\n'
            f'   MAVROS ns : {self.mavros_ns}/\n'
            f'   HOME offset: ({self._home_x}, {self._home_y})'
        )

        # ══════════════════════════════════════════════════════
        # DURUM DEĞİŞKENLERİ
        # ══════════════════════════════════════════════════════
        self.current_state = State()   # MAVROS'tan gelen son durum
        self.last_mode = ''            # Son gönderilen mod (tekrar engeli)
        self.pilot_override_active = False  # RC kill-switch aktif mi?
        self._arm_pending = False      # ARM komutu GUIDED onayı bekliyor
        self._arm_in_progress = False  # arm() çağrısı devam ediyor (disarm false-trigger koruması)
        self._current_altitude = 0.0   # MAVROS ENU z (metre) - yükseklik kapısı için
        # State-triggered yayın için: son yayınlanan değeri sakla.
        # Böylece sadece değişince yayınlarız, gereksiz Wi-Fi trafiği önlenir.
        self._last_published_override = None

        # ══════════════════════════════════════════════════════
        # QoS AYARI
        # NEDEN BEST_EFFORT?
        # MAVROS bazı topic'leri BEST_EFFORT ile yayınlar.
        # Subscriber RELIABLE olursa mesajlar HİÇ GELMEZ!
        # (swarm_takeoff'taki QoS uyumsuzluk uyarısının sebebi buydu)
        # ══════════════════════════════════════════════════════
        best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # ══════════════════════════════════════════════════════
        # MAVROS → SİSTEM ABONELİKLERİ
        # Pixhawk'tan okuyup sistemimize yayınlıyoruz
        # ══════════════════════════════════════════════════════

        # 1) KONUM: Her 50ms'de bir gelir (20 Hz)
        #    position.x/y/z = ENU koordinat (metre)
        #    orientation    = Quaternion (drone yönü)
        #    → formation_controller ve collision_avoidance kullanır
        self.create_subscription(
            PoseStamped,
            f'{self.mavros_ns}/local_position/pose',
            self._mavros_pose_cb,
            best_effort_qos   # MAVROS BEST_EFFORT yayınlıyor!
        )

        # 2) HIZ: Anlık hız vektörü (m/s)
        #    twist.linear.x/y/z = ENU hız
        #    → collision_avoidance APF'de "komşu nereye gidiyor?" için kullanır
        self.create_subscription(
            TwistStamped,
            f'{self.mavros_ns}/local_position/velocity_local',
            self._mavros_velocity_cb,
            best_effort_qos
        )

        # 3) DURUM: armed mi? hangi modda? bağlı mı?
        #    → Pilot override tespiti için izliyoruz
        self.create_subscription(
            State,
            f'{self.mavros_ns}/state',
            self._mavros_state_cb,
            10
        )

        # ══════════════════════════════════════════════════════
        # SİSTEM → MAVROS ABONELİKLERİ
        # Sistemimizden alıp Pixhawk'a iletiyoruz
        # ══════════════════════════════════════════════════════

        # 4) NİHAİ SETPOINT: collision_avoidance'dan gelir
        #    APF uygulandıktan sonra "gerçek hedef konum"
        #    → Pixhawk bu koordinata doğru uçar
        self.create_subscription(
            PoseStamped,
            f'/{self.ns}/setpoint_final',
            self._setpoint_final_cb,
            10
        )

        # 5) MOD KOMUTU: SADECE local_fsm yazar! (güvenlik kuralı)
        #    State değişimlerinde mod komutunu gönderir:
        #    LANDING state → 'LAND', SAFETY state → 'RTL', vb.
        self.create_subscription(
            String,
            f'/{self.ns}/cmd_mode',
            self._cmd_mode_cb,
            10
        )

        # 6) ARM/DISARM KOMUTU: SADECE local_fsm yazar! (güvenlik kuralı)
        #    Bool mesajı: True=ARM, False=DISARM
        #    Kullanım senaryoları:
        #      STANDBY→IDLE geçişi : ARM=True  → motorlar hazır
        #      DISARM_WAIT state   : ARM=False → motorlar durur
        #      REARM state         : ARM=True  → sürüye yeniden katılım
        #    NEDEN TOPIC? local_fsm ayrı bir process, arm() metodunu
        #    doğrudan çağıramaz. Topic üzerinden haberleşmek zorundayız.
        self.create_subscription(
            Bool,
            f'/{self.ns}/cmd_arm',
            self._cmd_arm_cb,
            10
        )

        # 7) HASSAS İNİŞ HEDEFİ: precision_landing'den gelir
        #    Kamerayla renk zone tespit edilince iniş koordinatı gelir
        #    LAND_ZONE state'inde aktif (ileride yazacağız)
        self.create_subscription(
            PoseStamped,
            f'/{self.ns}/landing_target',
            self._landing_target_cb,
            10
        )

        # ══════════════════════════════════════════════════════
        # PUBLISHER'LAR
        # ══════════════════════════════════════════════════════

        # Sisteme konum yayınla (ENU metre)
        # → formation_controller centroid hesabı için okur
        # → collision_avoidance APF için okur
        self.pose_pub = self.create_publisher(
            PoseStamped, f'/{self.ns}/pose', 10
        )

        # Sisteme hız yayınla (ENU m/s)
        # → collision_avoidance "komşu nereye gidiyor?" için okur
        self.velocity_pub = self.create_publisher(
            TwistStamped, f'/{self.ns}/velocity', 10
        )

        # Pilot override durumu
        # True  = RC kill-switch / GUIDED dışı mod → otonom devre dışı
        # False = Normal, sistem kontrolde
        # → local_fsm ve intent_coordinator izler
        self.pilot_override_pub = self.create_publisher(
            Bool, f'/{self.ns}/pilot_override', 10
        )

        # MAVROS'a setpoint gönder (drone buraya gitsin)
        # setpoint_final ve landing_target bu publisher'ı kullanır
        self.mavros_setpoint_pub = self.create_publisher(
            PoseStamped,
            f'{self.mavros_ns}/setpoint_position/local',
            10
        )

        # UWB konumunu ArduPilot EKF'ye besle (GPS yerine kullanır)
        # Gerekli ArduPilot parametreleri:
        #   EK3_SRC1_POSXY = 6  (ExtNav)
        #   EK3_SRC1_VELXY = 6  (ExtNav)
        #   VISO_TYPE      = 1  (Aktif)
        self._uwb_pose_pub = self.create_publisher(
            PoseStamped,
            f'{self.mavros_ns}/vision_pose/pose',
            10
        )

        # ══════════════════════════════════════════════════════
        # SERVİS İSTEMCİLERİ
        # Topic'lerden farklı: istek-cevap mantığı
        # Mod değiştirme ve ARM için servis çağrısı gerekir
        # ══════════════════════════════════════════════════════

        # Uçuş modunu değiştir (GUIDED, LAND, RTL...)
        self.set_mode_client = self.create_client(
            SetMode, f'{self.mavros_ns}/set_mode'
        )

        # Drone ARM / DISARM et
        # ARM=True  → motorlar hazır
        # ARM=False → motorlar durur (güvenli)
        self.arming_client = self.create_client(
            CommandBool, f'{self.mavros_ns}/cmd/arming'
        )
        # Force ARM için MAVLink komut servisi (pre-arm check'leri atlayarak)
        self.cmd_client = self.create_client(
            CommandLong, f'{self.mavros_ns}/cmd/command'
        )

        # Kalkış komutu (ARM sonrası çağrılır)
        self.takeoff_client = self.create_client(
            CommandTOL, f'{self.mavros_ns}/cmd/takeoff'
        )

        # ══════════════════════════════════════════════════════
        # PERİYODİK GÖREV (Timer) - HEARTBEAT
        # State-triggered yaklaşım:
        #   → Durum değişince ANINDA yayınla (_mavros_state_cb içinde)
        #   → Değişmese bile her 5 sn'de bir "heartbeat" gönder
        #     (Yeni başlayan node'lar mevcut durumu öğrensin)
        # NEDEN 2 Hz DEĞİL?
        #   3 drone × 2 Hz = saniyede 6 gereksiz mesaj → Wi-Fi trafiği
        #   Sürü büyüdükçe (10 drone) bu 20 mesaj/sn olur → darboğaz!
        # ══════════════════════════════════════════════════════
        self.create_timer(5.0, self._heartbeat_pilot_override)

        # UWB thread'ini başlat (sadece uwb_enabled=True ise)
        if self._uwb_enabled:
            t = threading.Thread(target=self._uwb_reader_thread, daemon=True)
            t.start()
            self.get_logger().info(
                f'📡 [{self.ns}] UWB (Nooploop LinkTrack P-A) başlatıldı: {self._uwb_port}'
            )

        self.get_logger().info(
            f'✅ [{self.ns}] drone_interface HAZIR! Topic\'ler dinleniyor...'
        )

    # ══════════════════════════════════════════════════════════════════════
    # MAVROS → SİSTEM CALLBACK'LERİ
    # ══════════════════════════════════════════════════════════════════════

    def _mavros_pose_cb(self, msg: PoseStamped):
        """
        Pixhawk'tan gelen konumu sisteme ilet.
        MAVROS local frame → global frame: HOME offset ekle.
        Böylece tüm dronelar aynı koordinat sisteminde görünür.
        """
        self._current_altitude = msg.pose.position.z  # ENU: z = yukarı (metre)
        # Local → Global: HOME offset ekle
        msg.pose.position.x += self._home_x
        msg.pose.position.y += self._home_y
        msg.header.frame_id = 'map'
        self.pose_pub.publish(msg)

    def _mavros_velocity_cb(self, msg: TwistStamped):
        """Pixhawk'tan gelen hızı sisteme ilet."""
        self.velocity_pub.publish(msg)

    def _mavros_state_cb(self, msg: State):
        """
        Pixhawk durum değişimlerini izle → Pilot override kontrolü yap.

        ÇALIŞMA MANTIĞI:
        Drone ARM'lıyken GUIDED dışı bir moda geçerse
        → Pilot RC ile müdahale etti demektir
        → pilot_override = True
        → intent_coordinator bu drone'u FLYING listesinden çıkarır
        → "Drone düştü!" yanlış alarmı engellenir (Şartname §5.5.4)
        """
        prev_connected = self.current_state.connected
        prev_mode  = self.current_state.mode
        prev_armed = self.current_state.armed
        self.current_state = msg

        # Mod değiştiyse logla
        if prev_mode != msg.mode:
            self.get_logger().info(
                f'🔄 [{self.ns}] Mod: {prev_mode or "?"} → {msg.mode}'
            )

        # MAVROS yeni bağlandıysa ve bekleyen bir mod komutu varsa yeniden gönder
        # (drone3 gibi geç bağlanan durumlarda retry'lar bitmeden önce bağlantı gelmez)
        if not prev_connected and msg.connected and self.last_mode:
            self.get_logger().info(
                f'🔌 [{self.ns}] MAVROS yeni bağlandı → {self.last_mode} komutu yeniden gönderiliyor'
            )
            self._send_mode_with_retry(self.last_mode, retries_left=30)

        # Beklenmedik DISARM tespiti (motor arızası / çökme)
        # Önceden ARM'lıydı, şimdi değil ve biz ne ARM ne DISARM komutu vermedik
        if prev_armed and not msg.armed and not self._arm_pending and not self._arm_in_progress:
            if msg.mode == 'GUIDED':
                # GUIDED modda DISARM → ArduCopter auto-disarm (takeoff gecikmesi)
                # Pilot override değil — otomatik re-ARM dene
                self.get_logger().warn(
                    f'⚡ [{self.ns}] GUIDED auto-disarm! Re-ARM deneniyor...'
                )
                self.create_timer(2.0, lambda: self.arm(value=True))
            else:
                self.get_logger().warn(
                    f'💥 [{self.ns}] Beklenmedik DISARM! Motor arızası veya çökme.'
                )
                self.pilot_override_active = True
                self._publish_pilot_override_state()

        # Otonom sistem tarafından kullanılan izinli modlar (whitelist).
        # BRAKE : ArduPilot acil frenleme modu → sistemimiz tetikleyebilir
        # AUTO  : Önceden yüklenmiş rota modu  → sistemimiz tetikleyebilir
        # Bu modlar whitelist'te olmasa "pilot müdahalesi" sanılır ve
        # drone sürüden koparılır! (Yanlış alarm)
        AUTONOMOUS_MODES = ('GUIDED', 'LAND', 'RTL', 'BRAKE', 'AUTO')

        # ARM'lıyken whitelist dışı mod → GERÇEK PILOT MÜDAHALESİ!
        if msg.armed and msg.mode not in AUTONOMOUS_MODES:
            if not self.pilot_override_active:
                self.get_logger().warn(
                    f'⚠️  [{self.ns}] PILOT OVERRIDE! Mod: {msg.mode}'
                )
                self.pilot_override_active = True
                # Değişti → ANINDA yayınla (state-triggered)
                self._publish_pilot_override_state()
        else:
            if self.pilot_override_active:
                self.get_logger().info(
                    f'✅ [{self.ns}] Override bitti, otonom moda dönüldü'
                )
                self.pilot_override_active = False
                # Değişti → ANINDA yayınla (state-triggered)
                self._publish_pilot_override_state()

        # GUIDED onaylandıysa bekleyen ARM varsa şimdi gönder
        if msg.mode == 'GUIDED' and self._arm_pending and not msg.armed:
            self._arm_pending = False
            self.get_logger().info(
                f'✅ [{self.ns}] GUIDED onaylandı → ARM gönderiliyor'
            )
            self.arm(value=True)

    # ══════════════════════════════════════════════════════════════════════
    # SİSTEM → MAVROS CALLBACK'LERİ
    # ══════════════════════════════════════════════════════════════════════

    def _setpoint_final_cb(self, msg: PoseStamped):
        """
        collision_avoidance → setpoint_final → Pixhawk.

        Pipeline:
          formation_controller → setpoint_raw (ideal hedef)
               ↓
          collision_avoidance  → setpoint_final (APF sonrası gerçek hedef)
               ↓
          drone_interface (biz) → MAVROS → Pixhawk → drone uçar!

        YÜKSEKLİK KAPISI:
          CMD_NAV_TAKEOFF aktifken SET_POSITION_TARGET_LOCAL_NED gönderilirse
          ArduPilot GUIDED_TAKEOFF → GUIDED_POSITION geçişi yapar ve kalkış iptal olur!
          Bu yüzden drone yere yakınken (< 0.5m) setpoint iletmiyoruz.
          Drone 0.5m üzerine çıkınca (kalkış tamamlandı) formation_controller devralır.

        """
        if self._current_altitude < (self.takeoff_altitude - 1.0):
            return  # Kalkış tamamlanmadı, setpoint gönderme (TAKEOFF iptal olmasın)
        # Global → Local: HOME offset çıkar (MAVROS local frame bekler)
        msg.pose.position.x -= self._home_x
        msg.pose.position.y -= self._home_y
        self.mavros_setpoint_pub.publish(msg)

    def _cmd_mode_cb(self, msg: String):
        """
        local_fsm'den gelen mod komutunu Pixhawk'a ilet.

        KURAL: SADECE local_fsm bu topic'e yazar!
        Başka node yazarsa kaos olur. local_fsm tüm state geçişlerini yönetir.

        Örnek akışlar:
          state=FLYING  → cmd_mode='GUIDED' → Otonom uçuş
          state=LANDING → cmd_mode='LAND'   → Pixhawk iner
          state=SAFETY  → cmd_mode='RTL'    → Eve dön
        """
        if msg.data == self.last_mode:
            return  # Zaten bu moddayız, tekrar gönderme

        self.get_logger().info(
            f'🧭 [{self.ns}] Mod komutu: {msg.data}'
        )
        self.last_mode = msg.data
        self._send_mode_with_retry(msg.data, retries_left=30)

    def _send_mode_with_retry(self, mode: str, retries_left: int = 30):
        """set_mode servisi hazır değilse veya Pixhawk reddederse 2sn sonra tekrar dene (en fazla 30 kez)."""
        if self.set_mode_client.service_is_ready():
            req = SetMode.Request()
            req.custom_mode = mode

            future = self.set_mode_client.call_async(req)

            def _on_set_mode_done(f):
                try:
                    result = f.result()
                    if result.mode_sent:
                        self.get_logger().info(
                            f'✅ [{self.ns}] Mod değişti: {mode}'
                        )
                    else:
                        self.get_logger().warn(
                            f'⚠️  [{self.ns}] Pixhawk modu reddetti: {mode} '
                            f'(EKF hazır değil?), {retries_left}s sonra tekrar → kalan: {retries_left}'
                        )
                        if retries_left > 0:
                            _t = [None]

                            def _retry_mode():
                                _t[0].cancel()
                                self._send_mode_with_retry(mode, retries_left - 1)

                            _t[0] = self.create_timer(2.0, _retry_mode)
                        else:
                            self.last_mode = ''
                            self.get_logger().error(
                                f'❌ [{self.ns}] Pixhawk {mode} modunu 60sn içinde kabul etmedi!'
                            )
                except Exception as e:
                    self.last_mode = ''
                    self.get_logger().error(
                        f'❌ [{self.ns}] set_mode servis hatası: {e}'
                    )

            future.add_done_callback(_on_set_mode_done)
        elif retries_left > 0:
            self.get_logger().warn(
                f'⚠️  [{self.ns}] set_mode servisi hazır değil, '
                f'2sn sonra tekrar denenecek (kalan: {retries_left})'
            )
            _timer_holder = [None]

            def _retry():
                _timer_holder[0].cancel()
                self._send_mode_with_retry(mode, retries_left - 1)

            _timer_holder[0] = self.create_timer(2.0, _retry)
        else:
            self.last_mode = ''
            self.get_logger().error(
                f'❌ [{self.ns}] set_mode servisi 20sn içinde hazır olmadı! '
                f'MAVROS bağlı mı?'
            )

    def _cmd_arm_cb(self, msg: Bool):
        """
        local_fsm'den gelen ARM/DISARM komutunu uygula.
        msg.data = True  → ARM   (motorlar hazır, uçuşa izin)
        msg.data = False → DISARM (motorlar dur, güvenli park)

        Çağrıldığı state geçişleri:
          STANDBY → IDLE        : ARM=True
          FLYING → DISARM_WAIT  : ARM=False (iniş sonrası)
          REARM state           : ARM=True  (sürüye yeniden katılım)
        """
        if not msg.data:
            self.arm(value=False)
            return

        # ARM=True: GUIDED mod onaylanana kadar bekle
        # (STABILIZE'da ARM → PILOT_OVERRIDE tetikler)
        if self.current_state.mode == 'GUIDED':
            self.arm(value=True)
        else:
            self._arm_pending = True
            self.get_logger().info(
                f'⏳ [{self.ns}] ARM bekleniyor: mod={self.current_state.mode or "?"} → GUIDED onayı bekleniyor'
            )

    def _landing_target_cb(self, msg: PoseStamped):
        """
        precision_landing'den gelen hassas iniş hedefini Pixhawk'a ilet.
        LAND_ZONE state'inde aktif olur.
        Şartname: Tolerans dışı iniş = 0 puan! Bu yüzden hassas iniş kritik.
        """
        self.mavros_setpoint_pub.publish(msg)

    # ══════════════════════════════════════════════════════════════════════
    # PERİYODİK GÖREV
    # ══════════════════════════════════════════════════════════════════════

    def _publish_pilot_override_state(self):
        """
        pilot_override değeri DEĞİŞTİĞİNDE anında yayınla.
        _mavros_state_cb tarafından çağrılır.

        State-triggered yaklaşım:
          - Değer True→False veya False→True olduğunda ANINDA yayınla
          - Wi-Fi'ya gereksiz trafik bindirmez
          - Değişim anında hemen tepki verir (gecikme yok!)
        """
        if self.pilot_override_active != self._last_published_override:
            self._last_published_override = self.pilot_override_active
            msg = Bool()
            msg.data = self.pilot_override_active
            self.pilot_override_pub.publish(msg)

    def _heartbeat_pilot_override(self):
        """
        Her 5 saniyede bir mevcut durumu yayınla (heartbeat).

        NEDEN GEREKLİ?
        Yeni başlayan bir node (örn. local_fsm restart oldu) mevcut
        pilot_override durumunu bilmez. Heartbeat sayesinde en fazla
        5 saniye içinde güncel durumu öğrenir.

        5 sn seçimi:
          - 2 Hz (0.5sn) → 3 drone = 6 mesaj/sn → gereksiz trafik
          - 5 sn         → 3 drone = 0.6 mesaj/sn → kabul edilebilir
        """
        msg = Bool()
        msg.data = self.pilot_override_active
        self.pilot_override_pub.publish(msg)

    # ══════════════════════════════════════════════════════════════════════
    # YARDIMCI FONKSİYONLAR
    # ══════════════════════════════════════════════════════════════════════

    def arm(self, value: bool = True):
        """
        Drone ARM/DISARM et.
        ARM=True  → Motorlar çalışmaya hazır
        ARM=False → Motorlar durur (güvenli)
        Şartname: Tüm drone'lar iniş yapıp DISARM olunca görev tamamdır.
        """
        if self.arming_client.service_is_ready():
            req = CommandBool.Request()
            req.value = value
            action = 'ARM' if value else 'DISARM'
            self.get_logger().info(
                f'🔐 [{self.ns}] {action} komutu gönderiliyor...'
            )
            if value:
                self._arm_in_progress = True  # DISARM false-trigger koruması
            future = self.arming_client.call_async(req)

            # Pixhawk ARM/DISARM isteğini kabul etti mi?
            # Reddederse (örn: öncalibrasyon eksik) logluyoruz.
            def _on_arm_done(f):
                try:
                    result = f.result()
                    if result.success:
                        self.get_logger().info(
                            f'✅ [{self.ns}] {action} başarılı!'
                        )
                        if value:
                            self._arm_in_progress = False
                            self.takeoff()
                    else:
                        self.get_logger().warn(
                            f'⚠️  [{self.ns}] Normal ARM reddedildi, force ARM deneniyor...'
                        )
                        self._arm_in_progress = False
                        self._force_arm(value)
                except Exception as e:
                    self._arm_in_progress = False
                    self.get_logger().error(
                        f'❌ [{self.ns}] arming servis hatası: {e}'
                    )

            future.add_done_callback(_on_arm_done)
        else:
            self.get_logger().warn(f'⚠️  [{self.ns}] arming servisi hazır değil!')

    def _force_arm(self, value: bool = True):
        """Pre-arm check'leri atlayarak force ARM (SITL simülasyon için)."""
        if not self.cmd_client.service_is_ready():
            return
        req = CommandLong.Request()
        req.command = 400  # MAV_CMD_COMPONENT_ARM_DISARM
        req.param1 = 1.0 if value else 0.0
        req.param2 = 21196.0  # ArduPilot force flag
        future = self.cmd_client.call_async(req)

        def _on_force_arm_done(f):
            try:
                r = f.result()
                if r.success:
                    self.get_logger().info(f'✅ [{self.ns}] Force ARM başarılı!')
                    if value:
                        self.takeoff()
                else:
                    self.get_logger().warn(
                        f'⚠️  [{self.ns}] Force ARM başarısız (EKF hazır değil?), '
                        f'10sn sonra tekrar denenecek...'
                    )
                    _t = [None]
                    def _retry_arm():
                        _t[0].cancel()
                        self._force_arm(value)
                    _t[0] = self.create_timer(10.0, _retry_arm)
            except Exception as e:
                self.get_logger().error(f'❌ [{self.ns}] Force ARM hatası: {e}')

        future.add_done_callback(_on_force_arm_done)

    def takeoff(self, _retry: int = 0):
        """
        ARM sonrası kalkış komutu gönder (MAV_CMD_NAV_TAKEOFF).
        ArduCopter ARM'dan sonra ~2 saniye içinde takeoff almazsa auto-disarm yapar.
        Bu metod ARM callback'inden hemen çağrılır.
        """
        if not self.takeoff_client.service_is_ready():
            if _retry < 5:
                self.get_logger().warn(
                    f'⚠️  [{self.ns}] takeoff servisi hazır değil, '
                    f'1sn sonra tekrar denenecek (kalan: {5 - _retry})'
                )
                _t = [None]

                def _retry_cb():
                    _t[0].cancel()
                    self.takeoff(_retry + 1)

                _t[0] = self.create_timer(1.0, _retry_cb)
            else:
                self.get_logger().error(f'❌ [{self.ns}] takeoff servisi 5sn içinde hazır olmadı!')
            return

        req = CommandTOL.Request()
        req.min_pitch = 0.0
        req.yaw = 0.0
        req.latitude = 0.0   # 0 = mevcut konumu kullan
        req.longitude = 0.0
        req.altitude = self.takeoff_altitude

        self.get_logger().info(
            f'🚀 [{self.ns}] KALKIŞ komutu: {self.takeoff_altitude}m'
        )
        future = self.takeoff_client.call_async(req)

        def _on_takeoff_done(f):
            try:
                r = f.result()
                if r.success:
                    self.get_logger().info(
                        f'✅ [{self.ns}] Kalkış komutu kabul edildi! '
                        f'Hedef: {self.takeoff_altitude}m'
                    )
                else:
                    self.get_logger().error(
                        f'❌ [{self.ns}] Kalkış komutu reddedildi! '
                        f'(result={r.result})'
                    )
            except Exception as e:
                self.get_logger().error(
                    f'❌ [{self.ns}] takeoff servis hatası: {e}'
                )

        future.add_done_callback(_on_takeoff_done)


    # ══════════════════════════════════════════════════════════════════════
    # UWB — NOOPLOOP LINKTRACK P-A (GPS-DENIED KONUMLAMA)
    # ══════════════════════════════════════════════════════════════════════
    #
    # Nooploop Nodeframe0 binary protokolü (32 bayt sabit uzunluk):
    #   [0]     0x55        Başlık
    #   [1]     0x00        Fonksiyon işareti (nodeframe0)
    #   [2]     0x20        Çerçeve uzunluğu (32)
    #   [3]     role        0=tag, 1=anchor
    #   [4]     id          Node kimliği
    #   [5-6]   sys_time    Sistem zamanı (ms, uint16 LE)
    #   [7-10]  pos_x       ENU X (metre, float32 LE)
    #   [11-14] pos_y       ENU Y (metre, float32 LE)
    #   [15-18] pos_z       ENU Z (metre, float32 LE)
    #   [19-22] vel_x       Hız X (m/s, float32 LE)
    #   [23-26] vel_y       Hız Y (m/s, float32 LE)
    #   [27-30] vel_z       Hız Z (m/s, float32 LE)
    #   [31]    checksum    Bayt toplamı mod 256
    #
    _NLINK_HEADER1    = 0x55
    _NLINK_NODEFRAME0 = 0x00
    _NLINK_FRAME_LEN  = 32

    def _uwb_reader_thread(self):
        """
        Nooploop seri port okuyucu — arka planda çalışır, ROS2 spin'i bloklamaz.
        Bağlantı kesilirse 2 saniye bekleyip otomatik yeniden bağlanır.
        """
        import time
        while rclpy.ok():
            try:
                ser = serial.Serial(self._uwb_port, baudrate=921600, timeout=1.0)
                self.get_logger().info(
                    f'✅ [{self.ns}] UWB seri port açıldı: {self._uwb_port}'
                )
                buf = bytearray()
                while rclpy.ok():
                    chunk = ser.read(64)
                    if not chunk:
                        continue
                    buf.extend(chunk)
                    # Tampon içinde tam çerçeve ara
                    while len(buf) >= self._NLINK_FRAME_LEN:
                        idx = buf.find(self._NLINK_HEADER1)
                        if idx == -1:
                            buf.clear()
                            break
                        if idx > 0:
                            del buf[:idx]   # Başlığa kadar çöp temizle
                        if len(buf) < self._NLINK_FRAME_LEN:
                            break           # Tam çerçeve henüz gelmedi
                        frame = bytes(buf[:self._NLINK_FRAME_LEN])
                        # Checksum doğrula: ilk 31 baytın toplamı mod 256
                        if sum(frame[:-1]) & 0xFF != frame[-1]:
                            del buf[:1]     # Yanlış çerçeve, 1 bayt at ve tekrar dene
                            continue
                        if frame[1] == self._NLINK_NODEFRAME0:
                            self._parse_nlink_nodeframe0(frame)
                        del buf[:self._NLINK_FRAME_LEN]
            except serial.SerialException as e:
                self.get_logger().warn(
                    f'⚠️  [{self.ns}] UWB seri port hatası: {e} — 2sn sonra tekrar denenecek'
                )
                time.sleep(2.0)
            except Exception as e:
                self.get_logger().error(f'❌ [{self.ns}] UWB okuma hatası: {e}')
                time.sleep(2.0)

    def _parse_nlink_nodeframe0(self, frame: bytes):
        """
        Nodeframe0 çerçevesini ayrıştır.
        Sürü ortamında birden fazla drone'un verisi aynı UWB ağından geçebilir;
        bu yüzden sadece kendi drone_id'mize ait paketi işliyoruz.
        """
        node_id = frame[4]
        if node_id != self.drone_id:
            return  # Başka drone'a ait paket, atla

        pos_x = struct.unpack_from('<f', frame, 7)[0]   # ENU X (metre)
        pos_y = struct.unpack_from('<f', frame, 11)[0]  # ENU Y (metre)
        pos_z = struct.unpack_from('<f', frame, 15)[0]  # ENU Z (metre)

        # Geçersiz değerleri filtrele (NaN, Inf, makul alan dışı)
        if not all(-1000.0 < v < 1000.0 for v in (pos_x, pos_y, pos_z)):
            return

        msg = PoseStamped()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = pos_x
        msg.pose.position.y = pos_y
        msg.pose.position.z = pos_z
        msg.pose.orientation.w = 1.0   # Yaw bilinmiyor → nötr quaternion
        self._uwb_pose_pub.publish(msg)


# ══════════════════════════════════════════════════════════════════════════
# ANA FONKSİYON
# ══════════════════════════════════════════════════════════════════════════

def main(args=None):
    """
    Node başlatma.

    TEST ETME:
    ----------
    1) Simülasyon çalışıyorken (Gazebo + SITL + MAVROS açıkken):
       ros2 run my_swarm_pkg drone_interface --ros-args -p drone_id:=1

    2) Topic'leri kontrol et (başka terminalde):
       ros2 topic echo /drone1/pose
       ros2 topic echo /drone1/pilot_override
       ros2 topic list | grep drone1

    3) Konum geliyor mu?
       ros2 topic hz /drone1/pose   (→ yaklaşık 20 Hz olmalı)
    """
    rclpy.init(args=args)
    node = DroneInterface()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info(f'⛔ drone_interface durduruluyor...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
