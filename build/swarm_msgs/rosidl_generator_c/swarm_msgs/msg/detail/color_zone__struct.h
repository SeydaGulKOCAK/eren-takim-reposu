// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/ColorZone.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'color'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ColorZone in the package swarm_msgs.
/**
  * ColorZone.msg
  * Yayıncı : qr_perception
  * Okuyan  : intent_coordinator (DETACH görevinde iniş bölgesi seçimi için)
  *
  * Rota boyunca tespit edilen tek bir renk bölgesi.
  * Sürü bu bölgeleri hafızaya alır; birey çıkarma komutunda kullanır.
  *
  * Şartname §5.1.2:
  *   "...birey ayrılacak iniş alanının rengini ve konumunu kaydeder"
 */
typedef struct swarm_msgs__msg__ColorZone
{
  /// ENU koordinat — z genellikle 0 (zemin)
  geometry_msgs__msg__Point position;
  /// 'RED' veya 'BLUE'
  rosidl_runtime_c__String color;
  /// Hassas iniş bölgesi yarıçapı
  float radius;
} swarm_msgs__msg__ColorZone;

// Struct for a sequence of swarm_msgs__msg__ColorZone.
typedef struct swarm_msgs__msg__ColorZone__Sequence
{
  swarm_msgs__msg__ColorZone * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__ColorZone__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__STRUCT_H_
