// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from swarm_msgs:srv/SetQRMap.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_H_
#define SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'qr_positions'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'qr_ids'
// Member 'next_qr_ids'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/SetQRMap in the package swarm_msgs.
typedef struct swarm_msgs__srv__SetQRMap_Request
{
  geometry_msgs__msg__Point__Sequence qr_positions;
  rosidl_runtime_c__uint32__Sequence qr_ids;
  rosidl_runtime_c__uint32__Sequence next_qr_ids;
} swarm_msgs__srv__SetQRMap_Request;

// Struct for a sequence of swarm_msgs__srv__SetQRMap_Request.
typedef struct swarm_msgs__srv__SetQRMap_Request__Sequence
{
  swarm_msgs__srv__SetQRMap_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__srv__SetQRMap_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetQRMap in the package swarm_msgs.
typedef struct swarm_msgs__srv__SetQRMap_Response
{
  bool success;
  rosidl_runtime_c__String message;
} swarm_msgs__srv__SetQRMap_Response;

// Struct for a sequence of swarm_msgs__srv__SetQRMap_Response.
typedef struct swarm_msgs__srv__SetQRMap_Response__Sequence
{
  swarm_msgs__srv__SetQRMap_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} swarm_msgs__srv__SetQRMap_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_H_
