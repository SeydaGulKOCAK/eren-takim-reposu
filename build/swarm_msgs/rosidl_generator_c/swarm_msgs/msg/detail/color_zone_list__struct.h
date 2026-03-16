// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/ColorZoneList.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__STRUCT_H_

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
// Member 'zones'
#include "swarm_msgs/msg/detail/color_zone__struct.h"

/// Struct defined in msg/ColorZoneList in the package swarm_msgs.
/**
  * ColorZoneList.msg
  * Yayıncı : qr_perception   → /perception/color_zones  (1 Hz)
  * Okuyan  : intent_coordinator (DETACH görevinde hedef zone seçimi için)
  *
  * Simülasyonda tüm renk bölgeleri YAML'dan yüklenip sürekli yayınlanır.
  * Gerçek sistemde kamera ile tespit edilir.
 */
typedef struct swarm_msgs__msg__ColorZoneList
{
  std_msgs__msg__Header header;
  /// Tespit edilen tüm renk bölgeleri
  swarm_msgs__msg__ColorZone__Sequence zones;
} swarm_msgs__msg__ColorZoneList;

// Struct for a sequence of swarm_msgs__msg__ColorZoneList.
typedef struct swarm_msgs__msg__ColorZoneList__Sequence
{
  swarm_msgs__msg__ColorZoneList * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__ColorZoneList__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__STRUCT_H_
