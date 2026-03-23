# Kullanim Rehberi (Beyza icin)

## 1. Simulasyonu Baslatma

```bash
cd ~/gz_ws
colcon build
source install/setup.bash
ros2 launch my_swarm_pkg swarm_competition.launch.py
```

Terminalde su mesajlari gorene kadar bekle (~40-50sn):
```
EKF3 IMU0 ... is using GPS
```
Bu mesaj **3 drone icin de** gelmeli. Gelmeden devam etme!

## 2. Simulasyonu Kapatma

```bash
pkill -9 -f ardupilot
pkill -9 -f mavros
pkill -9 -f gz
pkill -9 -f parameter_bridge
pkill -9 -f ros2
```

**ONEMLI:** Test sonrasi tekrar test yapacaksan MUTLAKA simulasyonu kapat ve yeniden baslat!

---

## 3. Drone Pozisyonlari

Dronelar bu pozisyonlarda baslar (global frame):

| Drone  | X     | Y     |
|--------|-------|-------|
| drone1 | 7.33  | 0.0   |
| drone2 | 2.33  | -2.5  |
| drone3 | 2.33  | 2.5   |

---

## 4. SETPOINT PIPELINE (EN ONEMLI KISIM!)

```
  Senin kodun → /{ns}/setpoint_raw    (hedef konum)
                      |
                      v
            collision_avoidance         (ORCA carpisma onleme)
                      |
                      v
               /{ns}/setpoint_final    (guvenli konum)
                      |
                      v
              drone_interface           (MAVROS'a gonderir)
                      |
                      v
                  ArduPilot → Drone ucar!
```

### KURAL: Drone'u hareket ettirmek icin `/{ns}/setpoint_raw`'a yaz!

```python
# DOGRU — carpisma onleme AKTIF:
pub = node.create_publisher(PoseStamped, '/drone1/setpoint_raw', 10)

# YANLIS — carpisma onleme YOK, dronelar CARPISIR:
pub = node.create_publisher(PoseStamped, '/drone1/mavros/setpoint_position/local', 10)
```

---

## 5. Droneları Elle Kaldirma (ARM + TAKEOFF)

Eger kendi test scriptinden droneları kaldirmak istiyorsan:

