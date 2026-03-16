// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from swarm_msgs:msg/ColorZone.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__FUNCTIONS_H_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "swarm_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "swarm_msgs/msg/detail/color_zone__struct.h"

/// Initialize msg/ColorZone message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * swarm_msgs__msg__ColorZone
 * )) before or use
 * swarm_msgs__msg__ColorZone__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__ColorZone__init(swarm_msgs__msg__ColorZone * msg);

/// Finalize msg/ColorZone message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__ColorZone__fini(swarm_msgs__msg__ColorZone * msg);

/// Create msg/ColorZone message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * swarm_msgs__msg__ColorZone__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__ColorZone *
swarm_msgs__msg__ColorZone__create();

/// Destroy msg/ColorZone message.
/**
 * It calls
 * swarm_msgs__msg__ColorZone__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__ColorZone__destroy(swarm_msgs__msg__ColorZone * msg);

/// Check for msg/ColorZone message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__ColorZone__are_equal(const swarm_msgs__msg__ColorZone * lhs, const swarm_msgs__msg__ColorZone * rhs);

/// Copy a msg/ColorZone message.
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
swarm_msgs__msg__ColorZone__copy(
  const swarm_msgs__msg__ColorZone * input,
  swarm_msgs__msg__ColorZone * output);

/// Initialize array of msg/ColorZone messages.
/**
 * It allocates the memory for the number of elements and calls
 * swarm_msgs__msg__ColorZone__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__ColorZone__Sequence__init(swarm_msgs__msg__ColorZone__Sequence * array, size_t size);

/// Finalize array of msg/ColorZone messages.
/**
 * It calls
 * swarm_msgs__msg__ColorZone__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__ColorZone__Sequence__fini(swarm_msgs__msg__ColorZone__Sequence * array);

/// Create array of msg/ColorZone messages.
/**
 * It allocates the memory for the array and calls
 * swarm_msgs__msg__ColorZone__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__ColorZone__Sequence *
swarm_msgs__msg__ColorZone__Sequence__create(size_t size);

/// Destroy array of msg/ColorZone messages.
/**
 * It calls
 * swarm_msgs__msg__ColorZone__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__ColorZone__Sequence__destroy(swarm_msgs__msg__ColorZone__Sequence * array);

/// Check for msg/ColorZone message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__ColorZone__Sequence__are_equal(const swarm_msgs__msg__ColorZone__Sequence * lhs, const swarm_msgs__msg__ColorZone__Sequence * rhs);

/// Copy an array of msg/ColorZone messages.
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
swarm_msgs__msg__ColorZone__Sequence__copy(
  const swarm_msgs__msg__ColorZone__Sequence * input,
  swarm_msgs__msg__ColorZone__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__FUNCTIONS_H_
