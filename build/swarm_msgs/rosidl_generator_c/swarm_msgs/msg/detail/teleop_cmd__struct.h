// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:msg/TeleopCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_H_
#define SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_H_

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
// Member 'mode'
// Member 'new_formation_type'
#include "rosidl_runtime_c/string.h"
// Member 'execute_at'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/TeleopCmd in the package swarm_msgs.
/**
  * TeleopCmd.msg
  * Yayıncı : swarm_teleop (GCS) — SADECE TASK2_ACTIVE modunda
  * Okuyan  : formation_controller (TÜM RPi4'ler)
  *
  * Görev 2 (Yarı Otonom Sürü Kontrolü) için joystick/RC kumanda komutunu taşır.
  * Ham hız vektörü içerir — world-frame setpoint DEĞİL.
  *
  * ÖNEMLİ NOTLAR:
  *   execute_at: Wi-Fi gecikmesi kompansasyonu için.
  *     Her drone bu timestamp'te komutu uygular → formasyon bütünlüğü korunur.
  *   TASK1_ACTIVE'de swarm_teleop bu topic'e YAZMAZ (mode gating ile kapalı).
  *
  * MOD AÇIKLAMASI:
  *   MOVE     : Joystick tüm sürüyü hareket ettirir.
  *              Formasyon bozulmaz, sürünün merkezi kayar.
  *              vx/vy/vz/yaw_rate ile kontrol edilir.
  *   MANEUVER : Formasyon şekli değişir.
  *              Sürünün merkezi sabit kalır.
  *              new_formation_type ve/veya new_spacing ile şekil değiştirilir.
 */
typedef struct swarm_msgs__msg__TeleopCmd
{
  std_msgs__msg__Header header;
  /// ── MOD ────────────────────────────────────────────────────────
  /// 'MOVE' veya 'MANEUVER'
  rosidl_runtime_c__String mode;
  /// ── HAREKET KOMUTU (MOVE modunda kullanılır) ───────────────────
  /// Koordinat: formation-local çerçeve (ileri/sol/yukarı)
  /// Birim: m/s (normalize edilmiş joystick girdisi × max_speed)
  /// ileri (+) / geri (-)     hızı
  float vx;
  /// sol   (+) / sağ  (-)     hızı
  float vy;
  /// yukarı(+) / aşağı(-)     hızı
  float vz;
  /// CCW(+)  / CW(-)  dönüş hızı
  /// → formasyon merkezi etrafında tüm sürüyü döndürür
  float yaw_rate;
  /// ── ZAMANLAMA (Wi-Fi gecikmesi kompansasyonu) ──────────────────
  /// Bu timestamp'te komut uygulanır.
  /// 0 → hemen uygula (gecikme yok)
  builtin_interfaces__msg__Time execute_at;
  /// ── FORMASYON DEĞİŞİKLİĞİ (MANEUVER modunda kullanılır) ───────
  /// 'OKBASI' / 'V' / 'CIZGI' — boş ise değişmez
  rosidl_runtime_c__String new_formation_type;
  /// 0.0 ise spacing değişmez
  float new_spacing;
} swarm_msgs__msg__TeleopCmd;

// Struct for a sequence of swarm_msgs__msg__TeleopCmd.
typedef struct swarm_msgs__msg__TeleopCmd__Sequence
{
  swarm_msgs__msg__TeleopCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__msg__TeleopCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_H_
