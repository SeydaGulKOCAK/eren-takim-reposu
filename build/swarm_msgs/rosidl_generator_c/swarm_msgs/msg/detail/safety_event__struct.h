// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/SafetyEvent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__STRUCT_H_

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
// Member 'event_type'
// Member 'description'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SafetyEvent in the package swarm_msgs.
/**
  * SafetyEvent.msg
  * Yayıncı : safety_monitor (Her RPi4)
  * Okuyan  : local_fsm (kendi RPi4), mission_fsm (GCS)
  *
  * Kritik güvenlik durumu oluştuğunda yayınlanır.
  * local_fsm bu mesajı alınca GCS'ye SORMADAN SAFETY_HOLD'a geçer.
  * §5.5.4: Her İHA bağımsız failsafe kararı alabilmelidir.
  *
  * EVENT_TYPE DEĞERLERİ:
  *   BATTERY_CRITICAL  → Batarya eşik altına düştü (örn: %15)
  *   GEOFENCE_BREACH   → Drone izin verilen uçuş alanının dışına çıktı
  *   OSCILLATION       → Osilasyon tespit edildi (PID yeter siz → tehlikeli)
  *   GNSS_DEGRADED     → GPS sinyal kalitesi kritik seviyenin altına düştü
  *   ALTITUDE_EXCEEDED → Yazılımsal tavan aşıldı
 */
typedef struct swarm_msgs__msg__SafetyEvent
{
  std_msgs__msg__Header header;
  /// Hangi drone'da olay oluştu?
  uint8_t drone_id;
  /// Yukarıdaki event type değerlerinden biri
  rosidl_runtime_c__String event_type;
  /// İnsan okunabilir açıklama (log için)
  rosidl_runtime_c__String description;
  /// 0.0-1.0 arası şiddet (1.0 = maksimum tehlike)
  float severity;
} swarm_msgs__msg__SafetyEvent;

// Struct for a sequence of swarm_msgs__msg__SafetyEvent.
typedef struct swarm_msgs__msg__SafetyEvent__Sequence
{
  swarm_msgs__msg__SafetyEvent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__SafetyEvent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__STRUCT_H_
