#!/usr/bin/env python3
"""
TEKNOFEST 2026 — Formasyon Testi (v4 — Düzgün Çalışan)
========================================================
ÖNEMLİ NOTLAR:
  - Her drone'un local frame'i KENDİ başlangıç noktasında (0,0)
  - Bu yüzden formasyon ofseti = drone'un KENDİ origin'inden ne kadar kayacağı
  - Tüm dronlara AYNI ofseti gönderirsek, hepsi aynı yöne gider → formasyon OLMAZ
  - ÇÖZÜM: Her drone'a kendi pozisyonundan göreceli ofset gönder

FORMASYON OFSETLERİ (Şartname):
  OKBASI: Lider öne, kanatlar dar açıyla arkada
  V:      Lider daha öne, kanatlar geniş açıyla arkada
  CIZGI:  Yan yana dizilim
"""

import math, time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, StreamRate
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import NavSatFix

HOVER_ALT = 10.0
SPACING   = 5.0
R_SAFE    = 3.0   # çarpışma önleme mesafesi (m)
K_REP     = 1.5   # itici kuvvet kazancı

BEST_EFFORT = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST, depth=10)

# Formasyon ofsetleri — metre cinsinden (ileri, sol)
# rank0 = lider (drone1, min ID), rank1 = drone2, rank2 = drone3
OFFSETS = {
    'OKBASI': {
        # Ok başı: Lider ÖNDE (ok ucu), takipçiler ARKADA yanlarda  >
        1: (+2/3,  0.0),   # lider: önde (ok ucu)
        2: (-1/3, -0.5),   # sol-arka kanat
        3: (-1/3, +0.5),   # sağ-arka kanat
    },
    'V': {
        # V formasyonu: Lider ARKADA (V'nin dibi), takipçiler ÖNDE yanlarda  <
        1: (-2/3,  0.0),   # lider: arkada (V'nin alt ucu)
        2: (+1/3, -0.5),   # sol-ön kanat (V'nin sol kolu)
        3: (+1/3, +0.5),   # sağ-ön kanat (V'nin sağ kolu)
    },
    'CIZGI': {
        # Çizgi: Yan yana dizilim  ---
        1: ( 0.0,  0.0),   # orta
        2: ( 0.0, -1.0),   # sol
        3: ( 0.0, +1.0),   # sağ
    },
}


def gps_to_meter(lat1, lon1, lat2, lon2):
    """İki GPS noktası arası metre cinsinden (dx_east, dy_north)."""
    R = 6371000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    avg_lat = math.radians((lat1 + lat2) / 2)
    dy = dlat * R                      # kuzey yönü (metre)
    dx = dlon * R * math.cos(avg_lat)  # doğu yönü (metre)
    return dx, dy


def meter_to_gps(lat_ref, lon_ref, dx_east, dy_north):
    """Metre ofsetini GPS koordinatına çevir."""
    R = 6371000.0
    new_lat = lat_ref + math.degrees(dy_north / R)
    new_lon = lon_ref + math.degrees(dx_east / (R * math.cos(math.radians(lat_ref))))
    return new_lat, new_lon


