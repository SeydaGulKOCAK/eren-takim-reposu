// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_H_

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
// Member 'task_id'
// Member 'formation_type'
// Member 'zone_color'
#include "rosidl_runtime_c/string.h"
// Member 'target_pos'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'wait_until'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/SwarmIntent in the package swarm_msgs.
/**
  * SwarmIntent.msg
  * Yayıncı : intent_coordinator (SADECE LİDER İHA)
  * Okuyan  : local_fsm (TÜM İHA'lar), formation_controller (TÜM)
  *
  * Tüm sürünün ne yapacağını söyleyen ANA KOMUT paketidir.
  * Bu mesajı SADECE lider İHA'daki intent_coordinator yazar.
  * GCS ASLA bu topic'e yazmaz → §5.3 dağıtık mimari kuralı.
  *
  * ÇİFT FİLTRE KURALI (local_fsm'de uygulanır):
  *   1) seq < son_seq → ESKİ LİDERDEN KALAN MESAJ → DROP et
  *   2) seq == son_seq ve header.stamp < son_timestamp → DROP et
 */
typedef struct swarm_msgs__msg__SwarmIntent
{
  /// timestamp (çift filtre için kullanılır)
  std_msgs__msg__Header header;
  /// Monotonic artan sıra no (lider değişiminde seq+1'den devam)
  uint32_t seq;
  /// Bu mesajı kim üretiyor? (lider drone'un ID'si)
  uint8_t leader_id;
  /// ── GÖREV BİLGİSİ ──────────────────────────────────────────────
  /// Aktif görev: 'QR_NAVIGATE' / 'DETACH' / 'REJOIN' /
  /// 'RETURN_HOME' / 'IDLE' / 'MANEUVER'
  rosidl_runtime_c__String task_id;
  /// ── FORMASYON ──────────────────────────────────────────────────
  /// 'OKBASI' / 'V' / 'CIZGI'
  rosidl_runtime_c__String formation_type;
  /// Drone'lar arası mesafe (metre) — QR'dan gelir
  float drone_spacing;
  /// Sürünün ilerleyeceği yön (radyan, ENU'da kuzeyden)
  /// formation_controller offset rotasyonu için kullanır
  float target_yaw;
  /// ── HEDEF POZİSYON ─────────────────────────────────────────────
  /// Sonraki QR / hedef koordinat (ENU, metre)
  geometry_msgs__msg__Point target_pos;
  /// Hedef irtifa (metre) — QR'dan gelir
  float drone_altitude;
  /// ── BİREY ÇIKARMA / EKLEME ──────────────────────────────────────
  /// Ayrılacak drone'un ID'si (0 = kimse ayrılmıyor)
  uint8_t detach_drone_id;
  /// İniş yapılacak zone rengi: 'RED' / 'BLUE' / ''
  rosidl_runtime_c__String zone_color;
  /// ── MANEVRA ────────────────────────────────────────────────────
  /// Pitch/Roll manevrası aktif mi?
  bool maneuver_active;
  /// Pitch açısı (derece) — negatif = öne eğim
  float maneuver_pitch_deg;
  /// Roll açısı (derece) — sağa pozitif
  float maneuver_roll_deg;
  /// ── SÜRÜ DURUMU ────────────────────────────────────────────────
  /// Şu an FLYING olan drone sayısı
  /// formation_controller fallback için kullanır:
  /// < 3 → 2'li LINE formasyonuna geç
  uint8_t active_drone_count;
  /// Sürüye katılacak yedek drone'un ID'si (0 = yok)
  uint8_t join_drone_id;
  /// ── QR BİLGİSİ ─────────────────────────────────────────────────
  /// QR sıra numarası (her QR için artar)
  /// Aynı QR'ı iki kez işlemeyi engeller
  uint32_t qr_seq;
  /// ── BEKLEME ────────────────────────────────────────────────────
  /// Bu zamana kadar mevcut konumda bekle
  /// Manevra / QR okuma sırasında kullanılır
  builtin_interfaces__msg__Time wait_until;
} swarm_msgs__msg__SwarmIntent;

// Struct for a sequence of swarm_msgs__msg__SwarmIntent.
typedef struct swarm_msgs__msg__SwarmIntent__Sequence
{
  swarm_msgs__msg__SwarmIntent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__SwarmIntent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_H_
