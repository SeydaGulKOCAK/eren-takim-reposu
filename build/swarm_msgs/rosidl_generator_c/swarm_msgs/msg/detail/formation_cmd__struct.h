// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/FormationCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_H_

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
// Member 'formation_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/FormationCmd in the package swarm_msgs.
/**
  * FormationCmd.msg
  * Yayıncı : intent_coordinator (LİDER İHA)
  * Okuyan  : formation_controller (TÜM İHA'lar)
  *
  * Aktif formasyon bilgisini taşır.
  * SwarmIntent içinde de aynı bilgi var, ama formation_controller
  * için ayrı ve sade bir topic daha temiz bir arayüz sağlar.
  *
  * GÖREV 2'DE: swarm_teleop da bu topic'e yazar (TASK1_ACTIVE'de kapalı).
 */
typedef struct swarm_msgs__msg__FormationCmd
{
  std_msgs__msg__Header header;
  /// 'OKBASI' / 'V' / 'CIZGI'
  rosidl_runtime_c__String formation_type;
  /// Drone'lar arası mesafe (metre)
  float drone_spacing;
  /// Formasyonun baktığı yön (radyan, ENU)
  /// formation_controller offset vektörlerini bu açıyla döndürür
  float target_yaw;
  /// Şu an havada kaç drone var?
  /// < 3 ise formation_controller 2'li LINE'a geçer (fallback)
  uint8_t active_drone_count;
} swarm_msgs__msg__FormationCmd;

// Struct for a sequence of swarm_msgs__msg__FormationCmd.
typedef struct swarm_msgs__msg__FormationCmd__Sequence
{
  swarm_msgs__msg__FormationCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__FormationCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_H_
