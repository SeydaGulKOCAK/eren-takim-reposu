// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/JoinRequest.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_H_

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

/// Struct defined in msg/JoinRequest in the package swarm_msgs.
/**
  * JoinRequest.msg
  * Yayıncı : local_fsm (STANDBY state'indeki yedek drone)
  * Okuyan  : intent_coordinator (TÜM İHA'lar)
  *
  * STANDBY'daki yedek drone periyodik olarak bu mesajı gönderir:
  * "Ben hazırım, ne zaman sürüye katılayım?"
  * intent_coordinator bir drone DISARM_WAIT'e geçince yedek drone'u
  * çağırır ve SwarmIntent.join_drone_id'yi doldurur.
 */
typedef struct swarm_msgs__msg__JoinRequest
{
  std_msgs__msg__Header header;
  /// Hangi yedek drone talep ediyor?
  uint8_t drone_id;
  /// Batarya yüzdesi (%) — intent_coordinator
  /// en dolu bataryalı yedek drone'u seçebilir
  float battery_pct;
  /// Gerçekten hazır mı? (ARM edilebilir durumdaysa True)
  bool ready;
} swarm_msgs__msg__JoinRequest;

// Struct for a sequence of swarm_msgs__msg__JoinRequest.
typedef struct swarm_msgs__msg__JoinRequest__Sequence
{
  swarm_msgs__msg__JoinRequest * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__JoinRequest__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_H_
