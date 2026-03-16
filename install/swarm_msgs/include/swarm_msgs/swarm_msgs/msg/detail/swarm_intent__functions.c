// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/swarm_intent__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `task_id`
// Member `formation_type`
// Member `zone_color`
#include "rosidl_runtime_c/string_functions.h"
// Member `target_pos`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `wait_until`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
swarm_msgs__msg__SwarmIntent__init(swarm_msgs__msg__SwarmIntent * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  // seq
  // leader_id
  // task_id
  if (!rosidl_runtime_c__String__init(&msg->task_id)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  // formation_type
  if (!rosidl_runtime_c__String__init(&msg->formation_type)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  // drone_spacing
  // target_yaw
  // target_pos
  if (!geometry_msgs__msg__Point__init(&msg->target_pos)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  // drone_altitude
  // detach_drone_id
  // zone_color
  if (!rosidl_runtime_c__String__init(&msg->zone_color)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  // maneuver_active
  // maneuver_pitch_deg
  // maneuver_roll_deg
  // active_drone_count
  // join_drone_id
  // qr_seq
  // wait_until
  if (!builtin_interfaces__msg__Time__init(&msg->wait_until)) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
    return false;
  }
  return true;
}

void
swarm_msgs__msg__SwarmIntent__fini(swarm_msgs__msg__SwarmIntent * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // seq
  // leader_id
  // task_id
  rosidl_runtime_c__String__fini(&msg->task_id);
  // formation_type
  rosidl_runtime_c__String__fini(&msg->formation_type);
  // drone_spacing
  // target_yaw
  // target_pos
  geometry_msgs__msg__Point__fini(&msg->target_pos);
  // drone_altitude
  // detach_drone_id
  // zone_color
  rosidl_runtime_c__String__fini(&msg->zone_color);
  // maneuver_active
  // maneuver_pitch_deg
  // maneuver_roll_deg
  // active_drone_count
  // join_drone_id
  // qr_seq
  // wait_until
  builtin_interfaces__msg__Time__fini(&msg->wait_until);
}

bool
swarm_msgs__msg__SwarmIntent__are_equal(const swarm_msgs__msg__SwarmIntent * lhs, const swarm_msgs__msg__SwarmIntent * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // seq
  if (lhs->seq != rhs->seq) {
    return false;
  }
  // leader_id
  if (lhs->leader_id != rhs->leader_id) {
    return false;
  }
  // task_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->task_id), &(rhs->task_id)))
  {
    return false;
  }
  // formation_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->formation_type), &(rhs->formation_type)))
  {
    return false;
  }
  // drone_spacing
  if (lhs->drone_spacing != rhs->drone_spacing) {
    return false;
  }
  // target_yaw
  if (lhs->target_yaw != rhs->target_yaw) {
    return false;
  }
  // target_pos
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->target_pos), &(rhs->target_pos)))
  {
    return false;
  }
  // drone_altitude
  if (lhs->drone_altitude != rhs->drone_altitude) {
    return false;
  }
  // detach_drone_id
  if (lhs->detach_drone_id != rhs->detach_drone_id) {
    return false;
  }
  // zone_color
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->zone_color), &(rhs->zone_color)))
  {
    return false;
  }
  // maneuver_active
  if (lhs->maneuver_active != rhs->maneuver_active) {
    return false;
  }
  // maneuver_pitch_deg
  if (lhs->maneuver_pitch_deg != rhs->maneuver_pitch_deg) {
    return false;
  }
  // maneuver_roll_deg
  if (lhs->maneuver_roll_deg != rhs->maneuver_roll_deg) {
    return false;
  }
  // active_drone_count
  if (lhs->active_drone_count != rhs->active_drone_count) {
    return false;
  }
  // join_drone_id
  if (lhs->join_drone_id != rhs->join_drone_id) {
    return false;
  }
  // qr_seq
  if (lhs->qr_seq != rhs->qr_seq) {
    return false;
  }
  // wait_until
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->wait_until), &(rhs->wait_until)))
  {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__SwarmIntent__copy(
  const swarm_msgs__msg__SwarmIntent * input,
  swarm_msgs__msg__SwarmIntent * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // seq
  output->seq = input->seq;
  // leader_id
  output->leader_id = input->leader_id;
  // task_id
  if (!rosidl_runtime_c__String__copy(
      &(input->task_id), &(output->task_id)))
  {
    return false;
  }
  // formation_type
  if (!rosidl_runtime_c__String__copy(
      &(input->formation_type), &(output->formation_type)))
  {
    return false;
  }
  // drone_spacing
  output->drone_spacing = input->drone_spacing;
  // target_yaw
  output->target_yaw = input->target_yaw;
  // target_pos
  if (!geometry_msgs__msg__Point__copy(
      &(input->target_pos), &(output->target_pos)))
  {
    return false;
  }
  // drone_altitude
  output->drone_altitude = input->drone_altitude;
  // detach_drone_id
  output->detach_drone_id = input->detach_drone_id;
  // zone_color
  if (!rosidl_runtime_c__String__copy(
      &(input->zone_color), &(output->zone_color)))
  {
    return false;
  }
  // maneuver_active
  output->maneuver_active = input->maneuver_active;
  // maneuver_pitch_deg
  output->maneuver_pitch_deg = input->maneuver_pitch_deg;
  // maneuver_roll_deg
  output->maneuver_roll_deg = input->maneuver_roll_deg;
  // active_drone_count
  output->active_drone_count = input->active_drone_count;
  // join_drone_id
  output->join_drone_id = input->join_drone_id;
  // qr_seq
  output->qr_seq = input->qr_seq;
  // wait_until
  if (!builtin_interfaces__msg__Time__copy(
      &(input->wait_until), &(output->wait_until)))
  {
    return false;
  }
  return true;
}

swarm_msgs__msg__SwarmIntent *
swarm_msgs__msg__SwarmIntent__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__SwarmIntent * msg = (swarm_msgs__msg__SwarmIntent *)allocator.allocate(sizeof(swarm_msgs__msg__SwarmIntent), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__SwarmIntent));
  bool success = swarm_msgs__msg__SwarmIntent__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__SwarmIntent__destroy(swarm_msgs__msg__SwarmIntent * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__SwarmIntent__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__SwarmIntent__Sequence__init(swarm_msgs__msg__SwarmIntent__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__SwarmIntent * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__SwarmIntent *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__SwarmIntent), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__SwarmIntent__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__SwarmIntent__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
swarm_msgs__msg__SwarmIntent__Sequence__fini(swarm_msgs__msg__SwarmIntent__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      swarm_msgs__msg__SwarmIntent__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

swarm_msgs__msg__SwarmIntent__Sequence *
swarm_msgs__msg__SwarmIntent__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__SwarmIntent__Sequence * array = (swarm_msgs__msg__SwarmIntent__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__SwarmIntent__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__SwarmIntent__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__SwarmIntent__Sequence__destroy(swarm_msgs__msg__SwarmIntent__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__SwarmIntent__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__SwarmIntent__Sequence__are_equal(const swarm_msgs__msg__SwarmIntent__Sequence * lhs, const swarm_msgs__msg__SwarmIntent__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__SwarmIntent__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__SwarmIntent__Sequence__copy(
  const swarm_msgs__msg__SwarmIntent__Sequence * input,
  swarm_msgs__msg__SwarmIntent__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__SwarmIntent);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__SwarmIntent * data =
      (swarm_msgs__msg__SwarmIntent *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__SwarmIntent__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__SwarmIntent__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__SwarmIntent__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