```python
#!/usr/bin/env python3
import time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, StreamRate
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

HOVER_ALT = 10.0

def main():
    rclpy.init()
    node = rclpy.create_node('my_test')

    def servis_cagir(srv_type, topic, req):
        cli = node.create_client(srv_type, topic)
        if not cli.wait_for_service(timeout_sec=5.0):
            print(f'  SERVIS YOK: {topic}')
            return None
        fut = cli.call_async(req)
        t = time.time()
        while time.time() - t < 5.0:
            rclpy.spin_once(node, timeout_sec=0.05)
            if fut.done():
                return fut.result()
        return None

    # Stream rate ayarla (konum verisi gelsin)
    for i in range(1, 4):
        req = StreamRate.Request()
        req.stream_id = 0
        req.message_rate = 10
        req.on_off = True
        servis_cagir(StreamRate, f'/drone{i}/mavros/set_stream_rate', req)

    # 15sn bekle (pozisyon verisi gelsin)
    print('Pozisyon verisi bekleniyor (15sn)...')
    t = time.time()
    while time.time() - t < 15.0:
        rclpy.spin_once(node, timeout_sec=0.05)

    # GUIDED moda gec
    print('GUIDED moda geciliyor...')
    for i in range(1, 4):
        req = SetMode.Request()
        req.custom_mode = 'GUIDED'
        servis_cagir(SetMode, f'/drone{i}/mavros/set_mode', req)

    time.sleep(0.5)

    # ARM
    print('ARM ediliyor...')
    for i in range(1, 4):
        req = CommandBool.Request()
        req.value = True
        servis_cagir(CommandBool, f'/drone{i}/mavros/cmd/arming', req)

    time.sleep(0.5)

    # TAKEOFF
    print(f'TAKEOFF {HOVER_ALT}m...')
    for i in range(1, 4):
        req = CommandTOL.Request()
        req.altitude = HOVER_ALT
        servis_cagir(CommandTOL, f'/drone{i}/mavros/cmd/takeoff', req)

    # Kalkis bekle
    print('Kalkis bekleniyor (25sn)...')
    t = time.time()
    while time.time() - t < 25.0:
        rclpy.spin_once(node, timeout_sec=0.05)

    print('Dronelar havada! Simdi setpoint_raw ile hedef gonderebilirsin.')

    # ORNEK: Drone1'i (10, 5, 10) konumuna gonder
    pub = node.create_publisher(PoseStamped, '/drone1/setpoint_raw', 10)
    msg = PoseStamped()
    msg.header.frame_id = 'map'
    msg.pose.position.x = 10.0
    msg.pose.position.y = 5.0
    msg.pose.position.z = 10.0
    msg.pose.orientation.w = 1.0

    # 20Hz yayinla (en az 2Hz olmali)
    print('Setpoint gonderiliyor...')
    for _ in range(200):  # 10sn
        msg.header.stamp = node.get_clock().now().to_msg()
        pub.publish(msg)
        rclpy.spin_once(node, timeout_sec=0.05)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 6. Onemli Topic'ler

### Okunan (Subscribe) Topic'ler

| Topic | Tip | Ne ise yarar |
|-------|-----|-------------|
| `/{ns}/pose` | PoseStamped | Drone konumu (global frame) |
| `/{ns}/velocity` | TwistStamped | Drone hizi (m/s) |
| `/{ns}/mavros/state` | State | ARM ve mod durumu |
| `/{ns}/local_state` | LocalState | Drone durumu (FLYING, LANDING vb.) |

### Yazilan (Publish) Topic'ler

| Topic | Tip | Ne ise yarar |
|-------|-----|-------------|
| `/{ns}/setpoint_raw` | PoseStamped | Hedef konum gonder (ORCA isler) |
| `/{ns}/local_state` | LocalState | Drone durumunu yayinla |

`{ns}` yerine `drone1`, `drone2`, `drone3` yaz.

---

## 7. LocalState FLYING Yayini

Collision avoidance'in calismasi icin her drone'un durumu **FLYING** olmali.
Normal gorevde `local_fsm` bunu otomatik yapar.
Test sirasinda kendin yayinlaman gerekir:

```python
from swarm_msgs.msg import LocalState

# Her drone icin 10Hz yayinla
for i in range(1, 4):
    pub = node.create_publisher(LocalState, f'/drone{i}/local_state', 10)
    msg = LocalState()
    msg.drone_id = i
    msg.state = 'FLYING'
    pub.publish(msg)
```

---

## 8. Sik Karsilasilan Hatalar

| Hata | Cozum |
|------|-------|
| `No module named 'swarm_msgs'` | `source ~/gz_ws/install/setup.bash` calistir |
| Dronelar kalkmiyor | EKF mesajlarini bekle (~40-50sn) |
| Dronelar ayni yerde gorunuyor | Simulasyonu tamamen kapat, yeniden baslat |
| Servis bulunamadi | Launch dosyasinin calistiginden emin ol |

---

## 9. Carpisma Onleme Nasil Calisiyor?

ORCA (Optimal Reciprocal Collision Avoidance) algoritmasi kullaniliyor.
- Her drone komsularini izler
- Hiz uzayinda guvenli hiz hesaplar
- 3 katmanli savunma:
  1. **ORCA LP solver** — matematiksel carpisma onleme
  2. **Hiz sinirla** — yakinlastikca yavasla
  3. **Hard safety** — 4m altinda acil kacis

**Sen hicbir sey yapmana gerek yok!** `setpoint_raw`'a yaz, gerisini ORCA halleder.

---

## 10. Dosya Yapisi

```
my_swarm_pkg/
├── launch/
│   └── swarm_competition.launch.py    # Simulasyonu baslatir
├── my_swarm_pkg/
│   ├── drone_interface.py             # MAVROS koprüsu
│   ├── collision_avoidance.py         # ORCA carpisma onleme
│   ├── local_fsm.py                   # Drone durum makinesi
│   ├── formation_controller.py        # Formasyon hesaplama
│   ├── qr_perception.py              # QR kod okuma
│   └── ...
├── scripts/
│   └── test_collision_avoidance.py    # Carpisma testi
└── config/
    └── qr_map.yaml                    # QR nokta haritasi
```
