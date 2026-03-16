// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/TeleopCmd.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/teleop_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `mode`
// Member `new_formation_type`
#include "rosidl_runtime_c/string_functions.h"
// Member `execute_at`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
swarm_msgs__msg__TeleopCmd__init(swarm_msgs__msg__TeleopCmd * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    swarm_msgs__msg__TeleopCmd__fini(msg);
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__init(&msg->mode)) {
    swarm_msgs__msg__TeleopCmd__fini(msg);
    return false;
  }
  // vx
  // vy
  // vz
  // yaw_rate
  // execute_at
  if (!builtin_interfaces__msg__Time__init(&msg->execute_at)) {
    swarm_msgs__msg__TeleopCmd__fini(msg);
    return false;
  }
  // new_formation_type
  if (!rosidl_runtime_c__String__init(&msg->new_formation_type)) {
    swarm_msgs__msg__TeleopCmd__fini(msg);
    return false;
  }
  // new_spacing
  return true;
}

void
swarm_msgs__msg__TeleopCmd__fini(swarm_msgs__msg__TeleopCmd * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // mode
  rosidl_runtime_c__String__fini(&msg->mode);
  // vx
  // vy
  // vz
  // yaw_rate
  // execute_at
  builtin_interfaces__msg__Time__fini(&msg->execute_at);
  // new_formation_type
  rosidl_runtime_c__String__fini(&msg->new_formation_type);
  // new_spacing
}

bool
swarm_msgs__msg__TeleopCmd__are_equal(const swarm_msgs__msg__TeleopCmd * lhs, const swarm_msgs__msg__TeleopCmd * rhs)
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
  // mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  // vx
  if (lhs->vx != rhs->vx) {
    return false;
  }
  // vy
  if (lhs->vy != rhs->vy) {
    return false;
  }
  // vz
  if (lhs->vz != rhs->vz) {
    return false;
  }
  // yaw_rate
  if (lhs->yaw_rate != rhs->yaw_rate) {
    return false;
  }
  // execute_at
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->execute_at), &(rhs->execute_at)))
  {
    return false;
  }
  // new_formation_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->new_formation_type), &(rhs->new_formation_type)))
  {
    return false;
  }
  // new_spacing
  if (lhs->new_spacing != rhs->new_spacing) {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__TeleopCmd__copy(
  const swarm_msgs__msg__TeleopCmd * input,
  swarm_msgs__msg__TeleopCmd * output)
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
  // mode
  if (!rosidl_runtime_c__String__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  // vx
  output->vx = input->vx;
  // vy
  output->vy = input->vy;
  // vz
  output->vz = input->vz;
  // yaw_rate
  output->yaw_rate = input->yaw_rate;
  // execute_at
  if (!builtin_interfaces__msg__Time__copy(
      &(input->execute_at), &(output->execute_at)))
  {
    return false;
  }
  // new_formation_type
  if (!rosidl_runtime_c__String__copy(
      &(input->new_formation_type), &(output->new_formation_type)))
  {
    return false;
  }
  // new_spacing
  output->new_spacing = input->new_spacing;
  return true;
}

swarm_msgs__msg__TeleopCmd *
swarm_msgs__msg__TeleopCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__TeleopCmd * msg = (swarm_msgs__msg__TeleopCmd *)allocator.allocate(sizeof(swarm_msgs__msg__TeleopCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__TeleopCmd));
  bool success = swarm_msgs__msg__TeleopCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__TeleopCmd__destroy(swarm_msgs__msg__TeleopCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__TeleopCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__TeleopCmd__Sequence__init(swarm_msgs__msg__TeleopCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__TeleopCmd * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__TeleopCmd *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__TeleopCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__TeleopCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__TeleopCmd__fini(&data[i - 1]);
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
swarm_msgs__msg__TeleopCmd__Sequence__fini(swarm_msgs__msg__TeleopCmd__Sequence * array)
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
      swarm_msgs__msg__TeleopCmd__fini(&array->data[i]);
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

swarm_msgs__msg__TeleopCmd__Sequence *
swarm_msgs__msg__TeleopCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__TeleopCmd__Sequence * array = (swarm_msgs__msg__TeleopCmd__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__TeleopCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__TeleopCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__TeleopCmd__Sequence__destroy(swarm_msgs__msg__TeleopCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__TeleopCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__TeleopCmd__Sequence__are_equal(const swarm_msgs__msg__TeleopCmd__Sequence * lhs, const swarm_msgs__msg__TeleopCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__TeleopCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__TeleopCmd__Sequence__copy(
  const swarm_msgs__msg__TeleopCmd__Sequence * input,
  swarm_msgs__msg__TeleopCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__TeleopCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__TeleopCmd * data =
      (swarm_msgs__msg__TeleopCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__TeleopCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__TeleopCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__TeleopCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
