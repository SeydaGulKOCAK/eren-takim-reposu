// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/qr_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `team_id`
// Member `formation_type`
// Member `zone_color`
#include "rosidl_runtime_c/string_functions.h"
// Member `qr_position`
// Member `next_qr_position`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
swarm_msgs__msg__QRResult__init(swarm_msgs__msg__QRResult * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // team_id
  if (!rosidl_runtime_c__String__init(&msg->team_id)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // qr_id
  // formation_active
  // formation_type
  if (!rosidl_runtime_c__String__init(&msg->formation_type)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // drone_spacing
  // altitude_active
  // altitude
  // maneuver_active
  // pitch_deg
  // roll_deg
  // detach_active
  // detach_drone_id
  // zone_color
  if (!rosidl_runtime_c__String__init(&msg->zone_color)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // next_qr_id
  // qr_position
  if (!geometry_msgs__msg__Point__init(&msg->qr_position)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // next_qr_position
  if (!geometry_msgs__msg__Point__init(&msg->next_qr_position)) {
    swarm_msgs__msg__QRResult__fini(msg);
    return false;
  }
  // wait_seconds
  return true;
}

void
swarm_msgs__msg__QRResult__fini(swarm_msgs__msg__QRResult * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // team_id
  rosidl_runtime_c__String__fini(&msg->team_id);
  // qr_id
  // formation_active
  // formation_type
  rosidl_runtime_c__String__fini(&msg->formation_type);
  // drone_spacing
  // altitude_active
  // altitude
  // maneuver_active
  // pitch_deg
  // roll_deg
  // detach_active
  // detach_drone_id
  // zone_color
  rosidl_runtime_c__String__fini(&msg->zone_color);
  // next_qr_id
  // qr_position
  geometry_msgs__msg__Point__fini(&msg->qr_position);
  // next_qr_position
  geometry_msgs__msg__Point__fini(&msg->next_qr_position);
  // wait_seconds
}

bool
swarm_msgs__msg__QRResult__are_equal(const swarm_msgs__msg__QRResult * lhs, const swarm_msgs__msg__QRResult * rhs)
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
  // team_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->team_id), &(rhs->team_id)))
  {
    return false;
  }
  // qr_id
  if (lhs->qr_id != rhs->qr_id) {
    return false;
  }
  // formation_active
  if (lhs->formation_active != rhs->formation_active) {
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
  // altitude_active
  if (lhs->altitude_active != rhs->altitude_active) {
    return false;
  }
  // altitude
  if (lhs->altitude != rhs->altitude) {
    return false;
  }
  // maneuver_active
  if (lhs->maneuver_active != rhs->maneuver_active) {
    return false;
  }
  // pitch_deg
  if (lhs->pitch_deg != rhs->pitch_deg) {
    return false;
  }
  // roll_deg
  if (lhs->roll_deg != rhs->roll_deg) {
    return false;
  }
  // detach_active
  if (lhs->detach_active != rhs->detach_active) {
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
  // next_qr_id
  if (lhs->next_qr_id != rhs->next_qr_id) {
    return false;
  }
  // qr_position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->qr_position), &(rhs->qr_position)))
  {
    return false;
  }
  // next_qr_position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->next_qr_position), &(rhs->next_qr_position)))
  {
    return false;
  }
  // wait_seconds
  if (lhs->wait_seconds != rhs->wait_seconds) {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__QRResult__copy(
  const swarm_msgs__msg__QRResult * input,
  swarm_msgs__msg__QRResult * output)
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
  // team_id
  if (!rosidl_runtime_c__String__copy(
      &(input->team_id), &(output->team_id)))
  {
    return false;
  }
  // qr_id
  output->qr_id = input->qr_id;
  // formation_active
  output->formation_active = input->formation_active;
  // formation_type
  if (!rosidl_runtime_c__String__copy(
      &(input->formation_type), &(output->formation_type)))
  {
    return false;
  }
  // drone_spacing
  output->drone_spacing = input->drone_spacing;
  // altitude_active
  output->altitude_active = input->altitude_active;
  // altitude
  output->altitude = input->altitude;
  // maneuver_active
  output->maneuver_active = input->maneuver_active;
  // pitch_deg
  output->pitch_deg = input->pitch_deg;
  // roll_deg
  output->roll_deg = input->roll_deg;
  // detach_active
  output->detach_active = input->detach_active;
  // detach_drone_id
  output->detach_drone_id = input->detach_drone_id;
  // zone_color
  if (!rosidl_runtime_c__String__copy(
      &(input->zone_color), &(output->zone_color)))
  {
    return false;
  }
  // next_qr_id
  output->next_qr_id = input->next_qr_id;
  // qr_position
  if (!geometry_msgs__msg__Point__copy(
      &(input->qr_position), &(output->qr_position)))
  {
    return false;
  }
  // next_qr_position
  if (!geometry_msgs__msg__Point__copy(
      &(input->next_qr_position), &(output->next_qr_position)))
  {
    return false;
  }
  // wait_seconds
  output->wait_seconds = input->wait_seconds;
  return true;
}

swarm_msgs__msg__QRResult *
swarm_msgs__msg__QRResult__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__QRResult * msg = (swarm_msgs__msg__QRResult *)allocator.allocate(sizeof(swarm_msgs__msg__QRResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__QRResult));
  bool success = swarm_msgs__msg__QRResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__QRResult__destroy(swarm_msgs__msg__QRResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__QRResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__QRResult__Sequence__init(swarm_msgs__msg__QRResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__QRResult * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__QRResult *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__QRResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__QRResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__QRResult__fini(&data[i - 1]);
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
swarm_msgs__msg__QRResult__Sequence__fini(swarm_msgs__msg__QRResult__Sequence * array)
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
      swarm_msgs__msg__QRResult__fini(&array->data[i]);
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

swarm_msgs__msg__QRResult__Sequence *
swarm_msgs__msg__QRResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__QRResult__Sequence * array = (swarm_msgs__msg__QRResult__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__QRResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__QRResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__QRResult__Sequence__destroy(swarm_msgs__msg__QRResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__QRResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__QRResult__Sequence__are_equal(const swarm_msgs__msg__QRResult__Sequence * lhs, const swarm_msgs__msg__QRResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__QRResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__QRResult__Sequence__copy(
  const swarm_msgs__msg__QRResult__Sequence * input,
  swarm_msgs__msg__QRResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__QRResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__QRResult * data =
      (swarm_msgs__msg__QRResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__QRResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__QRResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__QRResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
