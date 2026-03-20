# TEKNOFEST 2026 — Failsafe Test Senaryoları

## Ön Koşul
```bash
# 1. Sistemi başlat
ros2 launch my_swarm_pkg swarm_competition.launch.py

# 2. Dashboard açılınca [s] + Enter (3-4 saniye bekle)
# 3. 3 drone uçtuktan sonra testleri çalıştır
```

## Test Sırası

| No | Dosya | Senaryo | Beklenen |
|----|-------|---------|---------|
| 1 | test_rc_fail.py | RC kumanda kaybı | RTL modu |
| 2 | test_gcs_loss.py | YKİ bağlantı kaybı | Otonom devam |
| 3 | test_dds_loss.py | İHA–İHA haberleşme kaybı | Hover → sürü devam |
| 4 | test_battery.py | Batarya kritik | SAFETY_HOLD |
| 5 | test_gps_deny.py | GPS kaybı | Hover (UWB ile) |
| 6 | test_motor_fail.py | Motor arızası | Lider değişimi |

## Çalıştırma (her test ayrı terminal)

```bash
source ~/eren-takim-reposu/install/setup.bash
export ROS_LOCALHOST_ONLY=1

# Test 1
python3 test_scripts/test_rc_fail.py

# Test 2
python3 test_scripts/test_gcs_loss.py

# Test 3
python3 test_scripts/test_dds_loss.py

# Test 4
python3 test_scripts/test_battery.py

# Test 5 (uwb_mock önce başlatılmalı)
python3 test_scripts/uwb_mock.py &
python3 test_scripts/test_gps_deny.py

# Test 6
python3 test_scripts/test_motor_fail.py
```

## Sonuç Dosyaları
Her test `/tmp/test_<isim>_result.txt` dosyasına yazar.

```bash
cat /tmp/test_rc_fail_result.txt
cat /tmp/test_gcs_loss_result.txt
cat /tmp/test_dds_loss_result.txt
cat /tmp/test_battery_result.txt
cat /tmp/test_gps_deny_result.txt
cat /tmp/test_motor_fail_result.txt
```
