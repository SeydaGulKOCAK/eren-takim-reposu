#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    swarm_competition.launch.py                              ║
║         TEKNOFEST 2026 — 3 Drone Senkron Kalkış + Runtime QR Yükleme        ║
║                       İnşaallah Başarılı! 🙏                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 BU LAUNCH DOSYASININ YAPTIĞI:

1️⃣ GAZEBO → Simülasyon dünyası açılır (drone modelleri, QR markerları)
2️⃣ SITL x3 → 3 ArduPilot yazılımsal pilot (arka planda, UDP portlarda)
3️⃣ MAVROS x3 → SITL ile ROS2 arasında köprü
4️⃣ PER-DRONE NODES → drone_interface, local_fsm, intent_coordinator, vb.
5️⃣ GCS NODES → mission_fsm (dashboard), qr_perception (QR algılaması)

💡 SENKRON KALKIŞ:
  - Bully algoritması: drone1 otomatik lider olur
  - intent_coordinator lider → 3 drone'e aynı komut gönderir
  - local_fsm: ARM → TAKEOFF → FLYING (sinkronize)

⚠️ RUNTIME QR YÜKLEMESİ (JÜRİ KOORDİNATLARI):
  - mission_fsm dashboard'dan [m] tuşu → QR koordinat giri ekranı
  - SetQRMap service → qr_perception'a runtime'da waypoint gönder
  - YAML dosyası değiştirilmeye gerek YOK! 

🚀 KULLANIM:
  
  # Terminal 1 - Sistemi Başlat
  cd ~/gz_ws && source install/setup.bash
  ros2 launch my_swarm_pkg swarm_competition.launch.py
  
  # Terminal 2 - Mission FSM Dashboard (birkaç saniye sonra)
  # Otomatik açılacak. Komutlar:
  #   [m] → QR koordinatları gir (jüri verisi)
  #   [s] → TASK1 başlat (3 drone aynı anda kalkar)
  #   [a] → Acil durdur (RTL)
  #   [q] → Çık
