// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from swarm_msgs:msg/TaskTrigger.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "swarm_msgs/msg/detail/task_trigger__rosidl_typesupport_introspection_c.h"
#include "swarm_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "swarm_msgs/msg/detail/task_trigger__functions.h"
#include "swarm_msgs/msg/detail/task_trigger__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `task_type`
// Member `team_id`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  swarm_msgs__msg__TaskTrigger__init(message_memory);
}

void swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_fini_function(void * message_memory)
{
  swarm_msgs__msg__TaskTrigger__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_member_array[4] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__TaskTrigger, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "task_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__TaskTrigger, task_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "start",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__TaskTrigger, start),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "team_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(swarm_msgs__msg__TaskTrigger, team_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_members = {
  "swarm_msgs__msg",  // message namespace
  "TaskTrigger",  // message name
  4,  // number of fields
  sizeof(swarm_msgs__msg__TaskTrigger),
  swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_member_array,  // message members
  swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_init_function,  // function to initialize message memory (memory has to be allocated)
  swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_type_support_handle = {
  0,
  &swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_swarm_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, swarm_msgs, msg, TaskTrigger)() {
  swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_type_support_handle.typesupport_identifier) {
    swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &swarm_msgs__msg__TaskTrigger__rosidl_typesupport_introspection_c__TaskTrigger_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
