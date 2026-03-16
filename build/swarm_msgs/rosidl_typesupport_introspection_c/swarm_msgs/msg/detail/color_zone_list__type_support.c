// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from swarm_msgs:msg/ColorZoneList.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "swarm_msgs/msg/detail/color_zone_list__rosidl_typesupport_introspection_c.h"
#include "swarm_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "swarm_msgs/msg/detail/color_zone_list__functions.h"
#include "swarm_msgs/msg/detail/color_zone_list__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `zones`
#include "swarm_msgs/msg/color_zone.h"
// Member `zones`
#include "swarm_msgs/msg/detail/color_zone__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  swarm_msgs__msg__ColorZoneList__init(message_memory);
}

void swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_fini_function(void * message_memory)
{
  swarm_msgs__msg__ColorZoneList__fini(message_memory);
}

size_t swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__size_function__ColorZoneList__zones(
  const void * untyped_member)
{
  const swarm_msgs__msg__ColorZone__Sequence * member =
    (const swarm_msgs__msg__ColorZone__Sequence *)(untyped_member);
  return member->size;
}

const void * swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_const_function__ColorZoneList__zones(
  const void * untyped_member, size_t index)
{
  const swarm_msgs__msg__ColorZone__Sequence * member =
    (const swarm_msgs__msg__ColorZone__Sequence *)(untyped_member);
  return &member->data[index];
}

void * swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_function__ColorZoneList__zones(
  void * untyped_member, size_t index)
{
  swarm_msgs__msg__ColorZone__Sequence * member =
    (swarm_msgs__msg__ColorZone__Sequence *)(untyped_member);
  return &member->data[index];
}

void swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__fetch_function__ColorZoneList__zones(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const swarm_msgs__msg__ColorZone * item =
    ((const swarm_msgs__msg__ColorZone *)
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_const_function__ColorZoneList__zones(untyped_member, index));
  swarm_msgs__msg__ColorZone * value =
    (swarm_msgs__msg__ColorZone *)(untyped_value);
  *value = *item;
}

void swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__assign_function__ColorZoneList__zones(
  void * untyped_member, size_t index, const void * untyped_value)
{
  swarm_msgs__msg__ColorZone * item =
    ((swarm_msgs__msg__ColorZone *)
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_function__ColorZoneList__zones(untyped_member, index));
  const swarm_msgs__msg__ColorZone * value =
    (const swarm_msgs__msg__ColorZone *)(untyped_value);
  *item = *value;
}

bool swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__resize_function__ColorZoneList__zones(
  void * untyped_member, size_t size)
{
  swarm_msgs__msg__ColorZone__Sequence * member =
    (swarm_msgs__msg__ColorZone__Sequence *)(untyped_member);
  swarm_msgs__msg__ColorZone__Sequence__fini(member);
  return swarm_msgs__msg__ColorZone__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__ColorZoneList, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "zones",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__ColorZoneList, zones),  // bytes offset in struct
    NULL,  // default value
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__size_function__ColorZoneList__zones,  // size() function pointer
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_const_function__ColorZoneList__zones,  // get_const(index) function pointer
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__get_function__ColorZoneList__zones,  // get(index) function pointer
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__fetch_function__ColorZoneList__zones,  // fetch(index, &value) function pointer
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__assign_function__ColorZoneList__zones,  // assign(index, value) function pointer
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__resize_function__ColorZoneList__zones  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_members = {
  "swarm_msgs__msg",  // message namespace
  "ColorZoneList",  // message name
  2,  // number of fields
  sizeof(swarm_msgs__msg__ColorZoneList),
  swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_member_array,  // message members
  swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_init_function,  // function to initialize message memory (memory has to be allocated)
  swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_type_support_handle = {
  0,
  &swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_swarm_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, swarm_msgs, msg, ColorZoneList)() {
  swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, swarm_msgs, msg, ColorZone)();
  if (!swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_type_support_handle.typesupport_identifier) {
    swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &swarm_msgs__msg__ColorZoneList__rosidl_typesupport_introspection_c__ColorZoneList_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
