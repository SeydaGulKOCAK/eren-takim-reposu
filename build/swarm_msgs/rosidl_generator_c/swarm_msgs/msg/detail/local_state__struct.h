// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/LocalState.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__STRUCT_H_

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
// Member 'state'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LocalState in the package swarm_msgs.
/**
  * LocalState.msg
  * Yayıncı : local_fsm
  * Okuyan  : intent_coordinator (TÜM İHA'lar), swarm_comm (GCS izleme)
  *
  * Her drone'un şu an hangi görev adımında olduğunu bildirir.
  * intent_coordinator bu mesajları heartbeat olarak kullanır:
  * 500ms boyunca mesaj gelmezse drone düşmüş sayılır.
  *
  * STATE DEĞERLERİ:
  *   STANDBY      → Yerde bekliyor, henüz görev almadı (yedek drone)
  *   IDLE         → ARM edildi, kalkışa hazır
  *   FLYING       → Havada, sürüyle birlikte görev yapıyor
  *   DETACH       → Sürüden ayrıldı, iniş bölgesine gidiyor
  *   LAND_ZONE    → İniş bölgesi üzerinde, precision_landing aktif
  *   DISARM_WAIT  → İnis yapıldı, DISARM bekleniyor
  *   REARM        → Yeniden ARM ediliyor, sürüye katılacak
  *   REJOIN       → Sürüye katılma manevrası yapıyor
  *   RETURN_HOME  → Tüm görevler bitti, eve dönüyor
  *   LANDING      → Eve geldi, iniş yapıyor
  *   SAFETY_HOLD  → Güvenlik olayı: batarya kritik / geofence ihlali
  *   PILOT_OVERRIDE → RC kill-switch / GUIDED dışı mod tespit edildi
 */
typedef struct swarm_msgs__msg__LocalState
{
  /// timestamp + frame_id
  std_msgs__msg__Header header;
  /// Hangi drone? (1, 2, 3...)
  uint8_t drone_id;
  /// Yukarıdaki state değerlerinden biri
  rosidl_runtime_c__String state;
  /// Monotonic artan sıra numarası
  /// intent_coordinator çift filtre için kullanır:
  /// seq < son_seq → eski mesaj, DROP et
  uint32_t seq;
} swarm_msgs__msg__LocalState;

// Struct for a sequence of swarm_msgs__msg__LocalState.
typedef struct swarm_msgs__msg__LocalState__Sequence
{
  swarm_msgs__msg__LocalState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__LocalState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__STRUCT_H_