class Test(Node):
    def __init__(self):
        super().__init__('ftest')
        self.poses = {}     # local position
        self.states = {}
        self.gps = {}       # GPS koordinatları (lat, lon, alt)
        self.hedefler = {}  # {drone_id: (x, y, z) local frame}
        self.pubs = {}
        self.yayinla_aktif = False

        for i in range(1,4):
            ns = f'drone{i}'
            self.pubs[i] = self.create_publisher(
                PoseStamped, f'/{ns}/mavros/setpoint_position/local', 10)
            self.create_subscription(
                State, f'/{ns}/mavros/state',
                lambda m, i=i: self.states.update({i: m}), BEST_EFFORT)
            self.create_subscription(
                PoseStamped, f'/{ns}/mavros/local_position/pose',
                lambda m, i=i: self.poses.update({i: m}), BEST_EFFORT)
            self.create_subscription(
                NavSatFix, f'/{ns}/mavros/global_position/global',
                lambda m, i=i: self.gps.update({i: (m.latitude, m.longitude, m.altitude)}),
                BEST_EFFORT)

        self.create_timer(0.05, self._yayinla)  # 20Hz

    def _yayinla(self):
        if not self.yayinla_aktif:
            return
        for i in range(1,4):
            if i not in self.hedefler:
                continue
            x, y, z = self.hedefler[i]
            msg = PoseStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'map'
            msg.pose.position.x = float(x)
            msg.pose.position.y = float(y)
            msg.pose.position.z = float(z)
            msg.pose.orientation.w = 1.0
            self.pubs[i].publish(msg)

    def _spin_sure(self, sn):
        t = time.time()
        while time.time() - t < sn:
            rclpy.spin_once(self, timeout_sec=0.05)

    def _servis(self, srv_type, topic, req, timeout=5.0):
        cli = self.create_client(srv_type, topic)
        if not cli.wait_for_service(timeout_sec=timeout):
            return None
        fut = cli.call_async(req)
        t = time.time()
        while time.time() - t < timeout:
            rclpy.spin_once(self, timeout_sec=0.05)
            if fut.done():
                return fut.result()
        return None

    def formasyon_uygula(self, tip):
        """
        GPS tabanlı formasyon hesaplama.

        1) Tüm dronların GPS'ini oku → ortak merkez (lat, lon) bul
        2) Formasyondaki her drone'un hedef GPS'ini hesapla
        3) Her drone için: hedef GPS - kendi GPS = metre ofset
        4) Bu ofseti drone'un LOCAL frame'inde setpoint olarak gönder
        """
        if len(self.gps) < 3:
            self.get_logger().error('GPS verisi eksik!')
            return

        # 1) Merkez GPS
        avg_lat = sum(g[0] for g in self.gps.values()) / 3
        avg_lon = sum(g[1] for g in self.gps.values()) / 3
        self.get_logger().info(f'  GPS merkez: ({avg_lat:.6f}, {avg_lon:.6f})')

        # 2) Her drone'un hedef GPS'ini hesapla
        offsets = OFFSETS[tip]
        for i in range(1,4):
            fwd, left = offsets[i]
            dx_east  = fwd * SPACING   # ileri = doğu (yaw=0)
            dy_north = left * SPACING  # sol = kuzey

            hedef_lat, hedef_lon = meter_to_gps(avg_lat, avg_lon, dx_east, dy_north)

            # 3) Bu drone'un local frame'inde kaç metre gitcek?
            my_lat, my_lon, my_alt = self.gps[i]
            lokal_dx, lokal_dy = gps_to_meter(my_lat, my_lon, hedef_lat, hedef_lon)

            # 4) Local frame'de mevcut pozisyon + ofset = hedef
            p = self.poses.get(i)
            if p:
                cur_x = p.pose.position.x
                cur_y = p.pose.position.y
            else:
                cur_x, cur_y = 0.0, 0.0

            # Mevcut local pozisyon + GPS farkı = hedef local pozisyon
            self.hedefler[i] = (cur_x + lokal_dx, cur_y + lokal_dy, HOVER_ALT)
            self.get_logger().info(
                f'  drone{i}: hedef=({cur_x+lokal_dx:.1f}, {cur_y+lokal_dy:.1f}) '
                f'[GPS→local ofset: dx={lokal_dx:.1f}m dy={lokal_dy:.1f}m]')

    def calistir(self):
        # 1) Stream rate
        self.get_logger().info('=== STREAM RATE ===')
        for i in range(1,4):
            req = StreamRate.Request()
            req.stream_id = 0
            req.message_rate = 10
            req.on_off = True
            self._servis(StreamRate, f'/drone{i}/mavros/set_stream_rate', req)
        self.get_logger().info('  Tüm stream rate: 10Hz')

        # 2) Pozisyon + GPS oku
        self.get_logger().info('=== POZİSYON + GPS OKUMA (15sn) ===')
        self._spin_sure(15.0)

        for i in range(1,4):
            p = self.poses.get(i)
            g = self.gps.get(i)
            local_str = f'x={p.pose.position.x:.2f} y={p.pose.position.y:.2f} z={p.pose.position.z:.2f}' if p else 'YOK'
            gps_str = f'lat={g[0]:.6f} lon={g[1]:.6f}' if g else 'YOK'
            self.get_logger().info(f'  drone{i}: local=[{local_str}] gps=[{gps_str}]')

        if len(self.gps) < 3:
            self.get_logger().error('GPS alınamadı!')
            return

        # 3) ARM + GUIDED + TAKEOFF
        self.get_logger().info('\n=== ARM + GUIDED + TAKEOFF ===')
        for i in range(1,4):
            req = SetMode.Request()
            req.custom_mode = 'GUIDED'
            self._servis(SetMode, f'/drone{i}/mavros/set_mode', req)
        self.get_logger().info('  GUIDED OK')
        self._spin_sure(0.5)

        for i in range(1,4):
            req = CommandBool.Request()
            req.value = True
            self._servis(CommandBool, f'/drone{i}/mavros/cmd/arming', req)
        self.get_logger().info('  ARM OK')
        self._spin_sure(0.5)

        for i in range(1,4):
            req = CommandTOL.Request()
            req.altitude = HOVER_ALT
            self._servis(CommandTOL, f'/drone{i}/mavros/cmd/takeoff', req)
        self.get_logger().info(f'  TAKEOFF {HOVER_ALT}m OK')

        # 4) Kalkış bekle — setpoint GÖNDERME
        self.get_logger().info('\n=== KALKIŞ BEKLENİYOR (25sn) ===')
        self.get_logger().info('  Setpoint gönderilmiyor — TAKEOFF iptal olmasın!')
        t0 = time.time()
        while time.time() - t0 < 25.0:
            rclpy.spin_once(self, timeout_sec=0.1)
            elapsed = time.time() - t0
            if int(elapsed) % 5 == 0 and int(elapsed * 10) % 50 == 0:
                for i in range(1,4):
                    p = self.poses.get(i)
                    if p:
                        self.get_logger().info(f'  drone{i}: z={p.pose.position.z:.1f}m')

        # 5) Setpoint aktif — hover
        self.get_logger().info('\n=== SETPOINT AKTİF ===')
        for i in range(1,4):
            p = self.poses.get(i)
            if p:
                self.hedefler[i] = (p.pose.position.x, p.pose.position.y, HOVER_ALT)
        self.yayinla_aktif = True
        self._spin_sure(3.0)  # 3sn hover

        # 6) FORMASYONLAR
        for tip in ['OKBASI', 'V', 'CIZGI']:
            self.get_logger().info(f'\n{"="*50}')
            self.get_logger().info(f'=== {tip} FORMASYONU ===')
            self.get_logger().info(f'{"="*50}')

            self.formasyon_uygula(tip)

            self.get_logger().info(f'  Geçiş yapılıyor (20sn)...')
            self._spin_sure(20.0)

            self.get_logger().info(f'  ✓ {tip} — EKRAN GÖRÜNTÜSÜ AL! (15sn bekleniyor)')
            self._spin_sure(15.0)

        self.get_logger().info('\n=== TÜM FORMASYONLAR TAMAMLANDI ===')


def main():
    rclpy.init()
    node = Test()
    try:
        node.calistir()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