"""

import os
import subprocess
from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    TimerAction,
    LogInfo,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
import time


def generate_launch_description():
    """
    Launch açıklaması:
    
    DRONE KONFİGÜRASYONU (sabit, ama QR'lar runtime'da değişir):
    
    Drone   Ev Konumu    SITL UDP Port   MAVROS Namespace
    -----   -----------  ---------------  -----------------
    drone1  (0, 0, 0)    14550            /drone1/
    drone2  (4, 0, 0)    14560            /drone2/
    drone3  (8, 0, 0)    14570            /drone3/
    
    Haritalama:
      drone1_id = 1, sysid = 1
      drone2_id = 2, sysid = 2
      drone3_id = 3, sysid = 3
    """

    # ── DRONE KONFİGÜRASYONU ──────────────────────────────────────────────
    # (namespace, sysid, mavros_udp_port, mp_udp_port, home_x, home_y, home_z)
    # mavros_udp_port: MAVROS bağlantısı (udpclient → MAVROS dinliyor)
    # mp_udp_port    : Mission Planner bağlantısı (udpclient → MP dinliyor)
    DRONE_CONFIGS = [
        ('drone1', 1, 14550, 14551, 7.33,  0.0,  0.0),
        ('drone2', 2, 14560, 14561, 2.33, -2.5,  0.0),
        ('drone3', 3, 14570, 14571, 2.33,  2.5,  0.0),
    ]

    # ── GEOFENCİNG PARAMETRE (Güvenlik) ───────────────────────────────────
    # Yarışma alanının sınırları
    FENCE = {
        'FENCE_X_MIN': '-30.0',
        'FENCE_X_MAX': '125.0',
        'FENCE_Y_MIN': '-30.0',
        'FENCE_Y_MAX': '110.0',
        'FENCE_Z_MIN': '0.5',
        'FENCE_Z_MAX': '60.0',
    }

    # ── ORTAM AYARLARI ────────────────────────────────────────────────────
    # pkg_dir: ament_index ile paketin kaynak dizini bulunur.
    # Workspace adı ne olursa olsun çalışır.
    from ament_index_python.packages import get_package_share_directory
    pkg_dir = get_package_share_directory('my_swarm_pkg')
    # pkg_dir → install/my_swarm_pkg/share/my_swarm_pkg
    # ws      → install/my_swarm_pkg/share/../../../.. → workspace kökü
    ws = os.path.abspath(os.path.join(pkg_dir, '..', '..', '..', '..'))

    # eeprom.bin temizliği — bozuk SITL state'ini önler
    for ep in [
        '/home/beyza/ardupilot/eeprom.bin',
        '/home/beyza/ardupilot/ArduCopter/eeprom.bin',
        '/home/beyza/eeprom.bin',
        os.path.join(ws, 'eeprom.bin'),
    ]:
        try:
            os.remove(ep)
        except Exception:
            pass

    # DDS shared memory temizliği — eski launch'lardan kalan SHM kilitlerini kaldır
    import glob as _glob
    for shm in _glob.glob('/dev/shm/fastrtps_*') + _glob.glob('/dev/shm/Fast_*'):
        try:
            os.remove(shm)
        except Exception:
            pass

    # ROS2 loopback (DDS: sadece localhost arasında haberleşe)
    fastdds_profile = os.path.join(pkg_dir, 'config/fastdds_no_shm.xml')
    env = {
        'ROS_LOCALHOST_ONLY': '1',
        'FASTRTPS_DEFAULT_PROFILES_FILE': fastdds_profile,
        'CYCLONEDDS_URI': 'file://' + os.path.join(pkg_dir, 'config/cyclonedds_localhost.xml'),
        'GZ_SIM_RESOURCE_PATH': ':'.join([
            os.path.join(pkg_dir, 'models'),
            os.path.join(ws, 'src/ardupilot_gazebo/models'),
            os.path.join(ws, 'install/ardupilot_gazebo/share/ardupilot_gazebo/models'),
            os.path.expanduser('~/ardupilot_gazebo/models'),
            os.path.expanduser('~/new_repo_local/gz_ws/src/ardupilot_gazebo/models'),
            os.path.expanduser('~/new_repo_local/gz_ws/install/ardupilot_gazebo/share/ardupilot_gazebo/models'),
            '/usr/share/gz/gz-sim8/models',
        ]),
        'GZ_SIM_SYSTEM_PLUGIN_PATH': os.path.expanduser('~/ardupilot_gazebo/build'),
    }

    args = []

    # ═══════════════════════════════════════════════════════════════════════
    # 🛡️ KORUMA: Bir süreç çökerse sistemi KAPATMA, sadece logla
    # ros2 launch varsayılan davranışı: bir süreç ölünce hepsini öldür
    # Bu kural bunu engeller — Gazebo ve diğer süreçler ayakta kalır
    # ═══════════════════════════════════════════════════════════════════════
    args.append(
        RegisterEventHandler(
            OnProcessExit(
                on_exit=[LogInfo(msg='⚠️ Bir süreç çıktı ama sistem devam ediyor...')]
            )
        )
    )

    # ═══════════════════════════════════════════════════════════════════════
    # 0️⃣ ÖNCE: Eski FastRTPS shm dosyalarını temizle (stale mesaj sorunu önleme)
    # ═══════════════════════════════════════════════════════════════════════
    args.append(
        ExecuteProcess(
            cmd=['bash', '-c', 'rm -f /dev/shm/fastrtps_* 2>/dev/null; echo "FastRTPS shm temizlendi"'],
            output='screen',
        )
    )

    # ═══════════════════════════════════════════════════════════════════════
    # BAŞLANGIC BANNER
    # ═══════════════════════════════════════════════════════════════════════
    args.append(
        LogInfo(msg=[
            '\n╔════════════════════════════════════════════════════════════╗\n'
            '║          🚀 SWARM COMPETITION LAUNCH (3 Drone) 🚀            ║\n'
            '║               İnşaallah Başarılı Uçuş! 🙏                   ║\n'
            '╚════════════════════════════════════════════════════════════╝\n'
            '\n📍 ADIM ADIM NE OLACAK:\n'
            '  1️⃣  Gazebo simülasyon dünyası açılıyor...\n'
            '  2️⃣  3x ArduPilot SITL başlatılıyor (15 saniye bekleme)\n'
            '  3️⃣  3x MAVROS bağlantısı kurulacak\n'
            '  4️⃣  Swarm node\'ları spawn edilecek (drone_interface, local_fsm, ...)\n'
            '  5️⃣  GCS dashboard (mission_fsm) terminal açılacak\n'
            '\n⚠️  JÜRİ KOORDİNATLARI (YARN GÜNÜ):\n'
            '  → mission_fsm dashboard\'da [m] tuşuna basın\n'
            '  → QR koordinatlarını giriniz (x,y,z formatı)\n'
            '  → SetQRMap service otomatik gönderilir\n'
            '  → [s] ile mission başlatın\n'
            '\n🎯 SENKRON KALKIŞ:\n'
            '  → Bully algoritması drone1\'i lider yapar\n'
            '  → intent_coordinator 3 drone\'e aynı komut gönderir\n'
            '  → local_fsm: IDLE → ARMING → FLYING (eşzamanlı)\n\n'
        ])
    )

    # ═══════════════════════════════════════════════════════════════════════
    # 1️⃣ GAZEBO
    # ═══════════════════════════════════════════════════════════════════════
    world_file = os.path.join(pkg_dir, 'worlds', 'world_task1_qr_static.sdf')
    
    args.append(
        LogInfo(msg='🌍 GAZEBO başlatılıyor...')
    )

    args.append(
        ExecuteProcess(
            cmd=[
                'gz', 'sim',
                '-r',  # Paused başlasın (drone\'lar hazır olana kadar)
                world_file
            ],
            output='screen',
            additional_env=env,
        )
    )

    # ═══════════════════════════════════════════════════════════════════════
    # 2️⃣ ArduPilot SITL x3
    # ═══════════════════════════════════════════════════════════════════════
    sitl_procs = []

    for ns, sysid, mavros_port, mp_port, hx, hy, hz in DRONE_CONFIGS:
        idx = sysid - 1  # -I parameter için (0, 1, 2)

        args.append(
            LogInfo(msg=f'🛩️  SITL drone{sysid} (MAVROS UDP:{mavros_port} / MP UDP:{mp_port}) başlatılıyor...')
        )

        # Timer: SITL'ler sırayla başlasın (boğulma önleme)
        sitl_procs.append(
            TimerAction(
                period=10.0 + idx * 2.0,  # Gazebo yüklendikten sonra. drone1: 10s, drone2: 12s, drone3: 14s
                actions=[
                    ExecuteProcess(
                        cmd=[
                            os.path.expanduser('~/ardupilot/build/sitl/bin/arducopter'),
                            '--model', 'json',
                            '--speedup', '1',
                            f'-I{idx}',
                            '--sysid', str(sysid),
                            '--slave', '0',
                            '--defaults',
                            os.path.expanduser(
                                '~/ardupilot/Tools/autotest/default_params/copter.parm')
                            + ',' + os.path.join(pkg_dir, 'config/sitl_sr0.parm'),
                            '--sim-address=127.0.0.1',
                            '--home', f'-35.363262,149.165237,584.0,0.0',
                            # SERIAL0 → MAVROS UDP
                            '--serial0', f'udpclient:127.0.0.1:{mavros_port}',
                            # SERIAL1 → Mission Planner UDP
                            '--serial1', f'udpclient:127.0.0.1:{mp_port}',
                        ],
                        cwd=os.path.expanduser('~/ardupilot'),
                        output='log',
                        additional_env=env,
                    )
                ]
            )
        )

    args.extend(sitl_procs)

    # Bekleme: SITL'ler hazırlanması için
    args.append(
        LogInfo(msg='⏳ SITL hazırlığı için 15 saniye bekleniyor...')
    )

    # ═══════════════════════════════════════════════════════════════════════
    # 3️⃣ MAVROS x3
    # ═══════════════════════════════════════════════════════════════════════
    mavros_nodes = []

    for ns, sysid, mavros_port, mp_port, hx, hy, hz in DRONE_CONFIGS:
        args.append(
            LogInfo(msg=f'🔌 MAVROS {ns} (sysid={sysid}, UDP:{mavros_port}) kurulacak...')
        )

        mavros_nodes.append(
            TimerAction(
                period=25.0 + (sysid - 1) * 2.0,  # SITL hazır olduktan sonra (drone1: 25s, drone2: 27s, drone3: 29s)
                actions=[
                    Node(
                        package='mavros',
                        executable='mavros_node',
                        namespace=f'{ns}/mavros',
                        parameters=[{
                            'fcu_url': f'udp://:{mavros_port}@',
                            'tgt_system': sysid,
                        }, os.path.join(pkg_dir, 'config/mavros_config.yaml')],
                        output='log',
                        additional_env=env,
                    )
                ]
            )
        )

    args.extend(mavros_nodes)

    # ═══════════════════════════════════════════════════════════════════════
    # 4️⃣ PER-DRONE NODES (drone_interface, local_fsm, intent_coordinator, ...)
    # ═══════════════════════════════════════════════════════════════════════
    per_drone_nodes = []

    for ns, sysid, mavros_port, mp_port, hx, hy, hz in DRONE_CONFIGS:
        delay = 40.0 + (sysid - 1) * 1.0
        
        env_vars = {
            'DRONE_NS': ns,
            'DRONE_ID': str(sysid),
            'SWARM_SIZE': '3',
            'HOME_X': str(hx),
            'HOME_Y': str(hy),
            'HOME_Z': str(hz),
        }
        env_vars.update(FENCE)
        env_vars.update(env)

        # ── drone_interface (MAVROS köprüsü) ──────────────────────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='drone_interface',
                        namespace=ns,
                        parameters=[{'drone_id': sysid}],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── local_fsm (drone durum makinesi) ──────────────────────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.1,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='local_fsm',
                        namespace=ns,
                        parameters=[{'drone_id': sysid}],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── intent_coordinator (lider seçimi + QR dağıtımı) ──────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.2,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='intent_coordinator',
                        namespace=ns,
                        parameters=[{
                            'drone_id': sysid,
                            'num_drones': 3,
                            'camera_drone_id': 3,
                        }],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── formation_controller (virtual structure) ──────────────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.3,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='formation_controller',
                        namespace=ns,
                        parameters=[{
                            'drone_id': sysid,
                            'num_drones': 3,
                            'formation_type': 'OKBASI',
                            'drone_spacing': 6.0,
                        }],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── collision_avoidance (APF çarpışma önleme) ────────────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.4,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='collision_avoidance',
                        namespace=ns,
                        parameters=[{
                            'drone_id': sysid,
                            'num_drones': 3,
                        }],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── waypoint_navigator (QR→QR rota takibi — sadece lider aktif) ──
        # Her drone'da çalışır; lider olmayan _nav_loop'ta hemen return eder.
        # Lider değişince yeni lider otomatik devralır. (GCS'ye bağımlılık yok → §5.3)
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.5,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='waypoint_navigator',
                        namespace=ns,
                        parameters=[{
                            'drone_id': sysid,
                            'num_drones': 3,
                        }],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── precision_landing (hassas iniş — sadece DETACH drone aktif) ──
        # Her drone'da çalışır; sadece intent.detach_drone_id == kendi ID olunca aktif.
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.6,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='precision_landing',
                        namespace=ns,
                        parameters=[{
                            'drone_id': sysid,
                            'num_drones': 3,
                        }],
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

        # ── safety_monitor (batarya + geofence + heartbeat) ──────────────
        per_drone_nodes.append(
            TimerAction(
                period=delay + 0.7,
                actions=[
                    Node(
                        package='my_swarm_pkg',
                        executable='safety_monitor',
                        namespace=ns,
                        additional_env=env_vars,
                        output='log',
                    )
                ]
            )
        )

    # ── qr_perception — ONBOARD: kamera drone (drone3) üzerinde çalışır ────
    # §5.3 dağıtıklık: GCS'den bağımsız, hakem GCS'yi kesince QR okuma durmuyor.
    # Birincil kamera: drone3, yedek: drone2 (camera_drone_id parametresi ile).
    # Simülasyonda aynı makinede çalışır ama mantıksal olarak drone3'e aittir.
    CAMERA_DRONE_NS   = 'drone3'
    CAMERA_DRONE_ID   = 3
    BACKUP_CAMERA_ID  = 2
    camera_env = {
        'DRONE_NS': CAMERA_DRONE_NS,
        'DRONE_ID': str(CAMERA_DRONE_ID),
    }
    camera_env.update(env)

    args.append(
        LogInfo(msg='👁️  QR Perception ONBOARD (drone3) başlatılıyor...')
    )
    per_drone_nodes.append(
        TimerAction(
            period=45.0,
            actions=[
                Node(
                    package='my_swarm_pkg',
                    executable='qr_perception',
                    namespace=CAMERA_DRONE_NS,
                    parameters=[{
                        'team_id': 'team1',
                        'camera_drone_id': CAMERA_DRONE_ID,
                        'backup_camera_drone_id': BACKUP_CAMERA_ID,
                        'num_drones': 3,
                        'trigger_radius': 5.0,
                    }],
                    output='screen',
                    additional_env=camera_env,
                )
            ]
        )
    )

    # ── color_zone_detector — kamera ile HSV renk zonu tespiti ───────────
    # Drone2 + Drone3 kamerasını dinler, /perception/color_zones yayınlar.
    # qr_perception.py'deki YAML tabanlı sabit koordinatların yerini alır.
    color_zone_env = dict(env)
    per_drone_nodes.append(
        TimerAction(
            period=46.0,
            actions=[
                Node(
                    package='my_swarm_pkg',
                    executable='color_zone_detector',
                    parameters=[{
                        'camera_drone_id': 3,
                        'backup_drone_id': 2,
                        'publish_hz': 5.0,
                        'min_area_px': 500,
                        'camera_fov_h_deg': 60.0,
                        'img_width': 640,
                        'img_height': 480,
                        'zone_radius': 2.0,
                    }],
                    output='log',
                    additional_env=color_zone_env,
                )
            ]
        )
    )

    # ros_gz_image bridge devre dışı — paket kurulu değil, formasyon testi için gerekli değil
    # for drone_id in [1, 2, 3]:
    #     per_drone_nodes.append(
    #         TimerAction(
    #             period=48.0,
    #             actions=[
    #                 Node(
    #                     package='ros_gz_image',
    #                     executable='image_bridge',
    #                     arguments=[f'/drone{drone_id}/camera/image'],
    #                     remappings=[(
    #                         f'/drone{drone_id}/camera/image',
    #                         f'/drone{drone_id}/camera/image_raw'
    #                     )],
    #                     output='log',
    #                     additional_env=dict(env),
    #                 )
    #             ]
    #         )
    #     )

    args.extend(per_drone_nodes)

    # ═══════════════════════════════════════════════════════════════════════
    # 5️⃣ GCS NODES (mission_fsm — sadece dashboard/tetik)
    # ═══════════════════════════════════════════════════════════════════════
    gcs_nodes = []

    # ── mission_fsm (GCS dashboard + TASK1/TASK2 başlatma) ────────────────
    args.append(
        LogInfo(msg='🎮 MISSION FSM DASHBOARD açılıyor (yeni xterm\'de)...')
    )

    # mission_fsm xterm geçici olarak devre dışı — formasyon testi için gerekli değil
    # gcs_nodes.append(
    #     TimerAction(
    #         period=47.0,
    #         actions=[
    #             ExecuteProcess(
    #                 cmd=[
    #                     'xterm',
    #                     '-title', 'Mission FSM Dashboard',
    #                     '-e', 'bash', '-c',
    #                     f'source {ws}/install/setup.bash && '
    #                     f'export GZ_SIM_RESOURCE_PATH={env["GZ_SIM_RESOURCE_PATH"]} && '
    #                     f'export GZ_SIM_SYSTEM_PLUGIN_PATH={env["GZ_SIM_SYSTEM_PLUGIN_PATH"]} && '
    #                     f'export ROS_LOCALHOST_ONLY=1 && '
    #                     f'export FASTRTPS_DEFAULT_PROFILES_FILE={fastdds_profile} && '
    #                     f'export CYCLONEDDS_URI={env["CYCLONEDDS_URI"]} && '
    #                     f'ros2 run my_swarm_pkg mission_fsm'
    #                 ],
    #                 output='screen',
    #                 additional_env=env,
    #             )
    #         ]
    #     )
    # )

    args.extend(gcs_nodes)

    # ═══════════════════════════════════════════════════════════════════════
    # 6️⃣ LOCAL_POSITION_NED STREAM AKTİFLEŞTİR
    #    25s sonra MAVROS cmd/command servisiyle ArduPilot'a
    #    MAV_CMD_SET_MESSAGE_INTERVAL (511) gönderir → local_position/pose çalışır
    # ═══════════════════════════════════════════════════════════════════════
    # activate_streams geçici olarak devre dışı — formasyon testi için gerekli değil
    # stream_script = os.path.join(pkg_dir, 'config/activate_streams.py')
    # args.append(
    #     TimerAction(
    #         period=60.0,
    #         actions=[
    #             ExecuteProcess(
    #                 cmd=['python3', stream_script],
    #                 output='screen',
    #                 additional_env=env,
    #             )
    #         ]
    #     )
    # )

    # ═══════════════════════════════════════════════════════════════════════
    # KAPANIŞ BANNER
    # ═══════════════════════════════════════════════════════════════════════
    args.append(
        TimerAction(
            period=12.0,
            actions=[
                LogInfo(msg=[
                    '\n╔════════════════════════════════════════════════════════════╗\n'
                    '║              ✅ SİSTEM BAŞLATILDI - İNŞAALLAH! 🙏            ║\n'
                    '╚════════════════════════════════════════════════════════════╝\n'
                    '\n📊 DASHBOARD KOMUTLARI:\n'
                    '  [m]  → Jüri QR Koordinatlarını Gir (runtime setup)\n'
                    '  [s]  → TASK1 Başlat (3 drone senkron kalkar)\n'
                    '  [a]  → Acil Durdur (RTL Mode)\n'
                    '  [d]  → Durum Göster\n'
                    '  [q]  → Çık\n'
                    '\n💡 İPUÇLARİ:\n'
                    '  • Log dosyaları: ~/.swarm_logs/\n'
                    '  • Gazebo 4 saniye sonra oynatmaya başlayabilir\n'
                    '  • Drone konumları /drone{i}/pose topic\'inde\n'
                    '  • Intent mesajları /swarm/intent topic\'inde\n\n'
                ])
            ]
        )
    )

    # ═══════════════════════════════════════════════════════════════════════
    return LaunchDescription(args)
    # ═══════════════════════════════════════════════════════════════════════


if __name__ == '__main__':
    describe = generate_launch_description()
    print(describe)
