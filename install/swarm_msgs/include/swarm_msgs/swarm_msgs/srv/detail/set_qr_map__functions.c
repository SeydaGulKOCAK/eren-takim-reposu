// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from swarm_msgs:srv/SetQRMap.idl
// generated code does not contain a copyright notice
#include "swarm_msgs/srv/detail/set_qr_map__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `qr_positions`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `qr_ids`
// Member `next_qr_ids`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
swarm_msgs__srv__SetQRMap_Request__init(swarm_msgs__srv__SetQRMap_Request * msg)
{
  if (!msg) {
    return false;
  }
  // qr_positions
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->qr_positions, 0)) {
    swarm_msgs__srv__SetQRMap_Request__fini(msg);
    return false;
  }
  // qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__init(&msg->qr_ids, 0)) {
    swarm_msgs__srv__SetQRMap_Request__fini(msg);
    return false;
  }
  // next_qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__init(&msg->next_qr_ids, 0)) {
    swarm_msgs__srv__SetQRMap_Request__fini(msg);
    return false;
  }
  return true;
}

void
swarm_msgs__srv__SetQRMap_Request__fini(swarm_msgs__srv__SetQRMap_Request * msg)
{
  if (!msg) {
    return;
  }
  // qr_positions
  geometry_msgs__msg__Point__Sequence__fini(&msg->qr_positions);
  // qr_ids
  rosidl_runtime_c__uint32__Sequence__fini(&msg->qr_ids);
  // next_qr_ids
  rosidl_runtime_c__uint32__Sequence__fini(&msg->next_qr_ids);
}

bool
swarm_msgs__srv__SetQRMap_Request__are_equal(const swarm_msgs__srv__SetQRMap_Request * lhs, const swarm_msgs__srv__SetQRMap_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // qr_positions
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->qr_positions), &(rhs->qr_positions)))
  {
    return false;
  }
  // qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__are_equal(
      &(lhs->qr_ids), &(rhs->qr_ids)))
  {
    return false;
  }
  // next_qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__are_equal(
      &(lhs->next_qr_ids), &(rhs->next_qr_ids)))
  {
    return false;
  }
  return true;
}

bool
swarm_msgs__srv__SetQRMap_Request__copy(
  const swarm_msgs__srv__SetQRMap_Request * input,
  swarm_msgs__srv__SetQRMap_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // qr_positions
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->qr_positions), &(output->qr_positions)))
  {
    return false;
  }
  // qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__copy(
      &(input->qr_ids), &(output->qr_ids)))
  {
    return false;
  }
  // next_qr_ids
  if (!rosidl_runtime_c__uint32__Sequence__copy(
      &(input->next_qr_ids), &(output->next_qr_ids)))
  {
    return false;
  }
  return true;
}

