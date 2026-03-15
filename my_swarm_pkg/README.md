# TEKNOFEST 2026 — Swarm UAV Paketi (my_swarm_pkg)

> **ROS2 Humble + ArduPilot SITL + Gazebo 8**
> 3 drone'lu dağıtık otonom sürü — QR navigasyon, formasyon kontrolü, hassas iniş

---

## İçindekiler

1. [Proje Genel Bakış](#1-proje-genel-bakış)
2. [Mimari](#2-mimari)
3. [Dizin Yapısı](#3-dizin-yapısı)
4. [Bağımlılıklar ve Kurulum](#4-bağımlılıklar-ve-kurulum)
5. [Simülasyonu Başlatma](#5-simülasyonu-başlatma)
6. [Dashboard Kullanımı (mission_fsm)](#6-dashboard-kullanımı-mission_fsm)
7. [Node'lar — Detaylı Açıklama](#7-nodelar--detaylı-açıklama)
8. [Topic ve Mesaj Haritası](#8-topic-ve-mesaj-haritası)
9. [Özel Mesajlar (swarm_msgs)](#9-özel-mesajlar-swarm_msgs)
10. [Görev Akışı (TASK1)](#10-görev-akışı-task1)
11. [Durum Makineleri](#11-durum-makineleri)
12. [Formasyon Tipleri](#12-formasyon-tipleri)
13. [QR Haritası (qr_map.yaml)](#13-qr-haritası-qr_mapyaml)
14. [Launch Konfigürasyonu](#14-launch-konfigürasyonu)
15. [Güvenlik ve Sınırlar](#15-güvenlik-ve-sınırlar)
16. [Bilinen Eksiklikler / Yapılacaklar](#16-bilinen-eksiklikler--yapılacaklar)

---

## 1. Proje Genel Bakış

Bu paket TEKNOFEST 2026 Sürü İHA yarışması için geliştirilmiştir. Üç ArduCopter drone'u:

- **Bully algoritmasıyla** merkezi koordinatör seçer (lider seçimi)
- **Lider, 2 Hz SwarmIntent yayınlar** → tüm dronlar aynı komutu alır
- **QR waypoint rotasını** (1→2→3→4→5→6→HOME) takip eder
- QR kodlarından okunan formasyona ve irtifaya uyum sağlar
- QR3'te bir drone ayrılarak renk bölgesine (RED/BLUE/GREEN) hassas iner
- GCS bağlantısı kesilse bile sürü otonom devam eder (§5.3)

```
Yarışma Günü Prosedürü:
  1. mission_fsm aç → [h] ile irtifa gir (jüri söyler)
  2. [m] ile QR koordinatları gir (jüri söyler)
  3. [s] → 3 drone arm + kalkış + QR rotası
```

---

## 2. Mimari

```
                       ┌─────────────────────────────────────────┐
                       │          GCS (Yer İstasyonu)            │
                       │           mission_fsm.py                │
                       │  [s] start  [a] abort  [h] irtifa       │
                       │  [m] QR koordinat  [d] durum            │
                       └──────────────┬──────────────────────────┘
                                      │ /swarm/task_trigger
                                      │ /gcs/drone_altitude
                     ┌────────────────▼───────────────────────┐
                     │          SWARM (Her drone'da çalışır)   │
                     │                                         │
   /swarm/intent ←───┤  intent_coordinator  (Lider seçer)     │
   (SwarmIntent)     │  ↑ Bully: min(FLYING drone ID) = Lider │
                     └──────────────┬──────────────────────────┘
                                    │
          ┌────────────────┬─────────┴──────────────┐
          │                │                         │
   ┌──────▼──────┐  ┌──────▼──────┐         ┌──────▼──────┐
   │   drone1    │  │   drone2    │         │   drone3    │
   │             │  │             │         │             │
   │ local_fsm   │  │ local_fsm   │         │ local_fsm   │
   │ formation_  │  │ formation_  │         │ formation_  │
   │ controller  │  │ controller  │         │ controller  │
   │ collision_  │  │ collision_  │         │ collision_  │
   │ avoidance   │  │ avoidance   │         │ avoidance   │
   │ drone_iface │  │ drone_iface │         │ drone_iface │
   │ waypoint_   │  │ waypoint_   │         │ waypoint_   │
   │ navigator   │  │ navigator   │         │ navigator   │
   │ precision_  │  │ precision_  │         │ precision_  │
   │ landing     │  │ landing     │         │ landing     │
   │ safety_mon  │  │ safety_mon  │         │ safety_mon  │
   │             │  │             │         │ qr_percep.  │ ← onboard kamera drone
   └──────┬──────┘  └──────┬──────┘         └──────┬──────┘
          │                │                         │
   ┌──────▼──────┐  ┌──────▼──────┐         ┌──────▼──────┐
   │  MAVROS     │  │  MAVROS     │         │  MAVROS     │
   │  (UDP:14550)│  │  (UDP:14560)│         │  (UDP:14570)│
   └──────┬──────┘  └──────┬──────┘         └──────┬──────┘
          │                │                         │
   ┌──────▼──────┐  ┌──────▼──────┐         ┌──────▼──────┐
   │ ArduCopter  │  │ ArduCopter  │         │ ArduCopter  │
   │ SITL -I0    │  │ SITL -I1    │         │ SITL -I2    │
   │ JSON:9002   │  │ JSON:9012   │         │ JSON:9022   │
   └──────┬──────┘  └──────┬──────┘         └──────┬──────┘
          └────────────────┴──────────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │     Gazebo 8       │
                          │  ArduPilotPlugin   │
                          │  Drone1+2+3 model  │
                          │  QR Marker 1-6     │
                          └───────────────────┘
```

### Veri Akışı — Setpoint Zinciri

```
formation_controller
    ↓ /{ns}/setpoint_raw  (istenen pozisyon)
collision_avoidance (APF düzeltmesi)
    ↓ /{ns}/setpoint_final
drone_interface
    ↓ /{ns}/mavros/setpoint_position/local
MAVROS → ArduPilot → Gazebo fizik motoru

(DETACH fazında precision_landing aynı zincirin üstüne /{ns}/landing_target yazar
 ve 10 Hz yayın hızıyla formation_controller'ı ezer)
```

---

## 3. Dizin Yapısı

```
gz_ws/
├── src/
│   ├── my_swarm_pkg/
│   │   ├── my_swarm_pkg/          ← Python node dosyaları
│   │   │   ├── __init__.py
│   │   │   ├── drone_interface.py
│   │   │   ├── local_fsm.py
│   │   │   ├── intent_coordinator.py
│   │   │   ├── formation_controller.py
│   │   │   ├── collision_avoidance.py
│   │   │   ├── safety_monitor.py
│   │   │   ├── qr_perception.py
│   │   │   ├── waypoint_navigator.py
│   │   │   ├── precision_landing.py
│   │   │   └── mission_fsm.py
│   │   ├── launch/
│   │   │   └── swarm_competition.launch.py
│   │   ├── config/
│   │   │   ├── qr_map.yaml          ← QR waypoint haritası
│   │   │   └── cyclonedds_localhost.xml
│   │   ├── worlds/
│   │   │   └── world_task1_qr_static.sdf
│   │   ├── resource/
│   │   ├── package.xml
│   │   ├── setup.cfg
│   │   └── setup.py
│   ├── swarm_msgs/
│   │   ├── msg/
│   │   │   ├── SwarmIntent.msg
│   │   │   ├── LocalState.msg
│   │   │   ├── QRResult.msg
│   │   │   ├── FormationCmd.msg
│   │   │   ├── ColorZone.msg
│   │   │   ├── ColorZoneList.msg
│   │   │   ├── SafetyEvent.msg
│   │   │   ├── JoinRequest.msg
│   │   │   └── TaskTrigger.msg
│   │   └── srv/
│   │       └── SetQRMap.srv
│   └── ardupilot_gazebo/
│       └── models/
│           ├── Drone1/   Drone2/   Drone3/
│           └── qr_marker_1/ ... qr_marker_6/
└── install/   build/   log/
```

---

## 4. Bağımlılıklar ve Kurulum

> **Arkadaşa Not:** Bu bölüm Ubuntu 22.04 temiz kurulum üzerine sıfırdan kurulum adımlarını içerir. Her adımı sırayla uygula, atlamadan.

### Sistem Gereksinimleri
- Ubuntu 22.04 LTS (Jammy)
- ROS2 Humble
- Gazebo 8 (gz-sim8)
- ArduPilot SITL (`~/ardupilot/`)
- ardupilot_gazebo plugin (`~/gz_ws/src/ardupilot_gazebo/`)
- MAVROS (ROS2 için)
- Python 3.10+

---

### ADIM 1 — ROS2 Humble Kurulumu

```bash
# Locale ayarla
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# ROS2 apt repository ekle
sudo apt install -y software-properties-common curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# ROS2 Humble Desktop tam kurulum
sudo apt update
sudo apt install -y ros-humble-desktop

# Geliştirme araçları
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool

# rosdep init (bir kez)
sudo rosdep init
rosdep update

# Her yeni terminalde ROS2'yi source et
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### ADIM 2 — Gazebo 8 (gz-sim8) Kurulumu

```bash
# Gazebo apt repository ekle
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt update
sudo apt install -y gz-garden   # gz-sim8 içerir

# Kurulumu doğrula
gz sim --version   # "8.x.x" görmeli
```

---

### ADIM 3 — MAVROS Kurulumu (ROS2 Humble için)

```bash
sudo apt install -y ros-humble-mavros ros-humble-mavros-extras

# GeographicLib verilerini indir (MAVROS için zorunlu)
sudo /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh
```

---

### ADIM 4 — ArduPilot SITL Kurulumu

```bash
# ArduPilot kaynak kodunu indir
cd ~
git clone https://github.com/ArduPilot/ardupilot.git --recurse-submodules
cd ardupilot

# Bağımlılıkları kur (Ubuntu 22.04)
Tools/environment_install/install-prereqs-ubuntu.sh -y

# Profili yenile
. ~/.profile   # ya da terminali kapatıp aç

# ArduCopter SITL binary derle
./waf configure --board sitl
./waf copter

# Derleme başarıyla bitti mi kontrol et:
ls ~/ardupilot/build/sitl/bin/arducopter
# → dosya varsa başarılı

# Varsayılan parametreleri doğrula:
ls ~/ardupilot/Tools/autotest/default_params/copter.parm
```

---

### ADIM 5 — ardupilot_gazebo Plugin Kurulumu

```bash
# Workspace oluştur
mkdir -p ~/gz_ws/src
cd ~/gz_ws/src

# ardupilot_gazebo plugin indir
git clone https://github.com/ArduPilot/ardupilot_gazebo.git

# Build et
cd ~/gz_ws
colcon build --packages-select ardupilot_gazebo

# Kurulumu doğrula:
ls ~/gz_ws/install/ardupilot_gazebo/lib/  # *.so dosyaları görmeli
```

---

### ADIM 6 — Swarm Paketlerini Kur (Bu Repo)

```bash
cd ~/gz_ws/src

# Bu repoyu clone'la (swarm_msgs dahil)
git clone https://github.com/KULLANICI_ADI/REPO_ADI.git .
# NOT: Nokta (.) mevcut klasöre clone'lar

# VEYA eğer klasör zaten varsa:
git clone https://github.com/KULLANICI_ADI/REPO_ADI.git temp
mv temp/* .
rm -rf temp

# Bağımlılıkları çek
cd ~/gz_ws
rosdep install --from-paths src --ignore-src -r -y

# Build et (tüm paketler)
colcon build

# Başarı kontrolü:
ls install/my_swarm_pkg/lib/my_swarm_pkg/
# → mission_fsm, intent_coordinator, drone_interface, ... görünmeli
```

---

### ADIM 7 — ~/.bashrc Ayarları

Aşağıdaki satırları `~/.bashrc` dosyasına ekle (en alta):

```bash
# ROS2 Humble
source /opt/ros/humble/setup.bash

# Workspace
source ~/gz_ws/install/setup.bash

# Gazebo
export GZ_SIM_RESOURCE_PATH="$HOME/gz_ws/src/my_swarm_pkg/models:$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/install/ardupilot_gazebo/share/ardupilot_gazebo/models:/usr/share/gz/gz-sim8/models"

# ROS_LOCALHOST_ONLY (tek makinede DDS)
export ROS_LOCALHOST_ONLY=1
```

Ekledikten sonra uygula:
```bash
source ~/.bashrc
```

---

### ADIM 8 — Kurulumu Doğrula

Her şeyin çalıştığını kontrol etmek için:

```bash
# ROS2
ros2 --version   # "ros2 1.3.x" görmeli

# Gazebo
gz sim --version  # "8.x.x" görmeli

# MAVROS
ros2 pkg list | grep mavros   # "mavros" görmeli

# ArduCopter
~/ardupilot/build/sitl/bin/arducopter --version  # versiyon görmeli

# Swarm paketleri
ros2 pkg list | grep -E "my_swarm|swarm_msgs"  # iki paket görmeli
```

---

### Sadece my_swarm_pkg Değiştiyse

```bash
cd ~/gz_ws
colcon build --packages-select my_swarm_pkg
source install/setup.bash
```

### Tüm Workspace Rebuild

```bash
cd ~/gz_ws
colcon build
source install/setup.bash
```

---

## 5. Simülasyonu Başlatma

```bash
cd ~/gz_ws
source install/setup.bash
DISPLAY=:0 ros2 launch my_swarm_pkg swarm_competition.launch.py
```

**Ne açılır:**
1. Gazebo penceresi (Drone1-3 + QR Marker 1-6)
2. 3× ArduCopter SITL (arka planda, log'a yazıyor)
3. 3× MAVROS bağlantısı
4. Tüm swarm node'ları (her drone için 9 node)
5. **"Mission FSM Dashboard"** başlıklı xterm penceresi

**Başlangıç sırası (sn cinsinden):**
| Zaman | Olay |
|-------|------|
| 0s | Gazebo başlar |
| 0s | ArduCopter drone1 başlar |
| 2s | ArduCopter drone2 başlar |
| 4s | ArduCopter drone3 başlar |
| 8s | 3× MAVROS başlar |
| 9.0s | drone1 node'ları başlar |
| 9.5s | drone2 node'ları başlar |
| 10.0s | drone3 node'ları başlar |
| 10.5s | qr_perception başlar |
| 10.7s | mission_fsm Dashboard açılır |

---

## 6. Dashboard Kullanımı (mission_fsm)

Dashboard xterm penceresinde **sadece klavye ile** kontrol edilir. **Fare çalışmaz.**

### Komutlar

| Komut | Açıklama |
|-------|----------|
| `h` veya `alt` | **Uçuş irtifası gir** — jüri yarışmada söyler (2-100m) |
| `m` veya `map` | **QR koordinatları gir** — jüri yarışmada söyler |
| `s` veya `start` | **Görevi başlat** — 3 drone arm + kalkış + QR rotası |
| `a` veya `abort` | **ACİL DURDUR** — tüm dronlar RTL (eve döner) |
| `d` veya `status` | Mevcut durum ekranını göster |
| `q` veya `quit` | Dashboard'ı kapat |
| Enter | Ekranı yenile |

### Yarışma Günü Sırası

```
1. Dashboard açıldıktan sonra bekle
2. Jüri irtifayı söylediğinde:  h → 15 → Enter
3. Jüri QR koordinatlarını söylediğinde:  m → koordinatları gir
4. Jüri "başla" dediğinde:  s → Enter
5. Drone'lar arm olur, kalkar, QR rotasını takip eder
6. Abortlamak gerekirse:  a → Enter
```

### [m] QR Koordinat Girişi

```
m tuşuna bas →
  QR1: 10 5 0
  QR2: 10 -5 0
  ... gibi  x y z  formatında gir
  Enter ile onayla
```

---

## 7. Node'lar — Detaylı Açıklama

### 7.1 `drone_interface.py`

**Görev:** MAVROS ↔ Swarm ROS2 köprüsü. Her drone kendi instance'ını çalıştırır.

**MAVROS'tan okunanlar → ROS2'ye yayınlananlar:**
| MAVROS Topic | ROS2 Topic | Tip | Açıklama |
|---|---|---|---|
| `/{ns}/mavros/local_position/pose` | `/{ns}/pose` | PoseStamped | Drone konumu (ENU, 20 Hz) |
| `/{ns}/mavros/local_position/velocity_local` | `/{ns}/velocity` | TwistStamped | Hız (ENU) |
| `/{ns}/mavros/state` | — | State | Arm/mod takibi, PILOT_OVERRIDE tespiti |

**ROS2'den okunanlar → MAVROS'a yazılanlar:**
| ROS2 Topic | MAVROS Hedef | Açıklama |
|---|---|---|
| `/{ns}/setpoint_final` | `/{ns}/mavros/setpoint_position/local` | collision_avoidance'dan gelen son setpoint |
| `/{ns}/landing_target` | `/{ns}/mavros/setpoint_position/local` | precision_landing override (10 Hz → formation_controller'ı ezer) |
| `/{ns}/cmd_mode` | `/{ns}/mavros/set_mode` | GUIDED / LAND / RTL / BRAKE |
| `/{ns}/cmd_arm` | `/{ns}/mavros/cmd/arming` | ARM / DISARM |

**PILOT_OVERRIDE tespiti:**
- Drone arm + mod ∉ {GUIDED, LAND, RTL, BRAKE, AUTO} → `/{ns}/pilot_override = True`

---

### 7.2 `local_fsm.py`

**Görev:** Her drone'un kendi durum makinesi. `intent_coordinator`'dan gelen SwarmIntent'i işler, `drone_interface`'e komut gönderir.

**Çift Filtre (Eski lider paketlerini engeller):**
- `seq <= son_görülen_seq` → DROP
- `timestamp < son_görülen_timestamp (aynı seq'de)` → DROP

**Yayınladığı / Dinlediği Topic'ler:**
| Topic | Tip | Yön | Açıklama |
|---|---|---|---|
| `/swarm/intent` | SwarmIntent | Dinler | Görev komutları |
| `/{ns}/local_state` | LocalState | **Yayınlar** (10 Hz) | Kendi durumu (heartbeat) |
| `/safety/event` | SafetyEvent | Dinler | Güvenlik olayı → SAFETY_HOLD |
| `/{ns}/pilot_override` | Bool | Dinler | RC müdahalesi → PILOT_OVERRIDE |
| `/{ns}/cmd_mode` | String | **Yayınlar** | Mod komutu drone_interface'e |
| `/{ns}/cmd_arm` | Bool | **Yayınlar** | ARM/DISARM komutu |
| `/{ns}/pose` | PoseStamped | Dinler | Kendi konumu (irtifa kontrolü için) |
| `/perception/color_zones` | ColorZoneList | Dinler | DETACH fazında hedef zone |

---

### 7.3 `intent_coordinator.py`

**Görev:** Sürünün "ne yapacağına" karar veren lider mantığı. Her drone'da çalışır, sadece lider `/swarm/intent` yazar.

**Lider Seçimi (Bully):**
- Tüm drone'lar `/drone{i}/local_state` dinler (heartbeat: 600ms timeout)
- FLYING veya REJOIN drone'lar arasından `min(drone_id)` = lider
- ARMING fazında (kimse FLYING değil): STANDBY/IDLE arasından `min(id)`
- Tüm drone'lar aynı hesaplamayı yapar → aynı lider → merkezi koordinasyon gerekmez

**Seq Sürekliliği:**
- Yeni lider olunca `_my_intent_seq = global_last_seq + 1`
- Böylece local_fsm'in çift filtresi yeni lider paketlerini DROP etmez

**MissionPhase Durumları:**
```
IDLE       → görev başlamadı
ARMING     → dronlar ARM edilmekte (IDLE intent)
NAVIGATING → QR waypoint'e gidilmekte (QR_NAVIGATE intent)
AT_QR      → QR noktasında (loiter/işlem)
DETACHING  → drone ayrılmakta (DETACH intent)
REJOINING  → yedek drone katılmakta (REJOIN intent)
RETURNING  → tüm QR bitti, eve dönüş (RETURN_HOME intent)
COMPLETE   → görev tamamlandı
```

**ARMING → NAVIGATING Geçişi:**
- Tüm drone'lar IDLE (arm edildi) → lider phase'i NAVIGATING'e çeker
- QR1 konumu başlangıçta `qr_map.yaml`'dan yüklenir

**QR Haritası Ön-Yüklemesi:**
- Startup'ta `qr_map.yaml` okunur → `_qr_map_nodes` doldurulur
- `task_trigger` gelince QR1 konumu anında hazır

**Key Topic'ler:**
| Topic | Tip | Yön | Açıklama |
|---|---|---|---|
| `/swarm/intent` | SwarmIntent | **Yayınlar** (2 Hz, sadece lider) | Görev komutları |
| `/drone{i}/local_state` | LocalState | Dinler | Heartbeat + state takibi |
| `/swarm/task_trigger` | TaskTrigger | Dinler | GCS'den görev başlat/durdur |
| `/swarm/qr_map_ready` | Bool | Dinler | qr_perception hazır sinyali |
| `/gcs/drone_altitude` | Float64 | Dinler | Jüri irtifa komutu |
| `/qr/result` | QRResult | Dinler | QR içerik parse (sadece lider) |
| `/swarm/leader_id` | UInt8 | **Yayınlar** (5 Hz) | Mevcut lider ID'si |

---

### 7.4 `formation_controller.py`

**Görev:** Sanal yapı (virtual structure) ile formasyon geometrisi hesaplar. `/{ns}/setpoint_raw` yayınlar.

**Virtual Leader (Sanal Lider) Navigasyonu [v3]:**
- Hedef: `intent.target_pos`
- Hız: `VIRTUAL_LEADER_SPEED_MPS = 3.0 m/s`
- Varış: `ARRIVAL_RADIUS_M = 0.3m` içinde → sabit bekler
- Tüm dronlar aynı sanal lideri takip eder → formasyon dağılmaz

**Slew Rate Limiting:**
- Normal: 0.10 m/adım @ 50 Hz = 5 m/s² max ivme
- Titreşim sonrası (dampened): 0.02 m/adım (8 saniye sürer)

**Rank Sistemi (Formasyon sıralaması):**
- Dronlar ID sırasına göre FLYING olanlar arasından rank alır
- Rank değişiminde 30 döngü (0.6s) geçiş koruması

**Kontrol Döngüsü: 50 Hz**

**Aktif Olduğu State'ler:** `FLYING`, `REJOIN`

**Teleop Modu (TASK2):**
- `/swarm/teleop_mode` (IDLE/MOVE/MANEUVER) dinler
- MOVE: `vx/vy/vz/yaw_rate` → sanal lider kinematik entegrasyon
- MANEUVER: formasyon tipi/aralığı değiştirir, sanal lider sabit

---

### 7.5 `collision_avoidance.py`

**Görev:** APF (Yapay Potansiyel Alan) algoritması ile drone'lar arası çarpışmayı engeller.

**APF Formülü:**
```
F_j = K_REP * (1/d - 1/R_MAX) / d²    [d < R_MAX ise]

TTC varsa amplify:
  Kapanma hızı hesapla (v_rel · ĝ)
  TTC < 1.5s → kuvveti 3x büyüt

setpoint_final = setpoint_raw + clip(ΣF_j, 3.0m)
```

**Parametreler:**
| Parametre | Değer | Açıklama |
|---|---|---|
| R_MAX | 8.0 m | İtme kuvvetinin başladığı mesafe |
| R_MIN | 3.0 m | Tam kuvvet mesafesi |
| K_REP | 18.0 | İtme kazancı |
| MAX_CORR_M | 3.0 m | Maksimum düzeltme vektörü |
| TTC_THRESHOLD | 1.5 s | Zaman-çarpışmaya kuvvet amplifikasyonu |
| TTC_AMPLIFY | 3.0× | Hızlı yaklaşmada kuvvet çarpanı |

**Titreşim Tespiti:**
- 20 örneklik (0.4s) pencerede XY setpoint varyansı
- Eşik: 0.08 m → `SafetyEvent('OSCILLATION')` gönderir
- Cooldown: 5 saniye
- → formation_controller dampening moduna girer

**Kontrol Döngüsü: 50 Hz**

---

### 7.6 `safety_monitor.py`

**Görev:** Batarya, jeofence ve heartbeat izleme. Tehlike durumunda `SafetyEvent` yayınlar.

**Mock Batarya (Simülasyon):**
- Başlangıç: %100
- Tüketim hızı: 0.01 %/s → %15'e ulaşma süresi ~141 dakika
- Uyarı eşiği: %25 (log uyarısı)
- Kritik eşik: %15 → `SafetyEvent(BATTERY_CRITICAL)`
- Event cooldown: 30 saniye

**Jeofence (ENU koordinatları, env vars'dan):**
| Sınır | Env Var | Varsayılan |
|---|---|---|
| X min | FENCE_X_MIN | -5.0 m |
| X max | FENCE_X_MAX | 125.0 m |
| Y min | FENCE_Y_MIN | -5.0 m |
| Y max | FENCE_Y_MAX | 95.0 m |
| Z min | FENCE_ALT_MIN | 0.5 m |
| Z max | FENCE_ALT_MAX | 60.0 m |

- Sınıra 3m yaklaşınca log uyarısı
- Sınırı geçince: `SafetyEvent(GEOFENCE_BREACH)`
- Event cooldown: 5 saniye

**İzleme Döngüsü: 5 Hz**

---

### 7.7 `qr_perception.py`

**Görev:** QR tespit simülasyonu. Kamera drone'u QR marker yakınına girince YAML içeriğini okuyarak `QRResult` yayınlar.

**Tespit Mekanizması (Proximity-based):**
> **Not:** Gerçek drone'larda bu kısım OpenCV + kamera topic ile değiştirilmelidir.
> Simülasyonda: kamera drone konumu + QR marker konumu arasındaki mesafe < trigger_radius → "QR okundu"

- **trigger_radius:** 5.0 m (qr_map.yaml'dan)
- **Kamera drone:** drone3 (varsayılan)
- **Yedek kamera:** drone2

**Kamera Failover:**
- drone3 state ∈ {DETACH, SAFETY_HOLD, PILOT_OVERRIDE} → drone2 kamera görevi alır
- Her iki drone da aynı `/qr/result` topic'ine yazar

**QRResult İçeriği (Şekil 2 JSON formatından parse):**
- Formasyon tipi + aralık
- İrtifa değişimi
- Manevra (pitch/roll açıları)
- Detach komutu (drone ID + hedef renk)
- Sonraki QR ID

**Runtime QR Güncelleme:**
- `/swarm/set_qr_map` servisi → jüri koordinatları → iç harita güncellenir
- Güncelleme sonrası `/swarm/qr_map_ready = True` yayınlanır

**Startup:**
- YAML otomatik yüklenir → 2 saniye sonra `qr_map_ready = True` sinyali gönderilir
- (intent_coordinator task_trigger'ı bu sinyali bekler)

**Topic'ler:**
| Topic | Tip | Açıklama |
|---|---|---|
| `/qr/result` | QRResult | QR içeriği yayını |
| `/perception/color_zones` | ColorZoneList | 1 Hz renk zone listesi |
| `/swarm/qr_map_ready` | Bool | Harita hazır sinyali |
| `/swarm/set_qr_map` | Servis SetQRMap | Runtime harita güncelleme |

---

### 7.8 `waypoint_navigator.py`

**Görev:** QR waypoint'lere navigasyonu yönetir. Sadece lider drone'da aktif çalışır.

**Navigasyon Fazları:**
```
IDLE        → görev başlamadı
NAVIGATING  → hedefe tam hızla gidiliyor
APPROACHING → 20m içinde (debug log)
LOITERING   → QR noktasında hover + QR okuma tetiklendi
WAITING     → loiter süresi dolmayı bekliyor
HOME_RETURN → tüm QR bitti, eve dönüş
COMPLETE    → eve ulaşıldı
```

**Loiter Mantığı (QR'da bekleme):**
1. `centroid ↔ hedef` mesafesi < 5m → loiter başlar
2. `/swarm/loiter_cmd = True` → formation_controller setpoint'i dondurur
3. QR sonucu bekler (varsayılan 3s, QR'dan gelen `wait_seconds` ile override)
4. `/swarm/loiter_cmd = False` → navigasyon devam eder

**Parametreler:**
| Parametre | Değer |
|---|---|
| LOITER_RADIUS_M | 5.0 m |
| APPROACH_RADIUS_M | 20.0 m |
| DEFAULT_LOITER_S | 3.0 s |
| QR_TRIGGER_COOLDOWN_S | 10.0 s |
| Kontrol Hz | 10 Hz |

**Home Koordinatları:** `HOME_X, HOME_Y, HOME_Z` env vars'dan (varsayılan: 0, 0, 5m)

---

### 7.9 `precision_landing.py`

**Görev:** DETACH drone'unu renk zone'unun tam merkezine getirerek hassas iniş yapar.

**Aktivasyon:**
- `/swarm/intent.task_id == 'DETACH'` VE `intent.detach_drone_id == kendi_id`
- `/{ns}/local_state ∈ {DETACH, LAND_ZONE}` → aktif

**Çalışma Prensibi:**
```
1. intent'ten zone_color oku ("RED"/"BLUE"/"GREEN")
2. /perception/color_zones'dan eşleşen zone konumunu bul
3. /{ns}/landing_target = (zone_x, zone_y, HOVER_ALT_M=5.0) yayınla @ 10 Hz
4. drone_interface → MAVROS (formation_controller'ı override eder, 10 Hz > 50 Hz kazanır)
5. XY hata < 0.8m → "hizalandı" logu
6. local_fsm LAND_ZONE'dan iniş komutunu verir
7. State DISARM_WAIT'e geçince precision_landing durur
```

**Parametreler:**
| Parametre | Değer |
|---|---|
| HOVER_ALT_M | 5.0 m |
| XY_PRECISE_M | 0.8 m |
| ZONE_STALE_S | 3.0 s |
| Kontrol Hz | 10 Hz |

---

### 7.10 `mission_fsm.py`

**Görev:** GCS (yer istasyonu) arayüzü. Laptop/terminal'den çalışır. Görev başlatma/durdurma + durum izleme.

**GCS Durum Makinesi:**
```
STANDBY → TASK1_SENT → TASK1_ACTIVE → ABORT_SENT → COMPLETE
```

**Yayınladığı Topic'ler:**
| Topic | Tip | Açıklama |
|---|---|---|
| `/swarm/task_trigger` | TaskTrigger | Görev başlat/durdur |
| `/swarm/gcs_heartbeat` | String | GCS aktiflik sinyali (2 Hz) |
| `/gcs/drone_altitude` | Float64 | Jüri tarafından belirlenen irtifa |

**SetQRMap Servisi:**
- `/swarm/set_qr_map` → qr_perception'a jüri koordinatlarını iletir

---

## 8. Topic ve Mesaj Haritası

### Tüm Node'ların Tam Topic Listesi

```
SWARM BÜS (tüm drone'lar dinler/yazar):
  /swarm/intent          SwarmIntent   ← Lider (2 Hz)
  /swarm/leader_id       UInt8         ← Lider (5 Hz)
  /swarm/gcs_heartbeat   String        ← mission_fsm (2 Hz)
  /swarm/task_trigger    TaskTrigger   ← mission_fsm
  /swarm/qr_map_ready    Bool          ← qr_perception (startup + SetQRMap)
  /swarm/loiter_cmd      Bool          ← waypoint_navigator
  /swarm/join_request    JoinRequest   ← STANDBY dronlar
  /swarm/virtual_leader  PoseStamped   ← formation_controller (lider)
  /safety/event          SafetyEvent   ← safety_monitor, collision_avoidance
  /qr/result             QRResult      ← qr_perception
  /perception/color_zones ColorZoneList← qr_perception (1 Hz)
  /gcs/drone_altitude    Float64       ← mission_fsm

PER-DRONE TOPIC'LER (ns = drone1 / drone2 / drone3):
  /{ns}/pose             PoseStamped   ← drone_interface (20 Hz)
  /{ns}/velocity         TwistStamped  ← drone_interface
  /{ns}/local_state      LocalState    ← local_fsm (10 Hz)
  /{ns}/pilot_override   Bool          ← drone_interface
  /{ns}/setpoint_raw     PoseStamped   ← formation_controller (50 Hz)
  /{ns}/setpoint_final   PoseStamped   ← collision_avoidance (50 Hz)
  /{ns}/landing_target   PoseStamped   ← precision_landing (10 Hz)
  /{ns}/cmd_mode         String        ← local_fsm
  /{ns}/cmd_arm          Bool          ← local_fsm

MAVROS (dahili):
  /{ns}/mavros/local_position/pose
  /{ns}/mavros/local_position/velocity_local
  /{ns}/mavros/state
  /{ns}/mavros/setpoint_position/local
  /{ns}/mavros/set_mode  (servis)
  /{ns}/mavros/cmd/arming (servis)
```

---

## 9. Özel Mesajlar (swarm_msgs)

### SwarmIntent.msg
```
std_msgs/Header header
uint32  seq                 # Monoton artan, çift filtre için kritik
uint8   leader_id           # Yayınlayan drone ID
string  task_id             # IDLE | QR_NAVIGATE | MANEUVER | DETACH | REJOIN | RETURN_HOME
string  formation_type      # OKBASI | V | CIZGI
float32 drone_spacing       # metre cinsinden drone aralığı
float32 target_yaw          # radian, ENU (x-east = 0)
geometry_msgs/Point target_pos  # QR hedef konumu
float32 drone_altitude      # uçuş irtifası (m)
uint8   detach_drone_id     # ayrılacak drone ID (0 = yok)
string  zone_color          # RED | BLUE | GREEN
bool    maneuver_active     # pitch/roll manevrası aktif mi
float32 maneuver_pitch_deg
float32 maneuver_roll_deg
uint8   active_drone_count  # sürüdeki aktif drone sayısı
uint8   join_drone_id       # katılan drone ID (0 = yok)
uint32  qr_seq              # son işlenen QR ID
builtin_interfaces/Time wait_until
```

### LocalState.msg
```
std_msgs/Header header
uint8  drone_id
string state    # STANDBY | IDLE | FLYING | DETACH | LAND_ZONE |
                # DISARM_WAIT | REARM | REJOIN | RETURN_HOME |
                # LANDING | SAFETY_HOLD | PILOT_OVERRIDE
uint32 seq      # Monoton artan (heartbeat + çift filtre)
```

### QRResult.msg
```
std_msgs/Header header
string  team_id
uint32  qr_id
bool    formation_active
string  formation_type
float32 drone_spacing
bool    altitude_active
float32 altitude
bool    maneuver_active
float32 pitch_deg
float32 roll_deg
bool    detach_active
uint8   detach_drone_id
string  zone_color
uint32  next_qr_id          # 0 = son QR, eve dön
geometry_msgs/Point qr_position
geometry_msgs/Point next_qr_position
float32 wait_seconds        # loiter süresi
```

### SafetyEvent.msg
```
std_msgs/Header header
uint8  drone_id
string event_type    # BATTERY_CRITICAL | GEOFENCE_BREACH | OSCILLATION
string description
float32 severity
```

### TaskTrigger.msg
```
std_msgs/Header header
string task_type   # TASK1 | TASK2
bool   start       # True = başlat, False = durdur
string team_id
```

### SetQRMap.srv
```
# Request:
geometry_msgs/Point[] qr_positions
uint32[]              qr_ids
uint32[]              next_qr_ids
---
# Response:
bool   success
string message
```

---

## 10. Görev Akışı (TASK1)

```
[Operatör]                [intent_coordinator]        [local_fsm]
    │                           │                          │
    ├─[h] 15m irtifa─────────→ │ _drone_altitude=15       │
    │                           │                          │
    ├─[m] QR koordinatları────→ qr_perception             │
    │                           │ ← qr_map_ready=True      │
    │                           │                          │
    ├─[s] START ──────────────→ │ _mission_phase=ARMING    │
    │                           │                          │
    │                           ├──IDLE intent────────────→│ STANDBY→IDLE
    │                           │                          │ ARM + GUIDED
    │                           │     ←─local_state(IDLE)──│
    │                           │                          │
    │                           ├──QR_NAVIGATE intent─────→│ IDLE→FLYING
    │                           │  target=QR1(10,5)        │ setpoint aktif
    │                           │  formation=OKBASI        │
    │                           │  altitude=15m            │
    │                           │                          │
    │                    (drone kalkıp QR1'e yaklaşıyor)   │
    │                           │                          │
    │                    (qr_perception: drone3 QR1'e 5m yaklaştı)
    │                           │ ← QRResult(qr_id=1,       │
    │                           │   next=QR2, formasyon=V) │
    │                           ├──QR_NAVIGATE intent─────→│
    │                           │  target=QR2(-5,8)        │
    │                           │  formation=V             │
    │                           │  altitude=20m            │
    │                           │                          │
    │                    (QR2, QR3 aynı şekilde...)        │
    │                           │                          │
    │                    (QR3'te detach komutu)            │
    │                           ├──DETACH intent──────────→│ (drone2)
    │                           │  detach_drone_id=2        │ FLYING→DETACH
    │                           │  zone_color=RED          │
    │                           │                          │
    │                    (precision_landing drone2'yi RED zone'a götürür)
    │                           │                          │
    │                    (QR4, QR5, QR6...)               │
    │                           │                          │
    │                    (QR6: next_qr_id=0 → eve dön)   │
    │                           ├──RETURN_HOME intent─────→│
    │                           │                          │ FLYING→RETURN_HOME
    │                           │                          │ →LANDING
    [Görev Tamamlandı]
```

---

## 11. Durum Makineleri

### LocalState (local_fsm)

```
                    ┌─────────────┐
                    │   STANDBY   │ ← başlangıç
                    └──────┬──────┘
                           │ IDLE intent (arm)
                    ┌──────▼──────┐
                    │    IDLE     │ ← armed, GUIDED
                    └──────┬──────┘
                           │ QR_NAVIGATE intent
                    ┌──────▼──────┐
                    │   FLYING    │ ◄─────────────────┐
                    └──────┬──────┘                   │
                     DETACH│intent                    │ REJOIN
                    ┌──────▼──────┐            ┌──────┴──────┐
                    │   DETACH    │            │   REJOIN    │
                    └──────┬──────┘            └──────┬──────┘
                   zone<3m │                  arm+GUIDED│
                    ┌──────▼──────┐            ┌──────┴──────┐
                    │  LAND_ZONE  │            │    REARM    │
                    └──────┬──────┘            └──────┬──────┘
                    alt<0.5│                REJOIN │intent
                    ┌──────▼──────┐            ┌──────┴──────┐
                    │ DISARM_WAIT │────────────►│  (REJOIN)   │
                    └─────────────┘ REJOIN intent└─────────────┘

                    [Herhangi bir state'den]
                    SafetyEvent → SAFETY_HOLD
                    pilot_override=True → PILOT_OVERRIDE
                    RETURN_HOME intent → RETURN_HOME → LANDING
```

### MissionPhase (intent_coordinator)

```
IDLE → (task_trigger) → ARMING → (tüm drone IDLE) → NAVIGATING
     ↓                                                    ↓
  (abort)                                          (QR yaklaştı)
     ↓                                                    ↓
  IDLE ←──────────────────────────────────────── AT_QR
                                                    ↓ (detach komutu)
                                               DETACHING
                                                    ↓ (yedek drone varsa)
                                               REJOINING
                                                    ↓ (tüm QR bitti)
                                               RETURNING → COMPLETE
```

---

## 12. Formasyon Tipleri

### OKBASI (Ok Başı / Arrow Head)
```
Sıralama: rank-0 = en küçük ID, rank-1 = ikinci küçük, vb.

       ● rank-0  (drone en küçük ID)
      / \
 rank-1  rank-2

Normalize offsets (spacing=1m için):
  rank-0: (+2/3,  0 )   ← önce, ortada
  rank-1: (-1/3, -½)   ← arkada sol
  rank-2: (-1/3, +½)   ← arkada sağ
```

### V (V-Formation)
```
       ● rank-0
      /         \
 rank-1         rank-2

Normalize offsets:
  rank-0: (+2/3,  0 )   ← önde ortada
  rank-1: (-1/3, -1 )   ← daha geniş kanat
  rank-2: (-1/3, +1 )
```

### CIZGI (Line Abreast — Yan Yana)
```
● rank-0  ●rank-1  ● rank-2

Normalize offsets:
  rank-0: (0, +1)   ← sol
  rank-1: (0,  0)   ← orta
  rank-2: (0, -1)   ← sağ
```

**Spacing:** Tüm offsetler `drone_spacing` (metre) ile çarpılır.
Örn: spacing=5m, OKBASI → drone'lar arası yaklaşık 2.5-3.5m mesafe.

**Yaw Dönüşümü:** Offsetler formation_controller tarafından `target_yaw`'a göre döndürülür (ENU koordinat sistemi, x=doğu, y=kuzey).

---

## 13. QR Haritası (qr_map.yaml)

**Konum:** `config/qr_map.yaml`

**Format (Şekil 2 JSON):**
```yaml
trigger_radius: 5.0   # [m] — drone bu mesafeye girince QR okunur

qr_nodes:
  1:
    id: 1
    position:
      x: 10.0   # ENU koordinatları
      y: 5.0
      z: 0.0
    content:
      qr_id: 1
      gorev:
        formasyon:
          aktif: true
          tip: "OKBASI"          # OKBASI | V | CIZGI
        manevra_pitch_roll:
          aktif: false
          pitch_deg: "0"
          roll_deg: "0"
        irtifa_degisim:
          aktif: true
          deger: 15              # yeni hedef irtifa (m)
        bekleme_suresi_s: 3      # QR'da loiter süresi
      suruden_ayrilma:
        aktif: false
        ayrilacak_drone_id: null
        hedef_renk: null         # RED | BLUE | GREEN
        bekleme_suresi_s: null
      sonraki_qr:
        team_1: 2                # bu takım için bir sonraki QR ID
        team_2: 2
        team_3: 2

color_zones:
  - color: "RED"
    x: 5.0
    y: 3.0
    z: 0.0
    radius: 2.0
```

**Mevcut Rota:**
```
QR1(10,5) → QR2(10,-5) → QR3(15,0) → QR4(-5,8) → QR5(-5,-8) → QR6(20,0) → HOME
                               ↑
                          Detach: drone2 → RED zone(5,3)
```

**Yarışma Günü Değişikliği:**
- `[m]` komutuyla jüri koordinatları dashboard'dan girilir
- `SetQRMap` servisi bu YAML'ı runtime'da override eder
- Bu dosyaya yarışma günü dokunmayın → jüri koordinatları servis üzerinden gelir

---

## 14. Launch Konfigürasyonu

**Dosya:** `launch/swarm_competition.launch.py`

### Drone Konfigürasyonu

```python
DRONE_CONFIGS = [
    # (namespace, sysid, SITL_port, home_x, home_y, home_z)
    ('drone1', 1, 14550, 0.0, 0.0, 0.0),
    ('drone2', 2, 14560, 4.0, 0.0, 0.0),
    ('drone3', 3, 14570, 8.0, 0.0, 0.0),
]
```

### Port Tablosu

| Bağlantı | Port / Adres | Protokol |
|---|---|---|
| MAVROS ↔ SITL drone1 | UDP :14550 | MAVLink UDP |
| MAVROS ↔ SITL drone2 | UDP :14560 | MAVLink UDP |
| MAVROS ↔ SITL drone3 | UDP :14570 | MAVLink UDP |
| Gazebo ↔ SITL drone1 | UDP 127.0.0.1:9002 | ArduPilot JSON |
| Gazebo ↔ SITL drone2 | UDP 127.0.0.1:9012 | ArduPilot JSON |
| Gazebo ↔ SITL drone3 | UDP 127.0.0.1:9022 | ArduPilot JSON |
| SITL TCP serial | TCP :5760 (5770, 5780) | MAVLink TCP |

### Environment Variables (Her drone'a geçilen)

```
DRONE_NS=drone{i}
DRONE_ID={i}
SWARM_SIZE=3
HOME_X={hx}   HOME_Y={hy}   HOME_Z={hz}
FENCE_X_MIN=-5.0   FENCE_X_MAX=125.0
FENCE_Y_MIN=-5.0   FENCE_Y_MAX=95.0
FENCE_Z_MIN=0.5    FENCE_Z_MAX=60.0
ROS_LOCALHOST_ONLY=1
CYCLONEDDS_URI=file:///path/to/cyclonedds_localhost.xml
GZ_SIM_RESOURCE_PATH=...model_paths...
```

### Node Başlatma Gecikmesi

```python
per_drone_nodes başlatma offset'leri (drone1=0s, drone2=0.5s, drone3=1.0s):
  +0.0s : drone_interface
  +0.1s : local_fsm
  +0.2s : intent_coordinator
  +0.3s : formation_controller
  +0.4s : collision_avoidance
  +0.5s : waypoint_navigator
  +0.6s : precision_landing
  +0.7s : safety_monitor

GCS node'ları:
  +10.5s : qr_perception (drone3 namespace)
  +10.7s : mission_fsm (xterm'de ayrı pencere)
```

---

## 15. Güvenlik ve Sınırlar

### Şartname §5.3 (Dağıtık Mimari)
- GCS bağlantısı kesilse bile sürü devam eder
- TASK1_ACTIVE modunda GCS topic yazmaz (mode gating)
- Lider drone düşerse → diğer drone'lar 600ms içinde yeni lider seçer

### Şartname §13 (Hassas İniş)
- precision_landing XY hata < 0.8m garantisi
- Bölge merkezi üzerinde hover → local_fsm LAND komutu → ArduPilot hassas iner

### §5.4 (Çarpışma Önleme)
- APF R_MIN=3m içine girmeden önce tam kuvvet
- TTC < 1.5s → 3x amplifikasyon
- Titreşim tespiti → slew rate dampening

---

## 16. Bilinen Eksiklikler / Yapılacaklar

Bu bölüm arkadaşın çalışacağı alanları özetler:

### Yüksek Öncelikli

| # | Eksiklik | İlgili Dosya | Açıklama |
|---|---|---|---|
| 1 | **Gerçek QR Kamera Taraması** | `qr_perception.py` | Proximity yerine OpenCV + kamera topic ile pixel bazlı QR okuma. Drone3'ün kamera topic'i (`/{ns}/mavros/camera/...` veya RealSense) integrate edilmeli. |
| 2 | **Drone-to-Drone Wi-Fi** | `intent_coordinator.py` | Şu an tek makinede DDS localhost. Çoklu RPi4 için ROS2 discovery server veya CycloneDDS multicast konfigürasyonu gerekli. |
| 3 | **TASK2 (Teleop)** | `mission_fsm.py`, `swarm_teleop.py` | Joystick ile sürü kontrolü. `swarm_teleop.py` var ama launch'a ekli değil ve test edilmedi. |
| 4 | **REARM/REJOIN Akışı** | `local_fsm.py` | DISARM_WAIT → REARM → REJOIN geçişi implement edildi ama uçtan uca test edilmedi. |

### Orta Öncelikli

| # | Eksiklik | İlgili Dosya | Açıklama |
|---|---|---|---|
| 5 | **Gerçek Batarya İzleme** | `safety_monitor.py` | Mock batarya yerine `/{ns}/mavros/battery` topic'ini oku. |
| 6 | **GPS Tabanlı Konum** | `drone_interface.py` | Şu an ENU (Gazebo/MAVROS local_position). Gerçek dış mekan uçuşu için GPS + `global_position` gerekebilir. |
| 7 | **QR Format Doğrulama** | `qr_perception.py` | Şekil 2 JSON zorunlu alanlar için daha katı validation. |
| 8 | **Formasyon Geçiş Animasyonu** | `formation_controller.py` | Formasyon tipi değişiminde drone'lar sert atlıyor. Rank geçiş koruması 30 cycle var ama yeterli olmayabilir. |

### Düşük Öncelikli

| # | Eksiklik | Açıklama |
|---|---|---|
| 9 | Dashboard GUI | Şu an terminal CLI. Bir web dashboard (Flask + Socket.IO) veya rqt plugin daha kullanıcı dostu olur. |
| 10 | Log Kayıt Sistemi | Görev kayıt dosyası (uçuş logu, QR sırası, hata listesi) |
| 11 | Simülasyon Hız Ayarı | `speedup` parametresi ile daha hızlı test |

---

## Hızlı Başvuru

### Sık Kullanılan Komutlar

```bash
# Simülasyonu başlat
cd ~/gz_ws && source install/setup.bash && DISPLAY=:0 ros2 launch my_swarm_pkg swarm_competition.launch.py

# Sadece my_swarm_pkg rebuild
cd ~/gz_ws && colcon build --packages-select my_swarm_pkg

# Tüm workspace rebuild
cd ~/gz_ws && colcon build

# Tüm process'leri temizle
kill $(pgrep -f "arducopter|gz sim|mavros_node|drone_interface|local_fsm|mission_fsm|qr_percep|intent_coord|formation_con|collision_av|safety_mon|waypoint_nav|precision_land") 2>/dev/null

# Log izle (canlı)
tail -f /tmp/swarm_launch*.log | grep -E "FLYING|ARMING|QR|ERROR|irtifa|formasyon"

# Topic dinle
source ~/gz_ws/install/setup.bash
ROS_LOCALHOST_ONLY=1 ros2 topic echo /swarm/intent

# Node listesi
ROS_LOCALHOST_ONLY=1 ros2 node list
```

### Önemli Sabitler (Hızlı Referans)

```
MAVROS portları:     14550 / 14560 / 14570
Gazebo JSON:         9002 / 9012 / 9022
MAVROS namespace:    /drone1 /drone2 /drone3
Heartbeat timeout:   600 ms (intent_coordinator)
APF R_MIN:           3.0 m
APF R_MAX:           8.0 m
Formasyon spacing:   5.0 m (varsayılan)
QR trigger radius:   5.0 m
Precision landing:   < 0.8 m XY hata garantisi
HOVER_ALT_M:         5.0 m (precision_landing hover)
Batarya kritik:      %15
Jeofence X:          -5 → 125 m
Jeofence Y:          -5 → 95 m
Jeofence Z:          0.5 → 60 m
```

---

*TEKNOFEST 2026 — İnşaAllah başarılar! 🚁🚁🚁*
