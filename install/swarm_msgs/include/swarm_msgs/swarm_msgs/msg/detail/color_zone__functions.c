// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/ColorZone.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/color_zone__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `color`
#include "rosidl_runtime_c/string_functions.h"

bool
swarm_msgs__msg__ColorZone__init(swarm_msgs__msg__ColorZone * msg)
{
  if (!msg) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    swarm_msgs__msg__ColorZone__fini(msg);
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__init(&msg->color)) {
    swarm_msgs__msg__ColorZone__fini(msg);
    return false;
  }
  // radius
  return true;
}

void
swarm_msgs__msg__ColorZone__fini(swarm_msgs__msg__ColorZone * msg)
{
  if (!msg) {
    return;
  }
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // color
  rosidl_runtime_c__String__fini(&msg->color);
  // radius
}

bool
swarm_msgs__msg__ColorZone__are_equal(const swarm_msgs__msg__ColorZone * lhs, const swarm_msgs__msg__ColorZone * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->color), &(rhs->color)))
  {
    return false;
  }
  // radius
  if (lhs->radius != rhs->radius) {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__ColorZone__copy(
  const swarm_msgs__msg__ColorZone * input,
  swarm_msgs__msg__ColorZone * output)
{
  if (!input || !output) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__copy(
      &(input->color), &(output->color)))
  {
    return false;
  }
  // radius
  output->radius = input->radius;
  return true;
}

swarm_msgs__msg__ColorZone *
swarm_msgs__msg__ColorZone__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__ColorZone * msg = (swarm_msgs__msg__ColorZone *)allocator.allocate(sizeof(swarm_msgs__msg__ColorZone), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__ColorZone));
  bool success = swarm_msgs__msg__ColorZone__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__ColorZone__destroy(swarm_msgs__msg__ColorZone * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__ColorZone__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__ColorZone__Sequence__init(swarm_msgs__msg__ColorZone__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__ColorZone * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__ColorZone *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__ColorZone), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__ColorZone__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__ColorZone__fini(&data[i - 1]);
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
swarm_msgs__msg__ColorZone__Sequence__fini(swarm_msgs__msg__ColorZone__Sequence * array)
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
      swarm_msgs__msg__ColorZone__fini(&array->data[i]);
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

swarm_msgs__msg__ColorZone__Sequence *
swarm_msgs__msg__ColorZone__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__ColorZone__Sequence * array = (swarm_msgs__msg__ColorZone__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__ColorZone__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__ColorZone__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__ColorZone__Sequence__destroy(swarm_msgs__msg__ColorZone__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__ColorZone__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__ColorZone__Sequence__are_equal(const swarm_msgs__msg__ColorZone__Sequence * lhs, const swarm_msgs__msg__ColorZone__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__ColorZone__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__ColorZone__Sequence__copy(
  const swarm_msgs__msg__ColorZone__Sequence * input,
  swarm_msgs__msg__ColorZone__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__ColorZone);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__ColorZone * data =
      (swarm_msgs__msg__ColorZone *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__ColorZone__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__ColorZone__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__ColorZone__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
