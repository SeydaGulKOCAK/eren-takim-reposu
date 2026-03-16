// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from swarm_msgs:msg/SafetyEvent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__FUNCTIONS_H_
#define SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "swarm_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "swarm_msgs/msg/detail/safety_event__struct.h"

/// Initialize msg/SafetyEvent message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * swarm_msgs__msg__SafetyEvent
 * )) before or use
 * swarm_msgs__msg__SafetyEvent__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__init(swarm_msgs__msg__SafetyEvent * msg);

/// Finalize msg/SafetyEvent message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SafetyEvent__fini(swarm_msgs__msg__SafetyEvent * msg);

/// Create msg/SafetyEvent message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * swarm_msgs__msg__SafetyEvent__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__SafetyEvent *
swarm_msgs__msg__SafetyEvent__create();

/// Destroy msg/SafetyEvent message.
/**
 * It calls
 * swarm_msgs__msg__SafetyEvent__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SafetyEvent__destroy(swarm_msgs__msg__SafetyEvent * msg);

/// Check for msg/SafetyEvent message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__are_equal(const swarm_msgs__msg__SafetyEvent * lhs, const swarm_msgs__msg__SafetyEvent * rhs);

/// Copy a msg/SafetyEvent message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__copy(
  const swarm_msgs__msg__SafetyEvent * input,
  swarm_msgs__msg__SafetyEvent * output);

/// Initialize array of msg/SafetyEvent messages.
/**
 * It allocates the memory for the number of elements and calls
 * swarm_msgs__msg__SafetyEvent__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__Sequence__init(swarm_msgs__msg__SafetyEvent__Sequence * array, size_t size);

/// Finalize array of msg/SafetyEvent messages.
/**
 * It calls
 * swarm_msgs__msg__SafetyEvent__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SafetyEvent__Sequence__fini(swarm_msgs__msg__SafetyEvent__Sequence * array);

/// Create array of msg/SafetyEvent messages.
/**
 * It allocates the memory for the array and calls
 * swarm_msgs__msg__SafetyEvent__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__SafetyEvent__Sequence *
swarm_msgs__msg__SafetyEvent__Sequence__create(size_t size);

/// Destroy array of msg/SafetyEvent messages.
/**
 * It calls
 * swarm_msgs__msg__SafetyEvent__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SafetyEvent__Sequence__destroy(swarm_msgs__msg__SafetyEvent__Sequence * array);

/// Check for msg/SafetyEvent message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__Sequence__are_equal(const swarm_msgs__msg__SafetyEvent__Sequence * lhs, const swarm_msgs__msg__SafetyEvent__Sequence * rhs);

/// Copy an array of msg/SafetyEvent messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SafetyEvent__Sequence__copy(
  const swarm_msgs__msg__SafetyEvent__Sequence * input,
  swarm_msgs__msg__SafetyEvent__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__FUNCTIONS_H_
