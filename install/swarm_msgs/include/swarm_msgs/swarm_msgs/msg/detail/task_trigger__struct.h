// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/TaskTrigger.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__STRUCT_H_

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
// Member 'task_type'
// Member 'team_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TaskTrigger in the package swarm_msgs.
/**
  * TaskTrigger.msg
  * Yayıncı : mission_fsm (GCS — Yer Kontrol İstasyonu)
  * Okuyan  : intent_coordinator (TÜM İHA'lar)
  *
  * Görevi başlatan veya durduran TEK GCS komutu.
  * Şartname: TASK1_ACTIVE modunda GCS başka hiçbir kontrol komutu göndermez.
  * Bu mesaj gelince intent_coordinator mode_gating'i devreye alır.
  *
  * YARIŞMA PROSEDÜRÜ:
  *   Hakem "başlat" dediğinde operatör bu komutu gönderir.
  *   Sonrasında GCS müdahalesi imkânsız hale gelir (mode gating).
  *
  * TASK1: Otonom sürü görevi (QR navigasyon + birey çıkarma/ekleme)
  * TASK2: Yarı otonom görev (joystick ile sürü kontrolü)
 */
typedef struct swarm_msgs__msg__TaskTrigger
{
  std_msgs__msg__Header header;
  /// 'TASK1' veya 'TASK2'
  rosidl_runtime_c__String task_type;
  /// True = görevi başlat, False = görevi durdur
  bool start;
  /// Takım ID'si (doğrulama için)
  rosidl_runtime_c__String team_id;
} swarm_msgs__msg__TaskTrigger;

// Struct for a sequence of swarm_msgs__msg__TaskTrigger.
typedef struct swarm_msgs__msg__TaskTrigger__Sequence
{
  swarm_msgs__msg__TaskTrigger * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__TaskTrigger__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__STRUCT_H_
