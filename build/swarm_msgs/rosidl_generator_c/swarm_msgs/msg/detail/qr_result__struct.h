// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'team_id'
// Member 'formation_type'
// Member 'zone_color'
#include "rosidl_runtime_c/string.h"
// Member 'qr_position'
// Member 'next_qr_position'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/QRResult in the package swarm_msgs.
/**
  * QRResult.msg
  * Yayıncı : qr_perception (Kamera olan İHA)
  * Okuyan  : intent_coordinator (TÜM İHA'lar)
  *
  * QR kodu okunduğunda parse edilmiş içeriği taşır.
  * intent_coordinator sadece kendi takım ID'sine ait mesajları işler.
  *
  * FAILOVER:
  *   Kamera drone'u SAFETY_HOLD veya PILOT_OVERRIDE'a geçince
  *   yedek drone'un qr_perception'ı devreye girer — aynı topic'i kullanır.
  *
  * QR FORMATI (Şartname):
  *   team_id | formasyon | irtifa | manevra | birey_çıkar | sonraki_qr_no
 */
typedef struct swarm_msgs__msg__QRResult
{
  std_msgs__msg__Header header;
  /// Takım ID'si — kendi ID'mizle eşleşmeli, yoksa DROP
  rosidl_runtime_c__String team_id;
  /// Bu QR'ın numarası (1, 2, 3...)
  /// intent_coordinator: qr_id <= son_işlenen → DROP
  uint32_t qr_id;
  /// ── FORMASYON KOMUTU ──────────────────────────────────────────────────────
  /// Bu QR'da formasyon değişiyor mu?
  bool formation_active;
  /// 'OKBASI' / 'V' / 'CIZGI'
  rosidl_runtime_c__String formation_type;
  /// Drone'lar arası mesafe (metre)
  float drone_spacing;
  /// ── İRTİFA KOMUTU ─────────────────────────────────────────────────────────
  /// Bu QR'da irtifa değişiyor mu?
  bool altitude_active;
  /// Yeni hedef irtifa (metre)
  float altitude;
  /// ── MANEVRA KOMUTU ────────────────────────────────────────────────────────
  /// Pitch/Roll manevrası: formasyon yatay düzlemde eğilir
  /// formation_controller 3D rotasyon matrisiyle hesaplar
  bool maneuver_active;
  /// Eğim açısı (derece) — negatif = öne eğim
  float pitch_deg;
  /// Yatış açısı (derece) — pozitif = sağa
  float roll_deg;
  /// ── BİREY ÇIKARMA KOMUTU ─────────────────────────────────────────────────
  /// Bu QR'da birey ayrılıyor mu?
  bool detach_active;
  /// Ayrılacak drone'un ID'si
  uint8_t detach_drone_id;
  /// Hangi renkli alana inecek: 'RED' / 'BLUE'
  rosidl_runtime_c__String zone_color;
  /// ── SONRAKI QR ────────────────────────────────────────────────────────────
  /// Sonraki QR'ın numarası
  /// 0 = Bu SON QR → görev tamamlandı → RETURN_HOME
  uint32_t next_qr_id;
  /// Bu QR'ın ENU koordinatı (okunduğu nokta)
  geometry_msgs__msg__Point qr_position;
  /// Bir sonraki QR'ın ENU koordinatı
  /// intent_coordinator bunu target_pos olarak kullanır
  /// next_qr_id = 0 ise sıfır-nokta (RETURN_HOME)
  geometry_msgs__msg__Point next_qr_position;
  /// QR görevini icra ettikten sonra bekle
  float wait_seconds;
} swarm_msgs__msg__QRResult;

// Struct for a sequence of swarm_msgs__msg__QRResult.
typedef struct swarm_msgs__msg__QRResult__Sequence
{
  swarm_msgs__msg__QRResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__QRResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_H_