swarm_msgs__srv__SetQRMap_Request *
swarm_msgs__srv__SetQRMap_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Request * msg = (swarm_msgs__srv__SetQRMap_Request *)allocator.allocate(sizeof(swarm_msgs__srv__SetQRMap_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__srv__SetQRMap_Request));
  bool success = swarm_msgs__srv__SetQRMap_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__srv__SetQRMap_Request__destroy(swarm_msgs__srv__SetQRMap_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__srv__SetQRMap_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__srv__SetQRMap_Request__Sequence__init(swarm_msgs__srv__SetQRMap_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Request * data = NULL;

  if (size) {
    data = (swarm_msgs__srv__SetQRMap_Request *)allocator.zero_allocate(size, sizeof(swarm_msgs__srv__SetQRMap_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__srv__SetQRMap_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__srv__SetQRMap_Request__fini(&data[i - 1]);
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
swarm_msgs__srv__SetQRMap_Request__Sequence__fini(swarm_msgs__srv__SetQRMap_Request__Sequence * array)
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
      swarm_msgs__srv__SetQRMap_Request__fini(&array->data[i]);
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

swarm_msgs__srv__SetQRMap_Request__Sequence *
swarm_msgs__srv__SetQRMap_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Request__Sequence * array = (swarm_msgs__srv__SetQRMap_Request__Sequence *)allocator.allocate(sizeof(swarm_msgs__srv__SetQRMap_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__srv__SetQRMap_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__srv__SetQRMap_Request__Sequence__destroy(swarm_msgs__srv__SetQRMap_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__srv__SetQRMap_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__srv__SetQRMap_Request__Sequence__are_equal(const swarm_msgs__srv__SetQRMap_Request__Sequence * lhs, const swarm_msgs__srv__SetQRMap_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__srv__SetQRMap_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__srv__SetQRMap_Request__Sequence__copy(
  const swarm_msgs__srv__SetQRMap_Request__Sequence * input,
  swarm_msgs__srv__SetQRMap_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__srv__SetQRMap_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__srv__SetQRMap_Request * data =
      (swarm_msgs__srv__SetQRMap_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__srv__SetQRMap_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__srv__SetQRMap_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__srv__SetQRMap_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
swarm_msgs__srv__SetQRMap_Response__init(swarm_msgs__srv__SetQRMap_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    swarm_msgs__srv__SetQRMap_Response__fini(msg);
    return false;
  }
  return true;
}

void
swarm_msgs__srv__SetQRMap_Response__fini(swarm_msgs__srv__SetQRMap_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
swarm_msgs__srv__SetQRMap_Response__are_equal(const swarm_msgs__srv__SetQRMap_Response * lhs, const swarm_msgs__srv__SetQRMap_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
swarm_msgs__srv__SetQRMap_Response__copy(
  const swarm_msgs__srv__SetQRMap_Response * input,
  swarm_msgs__srv__SetQRMap_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

swarm_msgs__srv__SetQRMap_Response *
swarm_msgs__srv__SetQRMap_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Response * msg = (swarm_msgs__srv__SetQRMap_Response *)allocator.allocate(sizeof(swarm_msgs__srv__SetQRMap_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(swarm_msgs__srv__SetQRMap_Response));
  bool success = swarm_msgs__srv__SetQRMap_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
swarm_msgs__srv__SetQRMap_Response__destroy(swarm_msgs__srv__SetQRMap_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    swarm_msgs__srv__SetQRMap_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
swarm_msgs__srv__SetQRMap_Response__Sequence__init(swarm_msgs__srv__SetQRMap_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Response * data = NULL;

  if (size) {
    data = (swarm_msgs__srv__SetQRMap_Response *)allocator.zero_allocate(size, sizeof(swarm_msgs__srv__SetQRMap_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = swarm_msgs__srv__SetQRMap_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        swarm_msgs__srv__SetQRMap_Response__fini(&data[i - 1]);
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
swarm_msgs__srv__SetQRMap_Response__Sequence__fini(swarm_msgs__srv__SetQRMap_Response__Sequence * array)
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
      swarm_msgs__srv__SetQRMap_Response__fini(&array->data[i]);
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

swarm_msgs__srv__SetQRMap_Response__Sequence *
swarm_msgs__srv__SetQRMap_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  swarm_msgs__srv__SetQRMap_Response__Sequence * array = (swarm_msgs__srv__SetQRMap_Response__Sequence *)allocator.allocate(sizeof(swarm_msgs__srv__SetQRMap_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = swarm_msgs__srv__SetQRMap_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
swarm_msgs__srv__SetQRMap_Response__Sequence__destroy(swarm_msgs__srv__SetQRMap_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    swarm_msgs__srv__SetQRMap_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
swarm_msgs__srv__SetQRMap_Response__Sequence__are_equal(const swarm_msgs__srv__SetQRMap_Response__Sequence * lhs, const swarm_msgs__srv__SetQRMap_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!swarm_msgs__srv__SetQRMap_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
swarm_msgs__srv__SetQRMap_Response__Sequence__copy(
  const swarm_msgs__srv__SetQRMap_Response__Sequence * input,
  swarm_msgs__srv__SetQRMap_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(swarm_msgs__srv__SetQRMap_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    swarm_msgs__srv__SetQRMap_Response * data =
      (swarm_msgs__srv__SetQRMap_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!swarm_msgs__srv__SetQRMap_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          swarm_msgs__srv__SetQRMap_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!swarm_msgs__srv__SetQRMap_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
