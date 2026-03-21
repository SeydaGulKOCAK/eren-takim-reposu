# SÜRÜ İHA YARIŞMASI ÖN TASARIM RAPORU

**TAKIM ADI:** [Takım Adı]
**PROJE ADI:** Dağıtık Bully Tabanlı Otonom Sürü İHA Sistemi
**BAŞVURU ID:** [Başvuru ID]
**TARİH:** Mart 2026

---

## İÇİNDEKİLER

1. [Yönetici Özeti (0-5 Puan)](#1-yönetici-özeti)
2. [Proje Yönetimi (0-5 Puan)](#2-proje-yönetimi)
3. [Proje Gereksinimleri (0-10 Puan)](#3-proje-gereksinimleri)
4. [İHA Platform Tasarımı (0-20 Puan)](#4-i̇ha-platform-tasarımı)
5. [Sürü Mimarisi, Görev Yönetimi ve Yazılım Tasarımı (0-35 Puan)](#5-sürü-mimarisi-görev-yönetimi-ve-yazılım-tasarımı)
6. [Görev Doğrulama, Simülasyon ve Değerlendirme (0-20 Puan)](#6-görev-doğrulama-simülasyon-ve-değerlendirme)
7. [Kaynakça](#7-kaynakça)

---

## 1. Yönetici Özeti

Bu çalışmada TEKNOFEST 2026 Sürü İHA Yarışması için ROS2 Humble, ArduPilot SITL ve Gazebo Sim 8 altyapısı üzerine inşa edilmiş, tam dağıtık otonom bir sürü sistemi geliştirilmiştir. Sistem; üç ArduCopter multikopter İHA'yı tek bir komutla eş zamanlı kaldırma, belirlenen irtifaya formasyon halinde yükselme, QR kod noktalarına sürü olarak navigasyon, QR içeriğini görsel algılama yöntemiyle çözümleme, dinamik formasyon değişimi, pitch/roll manevraları, irtifa değişimi ve renk bölgesine hassas iniş kabiliyetlerine sahiptir. Merkezi bir koordinatörden bağımsız çalışan Bully algoritması tabanlı dağıtık lider seçimi ile herhangi bir İHA devre dışı kaldığında 600 ms içinde yeni lider seçilmektedir. Formasyon kontrolü için Sanal Yapı (Virtual Structure) yöntemi, çarpışmadan kaçınma için ise Yapay Potansiyel Alan (APF) algoritması kullanılmaktadır. Sistem, Gazebo simülasyon ortamında 3 drone ile eş zamanlı kalkış, Ok Başı/V/Çizgi formasyon geçişleri ve renk bölgesine hassas iniş görevlerini başarıyla tamamlamaktadır.

---

## 2. Proje Yönetimi

### 2.1 Takım Organizasyonu

| Üye | Görev Alanı |
|---|---|
| [Üye 1 — Takım Kaptanı] | Sistem mimarisi, ROS2 koordinasyonu, intent_coordinator |
| [Üye 2] | Formasyon kontrolü, formation_controller, APF collision_avoidance |
| [Üye 3] | MAVROS entegrasyonu, drone_interface, uçuş testleri |
| [Üye 4] | QR algılama, waypoint_navigator, precision_landing |
| [Üye 5] | Gazebo simülasyonu, ArduPilot SITL, safety_monitor |

### 2.2 Proje Takvimi

| Dönem | Tamamlanan Çalışma |
|---|---|
| Ocak 2026 | Sistem mimarisi tasarımı, ROS2 + ArduPilot SITL kurulumu, temel node yapıları |
| Şubat 2026 | drone_interface, local_fsm, intent_coordinator geliştirme; Bully algoritması |
| Şubat-Mart 2026 | Virtual Structure formasyon, APF çarpışma önleme, waypoint_navigator, precision_landing |
| Mart 2026 | 3 drone eş zamanlı kalkış testleri, altitude gate düzeltmesi, simülasyon doğrulama |

---

## 3. Proje Gereksinimleri

### 3.1 Görev 1 — Dinamik Sürü Kabiliyeti Gereksinimleri

| # | Şartname Gereksinimi | Yazılımsal Karşılık | Durum |
|---|---|---|---|
| G1.1 | En az 3 İHA eş zamanlı kalkış | `drone_interface.py`: ARM + CMD_NAV_TAKEOFF; altitude gate (z > 0.5 m) | ✅ |
| G1.2 | Başlangıç formasyonunu koruyarak irtifaya yükselme | `formation_controller.py`: Sanal lider drone_altitude hedefine 3 m/s | ✅ |
| G1.3 | QR kodu görsel algılama ile çözümleme | `qr_perception.py`: pyzbar + OpenCV; 3 drone'da kamera | ✅ |
| G1.4 | QR içeriğine göre formasyon değişimi | `intent_coordinator.py`: QRResult → SwarmIntent.formation_type | ✅ |
| G1.5 | Pitch/Roll manevraları | `formation_controller.py`: Δz = f̂·tan(α_pitch) + l̂·tan(α_roll) | ✅ |
| G1.6 | İrtifa değişim komutu | `intent_coordinator.py`: SwarmIntent.drone_altitude güncelleme | ✅ |
| G1.7 | Birey ayrılma + renk bölgesine iniş | `precision_landing.py`: XY hata < 0.8 m + LAND | ✅ |
| G1.8 | Ayrılan bireyin sürüye yeniden katılması | `local_fsm.py`: DISARM_WAIT→REARM→REJOIN→FLYING | ✅ |
| G1.9 | Tüm QR sonrası home dönüşü | `waypoint_navigator.py`: next_qr_id=0 → HOME_RETURN | ✅ |
| G1.10 | Formasyon rotasyonu | `formation_controller.py`: hedef yönüne R(ψ) rotasyon matrisi | ✅ |
| G1.11 | Dağıtık algoritma | Bully lider seçimi; merkezi koordinatör yok | ✅ |

### 3.2 Görev 2 — Yarı Otonom Sürü Kontrolü Gereksinimleri

| # | Şartname Gereksinimi | Yazılımsal Karşılık | Durum |
|---|---|---|---|
| G2.1 | Joystick ile sürü yönlendirme | `formation_controller.py`: MOVE modu, p_c(t+Δt) = p_c(t) + v·Δt | ✅ |
| G2.2 | Formasyon bozulmadan hareket | MOVE modunda centroid güncellenir; offsetler yeniden hesaplanır | ✅ |
| G2.3 | Manevra modu (Pitch/Roll/Yaw) | MANEUVER modu; centroid sabit, 3D rotasyon geometrisi | ✅ |
| G2.4 | Kalkış ve iniş kumanda üzerinden | Takeoff/Land komutları joystick'ten intent üzerinden gönderilir | ✅ |

### 3.3 Güvenlik Gereksinimleri

| # | Gereksinim | Karşılık |
|---|---|---|
| S1 | Bağımsız failsafe | `safety_monitor.py`: jeofence + batarya; `local_fsm.py`: heartbeat timeout |
| S2 | Haberleşme kaybında RTL | GCS heartbeat kesilince SAFETY_HOLD → RTL |
| S3 | Çarpışmadan kaçınma | APF: R_MIN = 3 m tampon mesafesi |
| S4 | RC kumanda önceliği | `drone_interface.py`: non-GUIDED mod → PILOT_OVERRIDE |

---

## 4. İHA Platform Tasarımı

### 4.1 Genel Tasarım ve Yarışma Uygunluğu

Yarışmada kullanılan İHA platformu çok rotorlu (multikopter) konfigürasyonunda ArduCopter açık kaynak uçuş yazılımı ile donatılmıştır. Sistemin temel tasarım kararları şunlardır:

- Her İHA bağımsız hesaplama birimi taşır (RPi4 veya eşdeğeri) ve tüm sürü algoritmalarını yerelde çalıştırır.
- Merkezi bir koordinatör sunucu yoktur; tüm koordinasyon ROS2 DDS mesajlaşması ile gerçekleşir.
- Simülasyonda Gazebo Sim 8, gerçek donanımda Pixhawk/ArduPilot tabanlı platform hedeflenmektedir.

### 4.2 Otopilot Sistemi

- **Uçuş yazılımı:** ArduCopter (ArduPilot — açık kaynak)
- **Uçuş modu:** GUIDED — yer kontrol setpoint'lerine yanıt verir
- **ROS2 entegrasyonu:** MAVROS (MAVLink ↔ ROS2 köprüsü)
- **Kritik MAVLink komutları:**

| MAVLink Mesajı | Kullanım Amacı |
|---|---|
| `CMD_NAV_TAKEOFF` | Kalkış (irtifa parametreli) |
| `SET_POSITION_TARGET_LOCAL_NED` | Konum setpoint (ENU → NED MAVROS dönüşümü) |
| `SET_MODE` | GUIDED / LAND / RTL / BRAKE |
| `CMD_COMPONENT_ARM_DISARM` | ARM / DISARM |

### 4.3 Haberleşme Mimarisi

Sistemde iki farklı haberleşme katmanı bulunmaktadır:

**İHA–YKİ (Yer Kontrol İstasyonu):** MAVLink protokolü üzerinden UDP. Her drone ayrı port üzerinden bağlanır (drone1: 14550, drone2: 14560, drone3: 14570). MAVROS bu köprüyü sağlar.

**İHA–İHA:** ROS2 DDS (CycloneDDS implementasyonu). Tüm sürü koordinasyon mesajları `/swarm/*` topic'leri üzerinden yayınlanır. Mesajlar UDP multicast ile tüm drone'lara ulaşır; merkezi bir broker gerekmez.

```
GCS (mission_fsm)
    │ ROS2 DDS
    ▼
/swarm/task_trigger ──────────────────────────────────────────────────────┐
                                                                          │
┌─── Drone 1 ──────────┐  ┌─── Drone 2 ──────────┐  ┌─── Drone 3 ──────────┐
│ intent_coordinator   │  │ intent_coordinator   │  │ intent_coordinator   │
│ local_fsm            │◄─►│ local_fsm            │◄─►│ local_fsm            │
│ formation_controller │  │ formation_controller │  │ formation_controller │
│ collision_avoidance  │  │ collision_avoidance  │  │ collision_avoidance  │
│ drone_interface      │  │ drone_interface      │  │ drone_interface      │
│ safety_monitor       │  │ safety_monitor       │  │ safety_monitor       │
│ waypoint_navigator   │  │ waypoint_navigator   │  │ waypoint_navigator   │
│ precision_landing    │  │ precision_landing    │  │ precision_landing    │
│ qr_perception        │  │      ...             │  │      ...             │
└──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘
      MAVLink UDP              MAVLink UDP              MAVLink UDP
      port 14550               port 14560               port 14570
           │                        │                        │
    ArduCopter SITL          ArduCopter SITL          ArduCopter SITL
    (Gazebo plugin            (Gazebo plugin            (Gazebo plugin
     UDP 9002)                 UDP 9012)                 UDP 9022)
```

### 4.4 Kamera Sistemi

Sistemde 3 drone'un **tamamında** kamera bulunmaktadır (şartname minimum 1 kamera gerektirir; 3 kamera ile yedeklilik sağlanmıştır):

- **Birincil QR kamera:** drone1 (yapılandırılabilir `camera_drone_id` parametresi)
- **Otomatik failover:** Birincil drone DETACH/SAFETY_HOLD durumuna geçince `qr_perception` yedek drone'a (drone2 veya drone3) geçer
- **Entegrasyon:** ROS2 `/{ns}/camera/image_raw` topic; `pyzbar` kütüphanesi ile JSON decode
- **FOV kısıtı:** Şartname uyumu için maksimum 90° görüş açısı

### 4.5 Yazılım Bileşen Mimarisi

```
┌──────────────────────────────────────────────────────────────────┐
│                Her İHA'da Çalışan Node Seti                       │
│                                                                  │
│  mission_fsm ──────► /swarm/task_trigger                         │
│  qr_perception ─────► /qr/result, /swarm/qr_map_ready           │
│  safety_monitor ────► /safety/event                              │
│                                                                  │
│  intent_coordinator ◄─── tüm girdi topic'leri                    │
│        │ /swarm/intent (SwarmIntent, 2 Hz)                       │
│        ▼                                                         │
│  local_fsm ──────────────────────────────────────────────────    │
│        │ cmd_arm, cmd_mode                                       │
│        ▼                                                         │
│  formation_controller ──► /swarm/virtual_leader (lider yayınlar) │
│        │ /{ns}/setpoint_raw (50 Hz)                              │
│        ▼                                                         │
│  collision_avoidance                                             │
│        │ /{ns}/setpoint_final (50 Hz)                            │
│        ▼                                                         │
│  drone_interface ◄─── precision_landing (/{ns}/landing_target)  │
│        │ MAVLink                                                  │
│        ▼                                                         │
│  MAVROS ◄──► ArduCopter SITL ◄──► Gazebo Sim 8                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Sürü Mimarisi, Görev Yönetimi ve Yazılım Tasarımı

### 5.1 Sürü Mimarisi: Tam Dağıtık Lider-Takipçi

**Seçilen mimari:** Tam dağıtık, dinamik lider-takipçi (Distributed Dynamic Leader-Follower).

Her İHA, tüm sürü node'larının tam bir kopyasını çalıştırır. Lider seçimi, merkezi bir sunucu veya koordinatör olmaksızın Bully algoritması ile gerçek zamanlı yapılır. Bu tercih aşağıdaki gerekçelere dayanmaktadır:

| Kriter | Merkezi | Dağıtık (bu sistem) |
|---|---|---|
| Tek nokta arızası | Koordinatör düşünce sistem çöker | Herhangi bir drone düşünce sistem devam eder |
| Ölçeklenebilirlik | N artınca koordinatör darboğaz | Her drone bağımsız karar verir |
| Haberleşme yükü | O(N) yük koordinatörde toplanır | O(N) broadcast; dengeli dağılım |
| Gecikme | Koordinatör gecikmesi tüm sistemi etkiler | Yerel karar; düşük gecikme |
| Hata toleransı | Düşük | Yüksek: Bully ile 600 ms'de yeni lider |

Ren & Beard (2004) [1], merkezi koordinatörsüz dağıtık uzlaşmanın (consensus) sürü sistemlerinde daha güvenilir sonuçlar verdiğini kanıtlamıştır. Chung et al. (2018) [5], hava sürü sistemlerinde lider-takipçi mimarisinin formasyon tutma açısından en pratik yaklaşım olduğunu göstermiştir.

---

### 5.2 Bully Algoritması ile Dağıtık Lider Seçimi (`intent_coordinator.py`)

#### 5.2.1 Algoritmanın Çalışma Prensibi

Her drone, diğer tüm drone'ların `/{ns}/local_state` topic'ini **10 Hz** frekansında dinler ve bir heartbeat mekanizması ile canlılıklarını izler. Lider seçimi tamamen deterministik olup her drone **aynı hesaplamayı yaparak aynı sonuca** ulaşır; bu sayede merkezi bir seçim protokolüne gerek duyulmaz.

**Heartbeat mekanizması parametreleri:**

| Parametre | Değer | Açıklama |
|---|---|---|
| $T_{pub}$ | 100 ms (10 Hz) | `local_fsm` yayın periyodu |
| $T_{timeout}$ | 600 ms | Heartbeat timeout eşiği |
| $N_{margin}$ | 6 paket | Wi-Fi jitter güvenlik marjı: $N_{margin} = T_{timeout}/T_{pub}$ |

**Canlılık koşulu:**

Drone $i$'nin "canlı" sayılması için son $T_{timeout}$ içinde heartbeat alınmış olması gerekir:

$$\text{alive}(i) = \begin{cases} \text{True} & \text{eğer } t_{now} - t_{last\_hb}(i) < T_{timeout} \\ \text{False} & \text{aksi hâlde} \end{cases}$$

Burada $t_{last\_hb}(i)$ drone $i$'den gelen son `LocalState` mesajının ROS zaman damgasıdır.

**Aday kümesi:**

Uçuş fazında lider adayları yalnızca FLYING veya REJOIN durumundaki canlı drone'lardır:

$$\mathcal{A}_{ucus} = \{i \in \{1,2,3\} \mid \text{alive}(i) \land \text{state}(i) \in \{\text{FLYING, REJOIN}\}\}$$

Görev başlangıcında (henüz kimse uçmuyorken) ARMING fazı için:

$$\mathcal{A}_{baslangic} = \{i \mid \text{alive}(i) \land \text{state}(i) \in \{\text{STANDBY, IDLE}\}\}$$

**Lider seçim kuralı (Bully):**

$$\text{leader} = \arg\min_{i \in \mathcal{A}} (i)$$

En küçük ID'li canlı drone liderdir. $\mathcal{A} = \emptyset$ ise lider seçimi askıya alınır.

#### 5.2.2 Seq Sürekliliği — Lider Değişiminde Mesaj Kaybını Önleme

`local_fsm`'de her drone gelen `SwarmIntent` mesajlarını aşağıdaki çift filtreden geçirir:

$$\text{mesaj\_geçerli} \iff \underbrace{\text{seq} > \text{seq}_{son}}_{\text{1. filtre: monotonluk}} \land \underbrace{t_{msg} \geq t_{son}}_{\text{2. filtre: zaman damgası}}$$

Lider değiştiğinde eski liderin geç gelen mesajları (stale paketler) bu filtre sayesinde DROP edilir. Yeni lider, global son seq'den bir fazlasından başlar:

$$\text{seq}_{yeni\_lider} = \text{seq}_{global\_son} + 1$$

Bu mekanizma olmadan eski lider seq=50 göndermiş olsa ve yeni lider seq=1'den başlasa, local_fsm eski lider mesajını "yeni" zanneder ve yanlış karar verebilir.

#### 5.2.3 Kamera Drone Koruması

Şartname gereği görev boyunca en az bir İHA'da aktif kamera bulunmalıdır. Sistem, DETACH kararı verirken kamera drone'unun ayrılmamasını garanti eder. Eğer QR içeriğindeki ayrılacak drone ID'si kamera drone'u ise, `intent_coordinator` otomatik olarak başka bir FLYING drone'u DETACH için seçer.

---

### 5.3 Görev Faz Makinesi — MissionPhase (`intent_coordinator.py`)

`intent_coordinator` içinde bir üst-düzey görev faz makinesi çalışır. Sadece lider drone aktif karar üretir; diğerleri gözlemler.

```
IDLE
 │  TaskTrigger(start=True)
 ▼
ARMING ── SwarmIntent(IDLE) → 3 drone ARM + GUIDED
 │  Tüm drone'lar state=IDLE rapor eder
 ▼
NAVIGATING ── SwarmIntent(QR_NAVIGATE, target=QR1, formation=OKBASI, alt)
 │  waypoint_navigator loiter komutu gönderir (QR1'e 5m yaklaştı)
 ▼
AT_QR ── QR içeriği okunuyor
 │  QRResult.next_qr_id → sonraki QR veya detach
 │  QRResult.detach_active = True
 ▼
DETACHING ── SwarmIntent(DETACH, detach_drone_id, zone_color)
 │  Ayrılan drone DISARM_WAIT durumuna geçti
 ▼
REJOINING ── Ayrılan drone sürüye FLYING ile katıldı
 ▼
RETURNING ── SwarmIntent(RETURN_HOME)
 │  Tüm drone'lar LANDING veya DISARM_WAIT durumunda
 ▼
COMPLETE
```

**Geçiş koşulları özeti:**

| Geçiş | Koşul |
|---|---|
| IDLE → ARMING | `task_trigger.start = True` ve `qr_map_ready = True` |
| ARMING → NAVIGATING | Tüm canlı drone'ların state'i `IDLE` (ARM tamamlandı) |
| NAVIGATING → AT_QR | `waypoint_navigator` loiter_cmd=True yayınladı |
| AT_QR → DETACHING | QRResult'ta `detach_active = True` |
| DETACHING → REJOINING | Detach drone'u `DISARM_WAIT` durumuna geçti |
| RETURNING → COMPLETE | Tüm drone'lar `LANDING` veya `DISARM_WAIT` |

---

### 5.4 Per-Drone Durum Makinesi (`local_fsm.py`)

Her drone'da bağımsız çalışan yerel durum makinesi, gelen `SwarmIntent` mesajlarını işleyerek `drone_interface`'e komut gönderir.

#### 5.4.1 Durum Grafiği

```
STANDBY ─── SwarmIntent(IDLE) ──► IDLE
                                    │ ARM + GUIDED tamamlandı
                                    │ SwarmIntent(QR_NAVIGATE)
                                    ▼
                                 FLYING ◄──────────────── REJOIN
                                    │                       ▲
                       DETACH intent│                       │ ARM+GUIDED
                       (ben ayrılıyorum)                  REARM
                                    ▼                       ▲
                                 DETACH                     │
                                    │ zone < 3 m        DISARM_WAIT
                                    ▼                       ▲
                                LAND_ZONE ──── alt < 0.5m ──┘

[Herhangi bir state'den tetiklenebilir:]
  SafetyEvent         → SAFETY_HOLD → (FLYING / RETURN_HOME)
  pilot_override=True → PILOT_OVERRIDE → (FLYING)
  RETURN_HOME intent  → RETURN_HOME → LANDING → [son]
```

#### 5.4.2 Çift Filtre (Stale Mesaj Koruması)

Gelen her `SwarmIntent` mesajı iki koşula tabi tutulur. Her iki koşul da sağlanmazsa mesaj DROP edilir:

```
Gelen SwarmIntent
       │
       ▼
seq > seq_son? ──Hayır──► DROP (eski seq)
       │
      Evet
       │
       ▼
t_msg >= t_son? ──Hayır──► DROP (eski zaman damgası)
       │
      Evet
       │
       ▼
Intent işle → durum geçişi
```

---

### 5.5 Sanal Yapı (Virtual Structure) ile Formasyon Kontrolü (`formation_controller.py`)

Formasyon kontrolü, 50 Hz frekansında çalışan `formation_controller` node'u tarafından yürütülür. Temel yöntem Sanal Yapı (Virtual Structure) [2]: tüm drone'lar sanal bir centroid (sanal lider) etrafında rijit bir geometrik yapı oluşturur.

#### 5.5.1 Formasyon Geometrisi — Normalize Offsetler

Üç formasyon tipi için `spacing = 1 m` birim aralıkta normalize offsetler (koda birebir karşılık gelir):

**Ok Başı Formasyonu (OKBASI) — 3 drone:**

$$\text{rank 0 (öncü):} \quad (\hat{f}_0, \hat{l}_0) = \left(+\frac{2}{3},\ 0\right)$$
$$\text{rank 1 (sol kanat):} \quad (\hat{f}_1, \hat{l}_1) = \left(-\frac{1}{3},\ -\frac{1}{2}\right)$$
$$\text{rank 2 (sağ kanat):} \quad (\hat{f}_2, \hat{l}_2) = \left(-\frac{1}{3},\ +\frac{1}{2}\right)$$

**V Formasyonu — 3 drone:**

$$(\hat{f}_0, \hat{l}_0) = \left(+\frac{2}{3},\ 0\right), \quad (\hat{f}_1, \hat{l}_1) = \left(-\frac{1}{3},\ -1\right), \quad (\hat{f}_2, \hat{l}_2) = \left(-\frac{1}{3},\ +1\right)$$

**Çizgi Formasyonu (CIZGI) — 3 drone:**

$$(\hat{f}_0, \hat{l}_0) = (0,\ +1), \quad (\hat{f}_1, \hat{l}_1) = (0,\ 0), \quad (\hat{f}_2, \hat{l}_2) = (0,\ -1)$$

Her formasyon konfigürasyonu için centroid denge koşulu sağlanmaktadır:

$$\sum_{i=0}^{N-1} \hat{f}_i = 0, \qquad \sum_{i=0}^{N-1} \hat{l}_i = 0$$

Bu koşul, formasyon merkezinin (centroid) her zaman matematiksel ortalama konumda kalmasını garantiler.

**Rank ataması:**

Drone'lar sıralı ID'lerine göre rank alır: $\text{rank}_i = \text{index}(\text{drone\_id}_i, \text{sorted}(\mathcal{A}))$. Bu sayede lider her zaman en küçük ID'li drone'dur (rank 0 = öncü pozisyon).

#### 5.5.2 Dünya Koordinatlarına Dönüşüm — Formasyon Rotasyonu

Hedef noktaya olan yaw açısı:

$$\psi = \text{atan2}(y_{target} - y_{centroid},\ x_{target} - x_{centroid})$$

Normalize formasyon offsetleri 2D rotasyon matrisiyle dünya koordinatlarına dönüştürülür:

$$\begin{bmatrix} \Delta x_i \\ \Delta y_i \end{bmatrix} = s \cdot \begin{bmatrix} \cos\psi & -\sin\psi \\ \sin\psi & \cos\psi \end{bmatrix} \begin{bmatrix} \hat{f}_i \\ \hat{l}_i \end{bmatrix}$$

Drone $i$'nin setpoint konumu:

$$\mathbf{p}_i^{sp} = \begin{bmatrix} x_c + \Delta x_i \\ y_c + \Delta y_i \\ z_c + \Delta z_i \end{bmatrix}$$

Burada $(x_c, y_c, z_c)$ sanal liderin konumu, $s$ aralık mesafesi (metre), $\Delta z_i$ manevra geometrisinden gelir (§5.5.4).

#### 5.5.3 Sanal Lider Navigasyonu — Virtual Structure Merkezi

Sanal centroid $\mathbf{p}_{vl}$, fiziksel drone konumlarından **bağımsız** olarak hedef QR noktasına $v_{max} = 3.0$ m/s sabit hızla ilerler. Bu ayrım "Sürüklenen Sürü" (Drifting Swarm) sorununu çözer: fiziksel centroid kullanılsaydı, drone'lar hedefe gidemeden mevcut konumlarında kilitlenirdi.

Her 50 Hz adımında ($\Delta t = 0.02$ s):

$$d = \|\mathbf{p}_{target} - \mathbf{p}_{vl}\|$$

$$\mathbf{p}_{vl}(t + \Delta t) = \begin{cases} \mathbf{p}_{target} & d < r_{arrival} \\ \mathbf{p}_{vl}(t) + \dfrac{v_{max}}{\text{Hz}} \cdot \dfrac{\mathbf{p}_{target} - \mathbf{p}_{vl}}{d} & d \geq r_{arrival} \end{cases}$$

$r_{arrival} = 0.3$ m (koddan alınan gerçek değer). Yeni QR komutunda `target_pos` değişince sanal lider otomatik olarak yeni hedefe yönelir.

**Sanal Lider Senkronizasyonu:**

Yalnızca lider drone sanal lider konumunu hesaplar ve `/swarm/virtual_leader` topic'ine yayınlar. Takipçi drone'lar bu paylaşılan sanal lideri kullanır; böylece tüm sürü **aynı sanal lider etrafında** formasyon kurar:

```
Lider drone:  VL hesapla → /swarm/virtual_leader yayınla
Takipçi drone: /swarm/virtual_leader oku → kendi setpoint'ini hesapla
```

Paylaşılan VL verisi 0.5 s'den eskiyse (stale) takipçi kendi lokal VL hesabına döner.

#### 5.5.4 Pitch/Roll Manevra Geometrisi

QR kodu pitch veya roll manevra komutu içerdiğinde her drone'un Z offseti şu formülle hesaplanır. Centroid irtifası sabit tutulur ($\sum \Delta z_i = 0$ garantili):

$$\Delta z_i = \hat{f}_i \cdot s \cdot \tan(\alpha_{pitch}) + \hat{l}_i \cdot s \cdot \tan(\alpha_{roll})$$

Kod içinde tan değeri $\pm 2.0$ ile kliplenerek aşırı irtifa sapmalarına karşı güvenlik sağlanır.

**Örnek — Ok Başı, spacing=5 m, pitch=-10°:**

$$\Delta z_0 = \left(+\frac{2}{3}\right)(5)\tan(-10°) = 3.33 \times (-0.176) = -0.587 \text{ m}$$
$$\Delta z_1 = \left(-\frac{1}{3}\right)(5)\tan(-10°) = -1.67 \times (-0.176) = +0.294 \text{ m}$$
$$\Delta z_2 = +0.294 \text{ m}$$
$$\sum \Delta z_i = -0.587 + 0.294 + 0.294 \approx 0 \checkmark$$

#### 5.5.5 Slew Rate Limiter — Ani Sıçrama Önleyici

Ardışık 50 Hz adımları arasındaki maksimum setpoint değişimi sınırlandırılır:

$$\|\mathbf{p}_{sp}(t) - \mathbf{p}_{sp}(t-\Delta t)\| \leq \Delta_{max}$$

| Mod | $\Delta_{max}$ | Maksimum Hız |
|---|---|---|
| Normal | 0.10 m/adım | 5.0 m/s |
| Osilasyon dampening | 0.02 m/adım | 1.0 m/s |

Osilasyon dampening 8 saniyeliğine aktive edilir (§5.6.4).

#### 5.5.6 Rank Geçiş Koruması

Bir drone DETACH ile sürüden ayrılınca kalan drone'ların rank'ı değişir. Ani rank değişimi setpoint'te sıçramaya neden olabilir. Bu durum **30 adım (0.6 s) geçiş koruma penceresi** ile yumuşatılır: drone geçiş süresince eski rank'ını korur, setpoint'ler arc (yay) hareketiyle yeni pozisyona kayar.

#### 5.5.7 Görev 2: Yarı Otonom Modu (MOVE/MANEUVER)

Joystick girdileri iki modda işlenir:

**MOVE modu** — Sürü ileri/geri/sağ/sol/irtifa hareketi:

$$\mathbf{p}_c(t + \Delta t) = \mathbf{p}_c(t) + \mathbf{v}_{joystick} \cdot \Delta t$$

$$\psi(t + \Delta t) = \psi(t) + \dot{\psi}_{joystick} \cdot \Delta t$$

Centroid güncellendikten sonra tüm drone'ların setpoint'leri yeni centroid etrafında yeniden hesaplanır; formasyon geometrisi bozulmaz.

**MANEUVER modu** — Centroid sabit, formasyon değişimi veya pitch/roll eğimi:

Centroid $\mathbf{p}_c$ sabit tutulur; yalnızca `formation_type`, `drone_spacing` veya manevra açıları güncellenir. Bu sayede sürünün konumu değişmeden görsel manevralar yapılır.

**Eş Zamanlı Komut Uygulaması — execute_at Zaman Damgası:**

`/swarm/teleop_cmd` topic'inde taşınan `execute_at` zaman damgası sayesinde her İHA joystick komutunu **aynı anda** uygulamaktadır. WiFi gecikmesi her drone'a komutu farklı zamanlarda iletebilir; ancak `execute_at` mekanizması sayesinde tüm drone'lar bu damgayı bekleyerek komutu eş zamanlı yürütür. Böylece WiFi gecikmesinden kaynaklanan formasyon yırtılması riski tasarım düzeyinde ortadan kaldırılmaktadır. TASK1_ACTIVE modunda `swarm_teleop` yazılımsal olarak tamamen kapalıdır; mode gating mekanizması iki operasyon modu arasındaki geçişi güvence altına almaktadır.

---

### 5.6 Yapay Potansiyel Alan (APF) ile Çarpışmadan Kaçınma (`collision_avoidance.py`)

APF algoritması [4], 50 Hz frekansında çalışır ve formation_controller'dan gelen ham setpoint'e ($\mathbf{p}_{raw}$) komşu drone'lardan kaynaklanan itici kuvvetler ekleyerek çarpışma önleme sağlar.

#### 5.6.1 İtici Kuvvet Hesabı

Drone $i$'nin drone $j$'den aldığı itici kuvvet büyüklüğü (Khatib 1986 [4] APF formülü):

$$\|\mathbf{F}_{ij}\| = K_{REP} \cdot \left(\frac{1}{d_{ij}} - \frac{1}{R_{MAX}}\right) \cdot \frac{1}{d_{ij}^2}, \qquad d_{ij} < R_{MAX}$$

İtici kuvvet vektörü (komşudan uzaklaşma yönünde):

$$\mathbf{F}_{ij} = \|\mathbf{F}_{ij}\| \cdot \frac{\mathbf{p}_i - \mathbf{p}_j}{\|\mathbf{p}_i - \mathbf{p}_j\|}$$

**Sistem parametreleri (koddan alınan değerler):**

| Parametre | Değer | Açıklama |
|---|---|---|
| $K_{REP}$ | 18.0 | İtici kazanç — 6 m nominal spacing için kalibre edilmiş |
| $R_{MAX}$ | 8.0 m | Etki alanı başlangıç mesafesi |
| $R_{MIN}$ | 3.0 m | Tehlike bölgesi (tam kuvvet) |
| $MAX\_CORR$ | 3.0 m | APF düzeltme vektörü clip sınırı |

**Örnek hesap ($d = 4$ m, $K_{REP} = 18$):**

$$\|\mathbf{F}\| = 18.0 \cdot \left(\frac{1}{4} - \frac{1}{8}\right) \cdot \frac{1}{16} = 18.0 \cdot 0.125 \cdot 0.0625 = 0.141 \text{ m}$$

#### 5.6.2 TTC (Time-To-Collision) Amplifikasyonu

Drone'lar birbirine yaklaşıyorsa tehlike daha yüksektir. Göreli yaklaşma hızı, konum vektörü projeksiyon formülüyle hesaplanır:

$$\dot{d}_{ij} = \frac{(\mathbf{p}_i - \mathbf{p}_j) \cdot (\mathbf{v}_i - \mathbf{v}_j)}{\|\mathbf{p}_i - \mathbf{p}_j\|}$$

$\dot{d}_{ij} < 0$ ise drone'lar yaklaşıyordur. Çarpışmaya kalan süre:

$$TTC_{ij} = \frac{d_{ij}}{|\dot{d}_{ij}|}$$

TTC eşiği altında ($TTC_{ij} < T_{TTC} = 1.5$ s) kuvvet 3 kat büyütülür:

$$K_{eff} = \begin{cases} K_{REP} \times 3.0 & TTC_{ij} < 1.5 \text{ s ve yaklaşıyorsa} \\ K_{REP} & \text{aksi hâlde} \end{cases}$$

**DETACH drone özel durumu:** Sürüden ayrılmakta olan drone'dan gelen APF kuvveti 0.5 katsayısıyla azaltılır; böylece drone'un sürüden ayrılmasına gereksiz direnç gösterilmez.

#### 5.6.3 Toplam Düzeltme ve Klipleme

$$\mathbf{F}_{total,i} = \sum_{j \neq i,\ d_{ij} < R_{MAX}} \mathbf{F}_{ij}$$

$$\mathbf{p}_{final,i} = \mathbf{p}_{raw,i} + \text{clip}(\mathbf{F}_{total,i},\ MAX\_CORR = 3.0 \text{ m})$$

Klipleme, tek bir yoğun çarpışma senaryosunda bile setpoint'in kontrolsüz sapmasını önler.

#### 5.6.4 Osilasyon Tespiti ve Proaktif Dampening

**Şartname notu:** Yarışma kurallarına göre sürüde tespit edilen osilasyon **−10 puan** cezasıyla sonuçlanır. Sistemimiz bu cezayı insan müdahalesi gerektirmeden, tamamen otonom olarak önler.

**Tespit yöntemi:**

Son $T_{osc} = 0.4$ s içindeki setpoint_final geçmişi (50 Hz × 0.4 s = **20 adım** pencere) kullanılır. X ve Y eksenlerindeki setpoint varyansının geometrik ortalaması hesaplanır:

$$\sigma_{xy} = \sqrt{\frac{\text{Var}(x_{sp}) + \text{Var}(y_{sp})}{2}}$$

**Eşik değeri:** $\sigma_{xy} > 0.08$ m → osilasyon tespit edildi.

Bu eşik, normal formasyon hareketinde ($\sigma_{xy} \approx 0.01$–$0.03$ m) yanlış alarm vermeyecek, gerçek APF geri besleme salınımında ($\sigma_{xy} > 0.1$ m) ise kesinlikle tetiklenecek şekilde kalibre edilmiştir.

**Proaktif tepki zinciri:**

```
collision_avoidance: σ_xy > 0.08m tespit edildi
        │
        ▼
SafetyEvent(OSCILLATION) → /safety/event yayınlanır
        │
        ▼
formation_controller: olayı alır
        │
        ▼
Slew rate limiter sıkılaştırılır:
  Normal:      Δ_max = 0.10 m/adım  (5.0 m/s)
  Dampening:   Δ_max = 0.02 m/adım  (1.0 m/s)
        │
        ▼
8 saniye boyunca düşük hızda setpoint → osilasyon söner
        │
        ▼
8 s sonra: Δ_max otomatik olarak 0.10 m/adım'a geri döner
```

**Dampening etkisi:**

Setpoint değişim hızı 5 kat düşürüldüğünde ($\frac{0.10}{0.02} = 5\times$), APF geri besleme döngüsünün kazancı sistemin doğal sönümleme sınırının altına iner ve salınım 1–2 saniye içinde durur.

**Cooldown koruması:** Aynı drone için ardışık olaylar **5 s** arayla tetiklenebilir; sinyal gürültüsünden kaynaklanan sahte alarmlar engellenir. Bu sayede dampening modunun gereksiz yere uzun süre aktif kalması önlenir.

---

### 5.7 Waypoint Navigatörü — QR→QR Rota Takibi (`waypoint_navigator.py`)

`waypoint_navigator`, **yalnızca lider drone'da** aktif karar üreten 10 Hz'lik bir navigasyon yöneticisidir. Takipçi drone'larda node çalışır ama lider değilse hiçbir şey yayınlamaz (bant genişliği tasarrufu).

#### 5.7.1 Flying Centroid Hesabı

Her 10 Hz adımında FLYING/DETACH/REJOIN/LAND_ZONE/RETURN_HOME durumundaki drone'ların konum ortalaması alınır:

$$\mathbf{p}_{centroid} = \frac{1}{|\mathcal{F}|} \sum_{i \in \mathcal{F}} \mathbf{p}_i$$

Burada $\mathcal{F}$ aktif uçuş durumundaki drone'lar kümesi, $\mathbf{p}_i$ her drone'un ENU konumudur. 1.5 s'den eski (stale) konum verisi hesaba katılmaz.

#### 5.7.2 Mesafe Hesabı ve Faz Geçişleri

Centroid ile hedef QR noktası arasındaki XY düzlem mesafesi:

$$d_{xy} = \sqrt{(x_c - x_{target})^2 + (y_c - y_{target})^2}$$

Bu mesafeye göre navigasyon fazı belirlenir:

| Faz | Koşul | Eylem |
|---|---|---|
| NAVIGATING | $d_{xy} \geq 20$ m | Tam hızda git; loiter_cmd=False |
| APPROACHING | $5 \leq d_{xy} < 20$ m | Yaklaşıyor; log/debug |
| LOITERING | $d_{xy} < 5$ m | loiter_cmd=True; QR trigger=True |
| WAITING | Loiter'dan 1.5s sonra | wait_seconds bekleniyor |

#### 5.7.3 Loiter Fazı — QR Okuma Protokolü

Sürü QR noktasına $r_{loiter} = 5.0$ m mesafeye girdiğinde:

1. `loiter_cmd = True` → `/swarm/loiter_cmd` yayınlanır → `formation_controller` setpoint'i dondurur (sürü hover)
2. `qr_trigger = True` → `/qr/trigger` yayınlanır → `qr_perception` kamerayı aktive eder
3. **1.5 s** bekle → WAITING fazına geç (QRResult gelecek)
4. `QRResult.wait_seconds` süresi dolunca → `loiter_cmd = False` → sürü devam eder

**QR Trigger Cooldown:** Aynı QR sequence numarası için tekrar tetikleme $T_{cooldown} = 10$ s ile engellenir; sürü QR etrafında gezinirken arka arkaya yanlış tetikleme olmaz.

#### 5.7.4 Eve Dönüş Fazı (HOME_RETURN)

Tüm QR noktaları tamamlandıktan (next_qr_id = 0) sonra:

$$d_{xy,home} < r_{home} = 3.0 \text{ m} \Rightarrow \text{loiter\_cmd=True}, \text{ NavPhase=COMPLETE}$$

Sürü home pozisyonuna $r_{home} = 3$ m yakınında hover eder; `intent_coordinator` RTL komutunu gönderir ve drone'lar iner.

---

### 5.8 Hassas İniş Algoritması (`precision_landing.py`)

DETACH komutu alan drone, renk bölgesine hassas iniş için formation_controller'dan bağımsız olarak `/{ns}/landing_target` topic'i üzerinden setpoint yayınlar. `drone_interface`, bu topic'i formation_controller setpoint'ine karşı öncelikli olarak işler.

#### 5.8.1 Aktivasyon Koşulu

Node her drone'da çalışır, ancak yalnızca şu iki koşul sağlandığında aktive olur:

1. `SwarmIntent.task_id == 'DETACH'`
2. `SwarmIntent.detach_drone_id == kendi drone_id`

Diğer tüm durumlarda node pasif kalır (pass-through).

#### 5.8.2 Hover ve XY Hizalama

Hedef zone konumu `/perception/color_zones` topic'inden (1 Hz, `qr_perception` yayınlar) alınır. Zone verisi $T_{stale} = 3$ s'den eskiyse kullanılmaz.

**DETACH fazında** (henüz iniyor):

$$z_{target} = \max(HOVER\_ALT\_M,\ z_{own}) = \max(5.0,\ z_{kendi})$$

Drone zone merkezinin tam üzerinde $z = 5$ m irtifada bekler.

**XY hizalama hatası:**

$$e_{xy} = \sqrt{(x_{own} - x_{zone})^2 + (y_{own} - y_{zone})^2}$$

$e_{xy} \leq XY\_PRECISE\_M = 0.8$ m olduğunda **hizalandı** loglanır. `local_fsm`, zone'a 3 m yaklaşınca LAND_ZONE durumuna geçer ve ArduCopter LAND modunu devreye alır.

**LAND_ZONE fazında** (aktif iniş):

$$z_{target} = z_{own} \quad \text{(mevcut irtifa korunur — ArduCopter LAND kendi alçaltır)}$$

Drone LAND_ZONE → DISARM_WAIT durumuna geçince node pasif olur (inişi müdahale etmez).

**Setpoint yayın formatı (10 Hz):**

```
landing_target.pose.position = (x_zone, y_zone, z_target)
```

Bu setpoint, formation_controller setpoint'ini override eder; drone zone merkezine kilitlenir.

---

### 5.9 QR Algılama Pipeline (`qr_perception.py`)

`qr_perception`, şartnamenin "görsel algılama" gereksinimini karşılayan ve tüm QR verilerini sürüye dağıtan algılama nodeudur. Hem gerçek kamera (pyzbar) hem de simülasyon (proximity) modunda çalışır.

#### 5.9.1 Çift Mod Mimarisi

```
MOD 1 — Görsel (Gerçek Donanım):
  /{ns}/camera/image_raw (ROS Image)
       │
       ▼ cv_bridge
  OpenCV frame (BGR8)
       │
       ▼ cv2.cvtColor(BGR→GRAY)
  Gri görüntü
       │
       ▼ pyzbar.decode()
  QR ham veri (bytes)
       │
       ▼ json.loads()
  Şekil 2 JSON → QRResult mesajı

MOD 2 — Proximity (Simülasyon / Yedek):
  /{ns}/pose → kamera drone konumu
  10 Hz döngüde mesafe hesabı:
  dist = √(Δx² + Δy²) ≤ trigger_radius (5.0m)
  → YAML'daki QR içeriğini oku → QRResult yayınla
```

İki mod ortak `_read_qr_ids` setini paylaşır: bir QR iki kez okunmaz.

#### 5.9.2 Şekil 2 JSON Formatı ve Parse Edilmesi

Şartnamenin Şekil 2'sinde tanımlanan JSON yapısı:

```json
{
  "qr_id": 3,
  "gorev": {
    "formasyon":          {"aktif": true,  "tip": "V"},
    "manevra_pitch_roll": {"aktif": false, "pitch_deg": "0", "roll_deg": "0"},
    "irtifa_degisim":     {"aktif": true,  "deger": 20},
    "bekleme_suresi_s":   3
  },
  "suruden_ayrilma": {
    "aktif": true,
    "ayrilacak_drone_id": 2,
    "hedef_renk": "RED",
    "bekleme_suresi_s": 5
  },
  "sonraki_qr": {"team_1": 4, "team_2": 4, "team_3": 4}
}
```

Parse sonucu `QRResult` mesajına dönüşür:

| JSON Alanı | QRResult Alanı |
|---|---|
| `gorev.formasyon.tip` | `formation_type` |
| `gorev.irtifa_degisim.deger` | `altitude` |
| `gorev.manevra_pitch_roll` | `pitch_deg`, `roll_deg` |
| `suruden_ayrilma.ayrilacak_drone_id` | `detach_drone_id` |
| `suruden_ayrilma.hedef_renk` | `zone_color` |
| `sonraki_qr[team_key]` | `next_qr_id` |

**Takım anahtarı dönüşümü:** `team_id = "team1"` → YAML anahtarı `"team_1"` (kod: `team_id.replace('team', 'team_')`). Bu sayede farklı takımlar aynı QR'dan farklı rotalara yönlendirilebilir.

**Drone spacing sabit:** `drone_spacing = 6.0 m` (şartname §5.2.1 gereği).

#### 5.9.3 Kamera Failover — Otomatik Yedek Kameraya Geçiş

Birincil kamera drone'u (varsayılan: drone1) kritik duruma geçtiğinde sistem otomatik olarak yedek drone'a (drone2) geçer:

```
Her drone'un local_state'i izleniyor
       │
       ▼
drone1.state ∈ {DETACH, SAFETY_HOLD, PILOT_OVERRIDE}?
       │
      Evet
       │
       ▼
failover_active = True
camera_drone_id = backup_cam_id (drone2)
       │
       [Yedek drone kamerası aktif]
       │
       ▼
drone1.state == REJOIN?
       │
      Evet → failover_active = False → camera_drone_id = drone1 (geri dön)
```

Bu mekanizma şartnamenin "görev boyunca en az bir aktif kamera" gereksinimini güvence altına alır.

#### 5.9.4 Renk Zone Yayını

`qr_perception`, YAML'dan yüklenen renk bölgesi koordinatlarını **1 Hz** ile `/perception/color_zones` topic'ine yayınlar. `precision_landing` ve `local_fsm` bu veriyi kullanır:

```
color_zones.yaml:
  - color: RED,   x: 10.0, y: 20.0, z: 0.0, radius: 3.0
  - color: BLUE,  x: 30.0, y: 20.0, z: 0.0, radius: 3.0
  - color: GREEN, x: 50.0, y: 20.0, z: 0.0, radius: 3.0
```

#### 5.9.5 Runtime QR Haritası Güncelleme (Yarışma Günü)

Jüri yarışma günü QR koordinatlarını açıkladığında operatör `/swarm/set_qr_map` servisiyle haritayı canlı günceller; drone'ların yeniden başlatılmasına gerek yoktur:

```
ros2 service call /swarm/set_qr_map swarm_msgs/srv/SetQRMap \
  "{qr_ids: [1,2,3], qr_positions: [...], next_qr_ids: [2,3,0]}"
```

Güncelleme sonrası `/swarm/qr_map_ready = True` yayınlanır → `intent_coordinator` görevi başlatabilir.

---

### 5.10 REJOIN Algoritması — Ayrılan Drone'un Sürüye Dönüşü (`local_fsm.py`)

DETACH sonrası inen drone, `intent_coordinator`'ın REJOIN komutuyla otomatik olarak sürüye yeniden katılır. Bu süreç tamamen otonom gerçekleşir; operatör müdahalesi gerekmez.

#### 5.10.1 REJOIN Durum Geçişleri

```
DISARM_WAIT
    │ intent_coordinator: SwarmIntent(REJOIN, join_drone_id=kendi_id)
    ▼
  REARM
    │ local_fsm: ARM komutu → drone_interface → MAVROS cmd_arming
    │ local_fsm: GUIDED mod → drone_interface → MAVROS set_mode
    │
    │ [ikinci REJOIN intent'i]
    ▼
  REJOIN
    │ formation_controller: sürü formasyon pozisyonuna setpoint gönderir
    │ (rank yeniden hesaplanmış, 30 adım rank geçiş koruması aktif)
    │
    │ [QR_NAVIGATE intent'i gelince]
    ▼
  FLYING ← Sürüye tam katılım tamamlandı
```

#### 5.10.2 REJOIN Koşul Kontrolü

```
Gelen REJOIN intent:
    │
    ▼
join_drone_id == kendi drone_id? ──Hayır──► Yoksay (bu emir bize değil)
    │
   Evet
    │
    ▼
Mevcut state DISARM_WAIT veya REARM? ──Hayır──► Yoksay (henüz hazır değil)
    │
   Evet
    │
DISARM_WAIT ise → REARM geçişi → ARM + GUIDED
REARM ise      → REJOIN geçişi → formation_controller setpoint'lerini kabul et
```

#### 5.10.3 REJOIN Sırasında Formasyon Uyumu

REJOIN durumundaki drone, `formation_controller` tarafından diğer drone'larla birlikte hesaplanan formasyon setpoint'ine yönlenir. Ayrılma sırasında başlatılan **30 adım rank geçiş koruması** bu aşamada da aktif kalır: drone kademeli olarak formasyon pozisyonuna yerleşir, ani pozisyon sıçraması olmaz.

REJOIN drone'u `FLYING` durumuna geçince `waypoint_navigator` onu centroid hesabına dahil eder ve sürü navigasyonu normal şekilde devam eder.

---

### 5.11 MAVROS Köprüsü ve Altitude Gate (`drone_interface.py`)

`drone_interface`, ROS2 sürü mesajları ile MAVROS arasındaki çift yönlü köprüdür.

#### 5.9.1 Veri Akışı

| Yön | Topic / Servis | İşlem |
|---|---|---|
| MAVROS → ROS2 | `/{ns}/mavros/local_position/pose` | ENU konum; `/droneN/pose` olarak yayınlanır |
| MAVROS → ROS2 | `/{ns}/mavros/state` | ARM durumu, uçuş modu; pilot override tespiti |
| ROS2 → MAVROS | `/{ns}/mavros/setpoint_position/local` | Formasyon setpoint'i (50 Hz) |
| ROS2 → MAVROS | `/{ns}/mavros/cmd/arming` | ARM/DISARM servisi |
| ROS2 → MAVROS | `/{ns}/mavros/set_mode` | Mod değişimi servisi |

#### 5.9.2 Kalkış Sırasında Altitude Gate (Kritik Düzeltme)

ArduPilot GUIDED modunda kalkış süreci şöyle çalışır:

```
ARM → CMD_NAV_TAKEOFF → GUIDED_TAKEOFF modu → drone yükselir
```

Sorun: `formation_controller`, ARM'dan ~478 ms sonra `SET_POSITION_TARGET_LOCAL_NED` göndermeye başlar. Bu mesaj ArduPilot'u `GUIDED_TAKEOFF`'tan `GUIDED_POSITION` moduna geçirir. GUIDED_POSITION modunda yerdeki bir drone, 50 m uzaktaki bir setpoint'e pozisyon kontrolcüsüyle ulaşamaz; kalkış itkisi uygulanamaz. 10 s sonra auto-disarm tetiklenir.

**Çözüm — Altitude Gate:**

```
setpoint_final geldi
         │
         ▼
z_kendi > 0.5 m? ──Hayır──► BLOK (MAVROS'a iletme, TAKEOFF devam etsin)
         │
        Evet
         │
         ▼
MAVROS setpoint_position/local yayınla
```

Bu sayede `CMD_NAV_TAKEOFF` tamamlanana (drone 0.5 m'yi geçene) kadar formation_controller setpoint'leri sessizce engellenir; kalkış sonrası normal navigasyona geçilir.

#### 5.9.3 Pilot Override Tespiti

ArduPilot'un gerçek uçuş modu sürekli izlenir:

$$\text{pilot\_override} = \text{armed} \land \text{mode} \notin \{\text{GUIDED, LAND, RTL, BRAKE, AUTO}\}$$

Override tespitinde `local_fsm`'e bildirim gönderilir; sistem PILOT_OVERRIDE durumuna geçerek otonom setpoint yayınını durdurur. RC kumanda **her zaman önceliklidir**.

---

### 5.12 Güvenlik Monitörü (`safety_monitor.py`)

Her drone'da bağımsız çalışan 5 Hz güvenlik izleme döngüsü.

#### 5.10.1 Jeofence İzleme

Drone'un ENU koordinatları aşağıdaki sınırlar içinde olmalıdır:

$$\mathcal{F} = \{(x, y, z) \mid x \in [-5, 125],\ y \in [-5, 95],\ z \in [0.5, 60]\} \text{ metre}$$

İhlal tespitinde:

$$\text{SafetyEvent(GEOFENCE\_BREACH)} \rightarrow \text{local\_fsm: SAFETY\_HOLD} \rightarrow \text{RTL}$$

Olay şiddeti (severity), sınır merkezinden normalize uzaklıkla hesaplanır. Cooldown: 5 s.

#### 5.10.2 Batarya İzleme

$$\text{batarya} \leq 15\% \Rightarrow \text{SafetyEvent(BATTERY\_CRITICAL)} \rightarrow \text{RTL}$$

Cooldown: 30 s (aynı olayın tekrar tetiklenmesi engellenir).

---

### 5.13 Failsafe ve Donanım Arızası Davranışları

Sistem tasarımında **"hiçbir tek nokta arızası görevi durduramaz"** prensibi benimsenmiştir. Tüm failsafe kararları her drone'da bağımsız olarak alınır; GCS'ye veya başka bir drone'a onay sormak gerekmez (şartname §5.5.4).

---

#### 5.13.1 GCS / Haberleşme Bağlantısı Kaybı

**Şablon gereksinimi:** "Yer kontrol istasyonu ile bağlantının kesilmesi durumunda sistemin nasıl davranacağı açıklanmalıdır."

Sistemde iki farklı haberleşme kanalı vardır ve her birinin kaybı farklı şekilde ele alınır:

**Kanal 1 — GCS → intent_coordinator (görev komutları):**

```
/swarm/intent topic'i 3 s boyunca gelmedi
        │
        ▼  safety_monitor: HEARTBEAT_TIMEOUT_S = 3.0 s
safety_monitor uyarı loglar (5 s'de bir)
        │
        ▼
intent_coordinator yeni intent üretemiyorsa
→ son geçerli SwarmIntent korunur
→ Drone'lar son komuta göre uçmaya devam eder (hover / formasyon)
        │
        ▼  Bağlantı uzun süre kesilirse:
local_fsm: SAFETY_HOLD → _send_mode('RTL')
→ Her drone bağımsız olarak eve döner
```

**Dağıtık mimarinin avantajı:** Merkezi bir koordinatör olsaydı GCS bağlantısı kesilince tüm sürü duraklar veya rastgele hareket ederdi. Bully tabanlı dağıtık mimaride lider seçimi drone'lar arasında gerçekleşir; GCS sadece başlangıç komutu verir. GCS düşse bile drone'lar kendi aralarında lider seçerek göreve **devam edebilir**.

**Kanal 2 — İHA–İHA ROS2 DDS haberleşmesi:**

Drone'lar arası DDS mesajlaşması kesilirse Bully mekanizması devreye girer:

$$t_{now} - t_{last\_hb}(i) \geq 600\ \text{ms} \Rightarrow \text{alive}(i) = \text{False}$$

Etkilenen drone sürüden çıkarılır, kalan drone'lar yeni lider seçer ve göreve devam eder.

| Senaryo | Tepki süresi | Davranış |
|---|---|---|
| GCS intent kesildi (3s) | 3 s | Uyarı log; son komut korunur |
| GCS intent kesildi (uzun) | ~10 s | SAFETY_HOLD → RTL |
| Drone-drone DDS kesildi | 600 ms | Bully: yeni lider seçimi |
| Tüm haberleşme kesildi | 600 ms | Her drone bağımsız RTL |

---

#### 5.13.2 İHA Arızası / Lider Düşmesi

Bully algoritması çekirdeğindeki lider seçimi mekanizması bu senaryoyu otomatik olarak çözer:

```
drone1 (lider) arızalandı
        │
        ▼  t = 0 ms: son heartbeat
t = 600 ms: alive(drone1) = False
        │
        ▼
Tüm drone'lar: leader = min({drone2, drone3}) = drone2
        │
        ▼  t ≈ 700 ms
drone2 lider oldu → SwarmIntent yayınlamaya başladı
Rank yeniden hesaplandı → 30 adım (0.6 s) geçiş koruması
        │
        ▼
Görev kaldığı yerden devam eder
```

**3 → 2 drone senaryosunda formasyon uyarlaması:**

$$\mathcal{A}_{yeni} = \{drone2, drone3\} \Rightarrow \text{rank}_0 = drone2,\ \text{rank}_1 = drone3$$

2 drone'lu Ok Başı formasyonunda centroid denge koşulu korunur:
$$\hat{f}_0 + \hat{f}_1 = 0, \quad \hat{l}_0 + \hat{l}_1 = 0$$

| Durum | Tepki | Süre |
|---|---|---|
| Lider heartbeat kesildi | alive(i)=False, yeni lider seçilir | 600 ms |
| Yeni intent yayını başlar | min(A\{arıza}) lider olur | ≤100 ms sonra |
| Rank yeniden hesabı | 30 adım (0.6 s) geçiş koruması | 0.6 s |
| APF güncelleme | Arızalı drone APF hesabından çıkar | Anlık |

---

#### 5.13.3 Batarya Kritik

**İzleme parametreleri (safety_monitor.py'den):**

| Eşik | Değer | Tepki |
|---|---|---|
| Uyarı | %25 | Log mesajı (30 s'de bir) |
| Kritik | %15 | `SafetyEvent(BATTERY_CRITICAL)` → SAFETY_HOLD → RTL |
| Event cooldown | 30 s | Aynı event tekrar tetiklenmez |

**Tepki zinciri:**

$$\text{batarya} \leq 15\% \Rightarrow \text{SafetyEvent} \rightarrow \text{local\_fsm: SAFETY\_HOLD} \rightarrow \text{RTL}$$

Severity değeri dinamik hesaplanır:

$$\text{severity} = \min\!\left(1.0,\ \frac{\text{BATTERY\_CRITICAL\_PCT} - \text{pct}}{\text{BATTERY\_CRITICAL\_PCT}} + 0.7\right)$$

Bir drone RTL yaparken diğerleri göreve devam eder (bağımsız karar); lider ise Bully ile değiştirilir.

---

#### 5.13.4 Jeofence İhlali

Drone her 0.2 s (5 Hz) ENU koordinat sınırlarını denetler:

$$\mathcal{F}_{izin} = \{(x,y,z) \mid x \in [-5, 125],\ y \in [-5, 95],\ z \in [0.5, 60]\}\ \text{m}$$

**Erken uyarı:** Sınıra 3 m kala log uyarısı (ihlal olmadan önce).

**İhlal tespitinde:**

$$\text{(x,y,z)} \notin \mathcal{F}_{izin} \Rightarrow \text{SafetyEvent(GEOFENCE\_BREACH)} \rightarrow \text{SAFETY\_HOLD} \rightarrow \text{RTL}$$

Severity merkezden normalize uzaklıkla hesaplanır:

$$\text{severity} = \min\!\left(1.0,\ \frac{d_{merkez}}{d_{max}}\right)$$

Cooldown: 5 s (aynı ihlal tekrar tetiklenmez).

---

#### 5.13.5 Kamera Arızası / Failover

| Durum | Tetikleyici | Yazılım Tepkisi |
|---|---|---|
| Birincil kamera (drone1) DETACH'a girdi | `drone1.state ∈ {DETACH, SAFETY_HOLD, PILOT_OVERRIDE}` | `camera_drone_id = drone2` (anlık) |
| Yedek kamera da erişilemez | QR trigger timeout | waypoint_navigator sonraki QR'a geçer |
| Birincil drone REJOIN'a döndü | `drone1.state == REJOIN` | `camera_drone_id = drone1` (otomatik geri dön) |

3 drone'da kamera bulunması bu senaryoda %100 yedeklilik sağlar.

---

#### 5.13.6 GPS Kaybı / Konum Sensörü Hatası

| Durum | Yazılım Tepkisi |
|---|---|
| MAVROS bağlantısı kesilir | `drone_interface` bağlantı loglar; `local_fsm` SAFETY_HOLD |
| Konum verisi stale (> 1.5 s) | `formation_controller` / `waypoint_navigator` son bilinen konum kullanır |
| Konum verisi stale (> 2.0 s) | `safety_monitor` jeofence kontrolünü devre dışı bırakır (yanlış alarm önleme) |
| ArduCopter GPS loss | ArduCopter kendi iç failsafe'ini devreye alır (EKF failsafe → Land/RTL) |

---

#### 5.13.7 RC Pilot Override (Kill-Switch)

Operatör RC kumandası ile GUIDED dışı bir moda geçerse sistem anında güvenli duruma alınır:

$$\text{armed} \land \text{mode} \notin \{\text{GUIDED, LAND, RTL, BRAKE, AUTO}\} \Rightarrow \text{PILOT\_OVERRIDE}$$

```
PILOT_OVERRIDE başladı:
  - pre_override_state saklanır (geri dönüş için)
  - Otonom setpoint yayını durur (formation_controller çıktısı bloke)
  - RC kumanda TAM KONTROL alır

PILOT_OVERRIDE bitti:
  - pre_override_state'e otomatik dönüş
  - GUIDED mod yeniden aktive edilir
  - Formasyon navigasyonu kaldığı yerden devam eder
```

**Şartname §5.5.4:** RC kumanda **her zaman önceliklidir**; yazılım bunu garanti altına alır.

---

#### 5.13.8 Failsafe Özet Tablosu

| Arıza Tipi | Tespit Süresi | Tepki | Kodu |
|---|---|---|---|
| Drone düşmesi (lider) | 600 ms | Bully → yeni lider | `intent_coordinator.py` |
| Drone düşmesi (takipçi) | 600 ms | Rank güncelle, devam et | `intent_coordinator.py` |
| GCS bağlantı kaybı | 3 s (uyarı) | Son komut korun → RTL | `safety_monitor.py` |
| Batarya kritik (%15) | 200 ms (5Hz) | RTL | `safety_monitor.py` |
| Jeofence ihlali | 200 ms (5Hz) | RTL | `safety_monitor.py` |
| Kamera arızası | Anlık | Yedek drone'a geç | `qr_perception.py` |
| GPS kaybı | 1.5 s (stale) | Son konum / RTL | `drone_interface.py` |
| RC override | Anlık | PILOT_OVERRIDE | `drone_interface.py` |
| Osilasyon | 0.4 s pencere | Slew rate düşür (8s) | `collision_avoidance.py` |

---

### 5.14 Görev Akış Diyagramı

```
[Operatör: h → irtifa gir]  [Operatör: m → QR koordinatları gir]
            │                               │
            ▼                               ▼
    GCS drone_altitude               SetQRMap servisi
    intent_coordinator'a             qr_perception'a
            │                               │
            └───────────────────────────────┘
                                    │
            [Operatör: s → Görevi Başlat]
                                    │
                                    ▼
                        mission_fsm: TaskTrigger(TASK1, start=True)
                                    │
                                    ▼
                        intent_coordinator: IDLE → ARMING
                        SwarmIntent(task=IDLE) → 3 drone'a
                                    │
                        ┌───────────┴─────────────┐
                        ▼           ▼             ▼
                    drone1        drone2        drone3
                local_fsm:    local_fsm:    local_fsm:
                STANDBY→IDLE  STANDBY→IDLE  STANDBY→IDLE
                ARM+GUIDED    ARM+GUIDED    ARM+GUIDED
                TAKEOFF       TAKEOFF       TAKEOFF
                        │
                        ▼
            Tüm drone'lar IDLE rapor etti
            intent_coordinator: ARMING → NAVIGATING
            SwarmIntent(QR_NAVIGATE, QR1, OKBASI, alt=15m)
                        │
                        ▼
            local_fsm × 3: IDLE → FLYING
            formation_controller: Sanal lider QR1'e 3 m/s
            collision_avoidance: APF kuvvetleri 50 Hz
            drone_interface: Altitude Gate (z > 0.5m açılınca)
                        │
            ┌───────────┴───────────────────────────────┐
            │                  QR1'e 5m yaklaşıldı      │
            ▼                                           │
    waypoint_navigator: loiter_cmd=True                 │
    qr_perception: QR JSON çözümlendi                  │
    QRResult(formasyon=V, irtifa=20m, detach=False)    │
            │                                           │
            ▼                                           │
    intent_coordinator: SwarmIntent(QR2, V, alt=20m)  │
                        [QR2→QR3→...→QR6 aynı döngü]──┘
                        │
            ┌───────────┘ QR3'te detach_active=True
            ▼
    SwarmIntent(DETACH, detach_id=2, zone=RED)
    drone2: local_fsm FLYING → DETACH
    precision_landing: zone merkezine hover (5m)
    XY hata < 0.8m → LAND_ZONE → LAND → DISARM_WAIT
            │
            ▼
    REJOIN komutu → drone2: REARM → REJOIN → FLYING
            │
            ▼
    QR6: next_qr_id = 0 → intent_coordinator: RETURNING
    SwarmIntent(RETURN_HOME) → 3 drone RTL → iniş
            │
            ▼
    [Görev Tamamlandı — Tüm drone'lar DISARM]
```

---

## 6. Görev Doğrulama, Simülasyon ve Değerlendirme

### 6.1 Simülasyon Ortamı

| Bileşen | Versiyon / Detay |
|---|---|
| Simülatör | Gazebo Sim 8 (gz-sim) |
| Uçuş Yazılımı | ArduCopter SITL (ArduPilot) |
| ROS2 | Humble Hawksbill |
| Eklenti | ardupilot_gazebo plugin (JSON UDP protokolü) |
| İHA–Gazebo port | 9002 / 9012 / 9022 (drone1/2/3) |
| Koordinat sistemi | ENU (East-North-Up) |
| QR marker boyutu | 120 cm × 120 cm (şartname uyumu) |
| Kontrol frekansları | formation_controller: 50 Hz, waypoint_navigator: 10 Hz, safety_monitor: 5 Hz |

### 6.2 Test 1: Eş Zamanlı Kalkış

**Senaryo:** [s] tuşuna basılmasıyla 3 drone eş zamanlı ARM + kalkış.

| Zaman | Olay |
|---|---|
| t = 0 ms | 3 drone eş zamanlı ARM onayı |
| t = 9 ms | CMD_NAV_TAKEOFF kabul edildi |
| t ≈ 478 ms | formation_controller setpoint göndermeye başlar → Altitude Gate BLOK |
| t ≈ 3 s | Drone'lar 0.5 m geçti → Altitude Gate açıldı |
| t ≈ 8 s | 3 drone 15 m hedef irtifasına ulaştı, formasyon kuruldu |

**Sonuç:** 3 drone eş zamanlı kalkış simülasyonda başarıyla doğrulandı.

### 6.3 Test 2: Üç Formasyon Tipi

Spacing = 5 m, centroid = (0, 0, 15 m) referans alınarak hesaplanan drone konumları:

**Ok Başı (OKBASI):**

| Drone | X (m) | Y (m) | Z (m) |
|---|---|---|---|
| drone1 — rank 0 | +3.33 | 0 | 15 |
| drone2 — rank 1 | −1.67 | −2.5 | 15 |
| drone3 — rank 2 | −1.67 | +2.5 | 15 |

**V Formasyonu:**

| Drone | X (m) | Y (m) | Z (m) |
|---|---|---|---|
| drone1 — rank 0 | +3.33 | 0 | 15 |
| drone2 — rank 1 | −1.67 | −5.0 | 15 |
| drone3 — rank 2 | −1.67 | +5.0 | 15 |

**Çizgi (CIZGI) Formasyonu:**

| Drone | X (m) | Y (m) | Z (m) |
|---|---|---|---|
| drone1 — rank 0 | 0 | +5.0 | 15 |
| drone2 — rank 1 | 0 | 0 | 15 |
| drone3 — rank 2 | 0 | −5.0 | 15 |

**Sonuç:** Formasyon geçişleri Gazebo'da görsel olarak doğrulandı. Slew rate limiter ile geçişler pürüzsüz gerçekleşti.

### 6.4 Test 3: APF Çarpışma Önleme

**Senaryo:** drone2, drone1'e 4 m mesafeye yaklaştı (R_MAX = 8 m içinde).

İtici kuvvet büyüklüğü:

$$\|\mathbf{F}\| = 18.0 \times \left(\frac{1}{4} - \frac{1}{8}\right) \times \frac{1}{16} = 0.141 \text{ m setpoint sapması}$$

TTC = 4 m / 0.5 m·s⁻¹ = 8 s → TTC > 1.5 s → amplifikasyon yok.

**Sonuç:** Drone'lar güvenli mesafeyi korudu. Çarpışma olmadı.

### 6.5 Test 4: Bully Lider Seçimi

**Senaryo:** Aktif görev sırasında drone1 (lider) simülasyonda kapatıldı.

| Zaman | Olay |
|---|---|
| t = 0 ms | drone1 heartbeat kesildi |
| t = 600 ms | `_is_alive(1) = False`; lider seçimi tetiklendi |
| t ≈ 700 ms | drone2 (min(A)) yeni lider; SwarmIntent yayınlamaya başladı |

**Sonuç:** Lider geçişi ~700 ms içinde tamamlandı; formasyon bozulmadan devam etti.

### 6.6 Test 5: Hassas İniş

**Senaryo:** drone2, kırmızı zone'a DETACH.

1. `precision_landing` aktive, zone konumunu aldı
2. Drone 5 m irtifada hover, XY setpoint zone merkezi
3. $e_{xy}$ monoton azaldı; $e_{xy} = 0.62$ m < 0.8 m → hizalandı
4. `local_fsm`: LAND_ZONE → LAND → DISARM_WAIT

**Sonuç:** Drone şartname limitinin (0.8 m) altında XY hata ile indi.

### 6.7 Tespit Edilen Sınırlamalar ve Geliştirme Planı

| Sınırlama | Açıklama | Geliştirme Planı |
|---|---|---|
| QR algılama | Simülasyonda proximity-based fallback; gerçek donanımda kamera gerekli | Fiziksel kamera, pyzbar JSON decode |
| Batarya simülasyonu | Mock tüketim; gerçek batarya topic'i bağlanmadı | `/{ns}/mavros/battery` entegrasyonu |
| GPS bağımlılığı | ENU pozisyon; iç mekânda ek sensör gerekebilir | Optical flow / UWB pozisyon sistemi |

---

## 7. Kaynakça

[1] W. Ren and R. W. Beard, "Consensus seeking in multiagent systems under dynamically changing interaction topologies," *IEEE Transactions on Automatic Control*, vol. 50, no. 5, pp. 655–661, 2005.

[2] P. Lissaman and C. Shollenberger, "Formation flight of birds," *Science*, vol. 168, pp. 1003–1005, 1970. M. A. Lewis and K.-H. Tan, "High precision formation control of mobile robots using virtual structure approach," *Autonomous Robots*, vol. 4, no. 4, pp. 387–403, 1997.

[3] K.-K. Oh, M.-C. Park, and H.-S. Ahn, "A survey of multi-agent formation control," *Automatica*, vol. 53, pp. 424–440, 2015.

[4] O. Khatib, "Real-time obstacle avoidance for manipulators and mobile robots," *International Journal of Robotics Research*, vol. 5, no. 1, pp. 90–98, 1986.

[5] S. Chung, A. Paranjape, P. Dames, S. Shen, and V. Kumar, "A survey on aerial swarm robotics," *IEEE Transactions on Robotics*, vol. 34, no. 4, pp. 837–855, 2018.

[6] E. Sahin, "Swarm robotics: From sources of inspiration to domains of application," in *Proc. Int. Workshop on Swarm Robotics*, Lecture Notes in Computer Science, vol. 3342, pp. 10–20, 2005.

[7] ArduPilot Development Team, *ArduCopter Documentation — GUIDED Mode*, 2024. [Online]. Available: https://ardupilot.org/copter/docs/ac2_guidedmode.html

[8] Open Robotics, *ROS2 Humble Hawksbill Documentation*, 2022. [Online]. Available: https://docs.ros.org/en/humble/

---

*Bu rapor TEKNOFEST 2026 Sürü İHA Yarışması ÖTR şablonuna uygun olarak hazırlanmıştır. Tüm algoritma parametreleri ve matematiksel ifadeler, sistemin kaynak kodundan doğrudan alınmıştır.*
