// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__FUNCTIONS_H_
#define SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "swarm_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "swarm_msgs/msg/detail/swarm_intent__struct.h"

/// Initialize msg/SwarmIntent message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * swarm_msgs__msg__SwarmIntent
 * )) before or use
 * swarm_msgs__msg__SwarmIntent__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SwarmIntent__init(swarm_msgs__msg__SwarmIntent * msg);

/// Finalize msg/SwarmIntent message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SwarmIntent__fini(swarm_msgs__msg__SwarmIntent * msg);

/// Create msg/SwarmIntent message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * swarm_msgs__msg__SwarmIntent__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__SwarmIntent *
swarm_msgs__msg__SwarmIntent__create();

/// Destroy msg/SwarmIntent message.
/**
 * It calls
 * swarm_msgs__msg__SwarmIntent__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SwarmIntent__destroy(swarm_msgs__msg__SwarmIntent * msg);

/// Check for msg/SwarmIntent message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SwarmIntent__are_equal(const swarm_msgs__msg__SwarmIntent * lhs, const swarm_msgs__msg__SwarmIntent * rhs);

/// Copy a msg/SwarmIntent message.
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
swarm_msgs__msg__SwarmIntent__copy(
  const swarm_msgs__msg__SwarmIntent * input,
  swarm_msgs__msg__SwarmIntent * output);

/// Initialize array of msg/SwarmIntent messages.
/**
 * It allocates the memory for the number of elements and calls
 * swarm_msgs__msg__SwarmIntent__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SwarmIntent__Sequence__init(swarm_msgs__msg__SwarmIntent__Sequence * array, size_t size);

/// Finalize array of msg/SwarmIntent messages.
/**
 * It calls
 * swarm_msgs__msg__SwarmIntent__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SwarmIntent__Sequence__fini(swarm_msgs__msg__SwarmIntent__Sequence * array);

/// Create array of msg/SwarmIntent messages.
/**
 * It allocates the memory for the array and calls
 * swarm_msgs__msg__SwarmIntent__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__SwarmIntent__Sequence *
swarm_msgs__msg__SwarmIntent__Sequence__create(size_t size);

/// Destroy array of msg/SwarmIntent messages.
/**
 * It calls
 * swarm_msgs__msg__SwarmIntent__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__SwarmIntent__Sequence__destroy(swarm_msgs__msg__SwarmIntent__Sequence * array);

/// Check for msg/SwarmIntent message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__SwarmIntent__Sequence__are_equal(const swarm_msgs__msg__SwarmIntent__Sequence * lhs, const swarm_msgs__msg__SwarmIntent__Sequence * rhs);

/// Copy an array of msg/SwarmIntent messages.
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
swarm_msgs__msg__SwarmIntent__Sequence__copy(
  const swarm_msgs__msg__SwarmIntent__Sequence * input,
  swarm_msgs__msg__SwarmIntent__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__FUNCTIONS_H_
