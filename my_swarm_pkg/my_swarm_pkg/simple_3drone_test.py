#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════╗
║    3 DRONE SENKRON UÇUŞ TESTİ - Basit Versiyon            ║
║    İnşaallah 3 drone aynı anda kalkar! 🙏                 ║
╚════════════════════════════════════════════════════════════╝

AMAÇ:
  1. 3 drone aynı anda ARM olsun
  2. 3 drone aynı anda TAKEOFF yapsın (başlangıç formasyonu)
  3. Jüri QR koordinatı girilsin
  4. 3 drone formasyonu koruyarak o koordinata gitsin

FORMATION:
  drone1: (0, 0, 0)     → Lider (orta)
  drone2: (4, 0, 0)     → Sağda 4m
  drone3: (8, 0, 0)     → Sağda 8m
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL
import time


class Simple3DroneTest(Node):
    """3 drone'u senkron uçur."""

    def __init__(self):
        super().__init__('simple_3drone_test')
        
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║   3 DRONE SENKRON UÇUŞ TESTİ BAŞLATILIYOR...          ║")
        print("║   İnşaallah başarılı olur! 🙏                         ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        # Drone state subscribers
        self.drone_states = {1: None, 2: None, 3: None}
        
        for drone_id in [1, 2, 3]:
            self.create_subscription(
                State,
                f'/drone{drone_id}/mavros/state',
                lambda msg, d=drone_id: self._state_callback(d, msg),
                10
            )
        
        # Setpoint publishers (her drone için)
        self.setpoint_pubs = {}
        for drone_id in [1, 2, 3]:
            self.setpoint_pubs[drone_id] = self.create_publisher(
                PoseStamped,
                f'/drone{drone_id}/mavros/setpoint_position/local',
                10
            )
        
        # Service clients
        self.arm_clients = {}
        self.mode_clients = {}
        self.takeoff_clients = {}
        
        for drone_id in [1, 2, 3]:
            self.arm_clients[drone_id] = self.create_client(
                CommandBool,
                f'/drone{drone_id}/mavros/cmd/arming'
            )
            self.mode_clients[drone_id] = self.create_client(
                SetMode,
                f'/drone{drone_id}/mavros/set_mode'
            )
            self.takeoff_clients[drone_id] = self.create_client(
                CommandTOL,
                f'/drone{drone_id}/mavros/cmd/takeoff'
            )
        
        print("✅ Node başlatıldı, MAVROS bağlantıları kontrol ediliyor...")
        
        # Formation offsets (lider drone1'e göre)
        self.formation_offsets = {
            1: (0.0, 0.0, 0.0),   # Lider orta
            2: (0.0, 4.0, 0.0),   # Sağda 4m
            3: (0.0, 8.0, 0.0),   # Sağda 8m
        }
        
        # Timer: setpoint yayını (20 Hz)
        self.create_timer(0.05, self._publish_setpoints)
        
        # Current target positions
        self.target_positions = {
            1: [0.0, 0.0, 0.0],
            2: [0.0, 4.0, 0.0],
            3: [0.0, 8.0, 0.0],
        }
    
    def _state_callback(self, drone_id, msg):
        """MAVROS state güncellemesi."""
        self.drone_states[drone_id] = msg
    
    def _publish_setpoints(self):
        """Her drone için setpoint yayınla (OFFBOARD mode için gerekli)."""
        for drone_id in [1, 2, 3]:
            pose = PoseStamped()
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.header.frame_id = "map"
            
            pose.pose.position.x = self.target_positions[drone_id][0]
            pose.pose.position.y = self.target_positions[drone_id][1]
            pose.pose.position.z = self.target_positions[drone_id][2]
            
            self.setpoint_pubs[drone_id].publish(pose)
    
    def wait_for_mavros(self):
        """MAVROS bağlantısını bekle."""
        print("\n⏳ MAVROS bağlantısı bekleniyor (3 drone)...")
        
        timeout = 30  # saniye
        start_time = time.time()
        
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            
            all_connected = all(
                state is not None and state.connected 
                for state in self.drone_states.values()
            )
            
            if all_connected:
                print("✅ Tüm drone'ler MAVROS'a bağlı!")
                return True
            
            if time.time() - start_time > timeout:
                print("❌ Timeout! MAVROS bağlantısı kurulamadı.")
                return False
        
        return False
    
    def arm_all_drones(self):
        """3 drone'u aynı anda ARM et."""
        print("\n🔧 ARM komutu gönderiliyor (3 drone)...")
        
        # Önce OFFBOARD mode'a geç
        for drone_id in [1, 2, 3]:
            req = SetMode.Request()
            req.custom_mode = "OFFBOARD"
            
            future = self.mode_clients[drone_id].call_async(req)
            rclpy.spin_until_future_complete(self, future, timeout_sec=2.0)
        
        print("✅ OFFBOARD mode ayarlandı")
        time.sleep(1)
        
        # Şimdi ARM et (AYNI ANDA!)
        futures = []
        for drone_id in [1, 2, 3]:
            req = CommandBool.Request()
            req.value = True
            future = self.arm_clients[drone_id].call_async(req)
            futures.append(future)
        
        # Hepsini bekle
        for future in futures:
            rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        
        print("✅ 3 drone ARM edildi! (motorlar dönüyor)")
        time.sleep(2)
    
    def takeoff_all_drones(self, altitude=15.0):
        """3 drone aynı anda kalkış yapsın."""
        print(f"\n🚀 TAKEOFF komutu (Z={altitude}m) - SENKRON KALKIŞ!")
        
        # Hedef pozisyonları ayarla (Z yüksekliği)
        for drone_id in [1, 2, 3]:
            offset = self.formation_offsets[drone_id]
            self.target_positions[drone_id] = [
                offset[0],
                offset[1],
                altitude  # Hepsi aynı yüksekliğe
            ]
        
        print("✅ Setpoint'ler güncellendi, drone'ler yükseliyor...")
        
        # 10 saniye bekle (kalkış tamamlansın)
        for i in range(10):
            rclpy.spin_once(self, timeout_sec=0.5)
            print(f"   ⏱️  {i+1}/10 saniye...")
        
        print("✅ TAKEOFF tamamlandı! (3 drone havada)")
    
    def fly_to_qr_coordinate(self):
        """Jüri QR koordinatına git (formasyonu koru)."""
        print("\n📍 JÜRİ QR KOORDİNATI GİRİŞİ")
        print("════════════════════════════════════════")
        
        try:
            qr_input = input("QR1 koordinatı (x,y,z): ").strip()
            parts = qr_input.split(',')
            
            if len(parts) != 3:
                print("❌ Format: x,y,z şeklinde giriniz!")
                return
            
            qr_x = float(parts[0])
            qr_y = float(parts[1])
            qr_z = float(parts[2])
            
            print(f"\n✅ Hedef: ({qr_x}, {qr_y}, {qr_z})")
            print("🚁 3 drone formasyonu koruyarak gidiyor...\n")
            
            # Formation offset'leri uygula
            for drone_id in [1, 2, 3]:
                offset = self.formation_offsets[drone_id]
                
                self.target_positions[drone_id] = [
                    qr_x + offset[0],
                    qr_y + offset[1],
                    qr_z + offset[2]
                ]
                
                print(f"   drone{drone_id}: ({self.target_positions[drone_id][0]:.1f}, "
                      f"{self.target_positions[drone_id][1]:.1f}, "
                      f"{self.target_positions[drone_id][2]:.1f})")
            
            # 30 saniye bekle (hedefe varma süresi)
            print("\n⏱️  Hedefe doğru gidiyor (30 saniye)...")
            for i in range(30):
                rclpy.spin_once(self, timeout_sec=0.5)
                if i % 5 == 0:
                    print(f"   {i}/30 saniye geçti...")
            
            print("\n✅ İnşaallah QR koordinatına ulaştılar! 🎯")
            
        except ValueError:
            print("❌ Koordinat formatı hatalı!")
        except KeyboardInterrupt:
            print("\n⛔ İptal edildi.")


def main():
    """Ana fonksiyon."""
    rclpy.init()
    
    node = Simple3DroneTest()
    
    try:
        # 1. MAVROS bağlantısını bekle
        if not node.wait_for_mavros():
            print("❌ MAVROS bağlanamadı, çıkılıyor.")
            return
        
        time.sleep(2)
        
        # 2. ARM et (3 drone aynı anda)
        node.arm_all_drones()
        
        # 3. TAKEOFF (senkron kalkış)
        node.takeoff_all_drones(altitude=15.0)
        
        # 4. Jüri QR koordinatına git
        node.fly_to_qr_coordinate()
        
        print("\n════════════════════════════════════════")
        print("✅ TEST TAMAMLANDI!")
        print("════════════════════════════════════════\n")
        
        # HOVER modda kal
        print("🔄 HOVER modda kalıyor (Ctrl+C ile çık)...")
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.5)
    
    except KeyboardInterrupt:
        print("\n⛔ Kullanıcı durdurdu.")
    
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
