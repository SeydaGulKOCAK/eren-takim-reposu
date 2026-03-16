// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:msg/JoinRequest.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/msg/detail/join_request__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
swarm_msgs__msg__JoinRequest__init(swarm_msgs__msg__JoinRequest * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    swarm_msgs__msg__JoinRequest__fini(msg);
    return false;
  }
  // drone_id
  // battery_pct
  // ready
  return true;
}

void
swarm_msgs__msg__JoinRequest__fini(swarm_msgs__msg__JoinRequest * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // drone_id
  // battery_pct
  // ready
}

bool
swarm_msgs__msg__JoinRequest__are_equal(const swarm_msgs__msg__JoinRequest * lhs, const swarm_msgs__msg__JoinRequest * rhs)
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
  // drone_id
  if (lhs->drone_id != rhs->drone_id) {
    return false;
  }
  // battery_pct
  if (lhs->battery_pct != rhs->battery_pct) {
    return false;
  }
  // ready
  if (lhs->ready != rhs->ready) {
    return false;
  }
  return true;
}

bool
swarm_msgs__msg__JoinRequest__copy(
  const swarm_msgs__msg__JoinRequest * input,
  swarm_msgs__msg__JoinRequest * output)
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
  // drone_id
  output->drone_id = input->drone_id;
  // battery_pct
  output->battery_pct = input->battery_pct;
  // ready
  output->ready = input->ready;
  return true;
}

swarm_msgs__msg__JoinRequest *
swarm_msgs__msg__JoinRequest__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__JoinRequest * msg = (swarm_msgs__msg__JoinRequest *)allocator.allocate(sizeof(swarm_msgs__msg__JoinRequest), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__msg__JoinRequest));
  bool success = swarm_msgs__msg__JoinRequest__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__msg__JoinRequest__destroy(swarm_msgs__msg__JoinRequest * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__msg__JoinRequest__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__msg__JoinRequest__Sequence__init(swarm_msgs__msg__JoinRequest__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__JoinRequest * data = NULL;

  if (size) {
    data = (swarm_msgs__msg__JoinRequest *)allocator.zero_allocate(size, sizeof(swarm_msgs__msg__JoinRequest), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__msg__JoinRequest__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__msg__JoinRequest__fini(&data[i - 1]);
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
swarm_msgs__msg__JoinRequest__Sequence__fini(swarm_msgs__msg__JoinRequest__Sequence * array)
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
      swarm_msgs__msg__JoinRequest__fini(&array->data[i]);
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

swarm_msgs__msg__JoinRequest__Sequence *
swarm_msgs__msg__JoinRequest__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__msg__JoinRequest__Sequence * array = (swarm_msgs__msg__JoinRequest__Sequence *)allocator.allocate(sizeof(swarm_msgs__msg__JoinRequest__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__msg__JoinRequest__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__msg__JoinRequest__Sequence__destroy(swarm_msgs__msg__JoinRequest__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__msg__JoinRequest__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__msg__JoinRequest__Sequence__are_equal(const swarm_msgs__msg__JoinRequest__Sequence * lhs, const swarm_msgs__msg__JoinRequest__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__msg__JoinRequest__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__msg__JoinRequest__Sequence__copy(
  const swarm_msgs__msg__JoinRequest__Sequence * input,
  swarm_msgs__msg__JoinRequest__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__msg__JoinRequest);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__msg__JoinRequest * data =
      (swarm_msgs__msg__JoinRequest *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__msg__JoinRequest__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__msg__JoinRequest__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__msg__JoinRequest__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
