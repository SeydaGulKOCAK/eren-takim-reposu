// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from swarm_msgs:msg/JoinRequest.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__FUNCTIONS_H_
#define SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "swarm_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "swarm_msgs/msg/detail/join_request__struct.h"

/// Initialize msg/JoinRequest message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * swarm_msgs__msg__JoinRequest
 * )) before or use
 * swarm_msgs__msg__JoinRequest__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__JoinRequest__init(swarm_msgs__msg__JoinRequest * msg);

/// Finalize msg/JoinRequest message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__JoinRequest__fini(swarm_msgs__msg__JoinRequest * msg);

/// Create msg/JoinRequest message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * swarm_msgs__msg__JoinRequest__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__JoinRequest *
swarm_msgs__msg__JoinRequest__create();

/// Destroy msg/JoinRequest message.
/**
 * It calls
 * swarm_msgs__msg__JoinRequest__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__JoinRequest__destroy(swarm_msgs__msg__JoinRequest * msg);

/// Check for msg/JoinRequest message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__JoinRequest__are_equal(const swarm_msgs__msg__JoinRequest * lhs, const swarm_msgs__msg__JoinRequest * rhs);

/// Copy a msg/JoinRequest message.
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
swarm_msgs__msg__JoinRequest__copy(
  const swarm_msgs__msg__JoinRequest * input,
  swarm_msgs__msg__JoinRequest * output);

/// Initialize array of msg/JoinRequest messages.
/**
 * It allocates the memory for the number of elements and calls
 * swarm_msgs__msg__JoinRequest__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__JoinRequest__Sequence__init(swarm_msgs__msg__JoinRequest__Sequence * array, size_t size);

/// Finalize array of msg/JoinRequest messages.
/**
 * It calls
 * swarm_msgs__msg__JoinRequest__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__JoinRequest__Sequence__fini(swarm_msgs__msg__JoinRequest__Sequence * array);

/// Create array of msg/JoinRequest messages.
/**
 * It allocates the memory for the array and calls
 * swarm_msgs__msg__JoinRequest__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
swarm_msgs__msg__JoinRequest__Sequence *
swarm_msgs__msg__JoinRequest__Sequence__create(size_t size);

/// Destroy array of msg/JoinRequest messages.
/**
 * It calls
 * swarm_msgs__msg__JoinRequest__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
void
swarm_msgs__msg__JoinRequest__Sequence__destroy(swarm_msgs__msg__JoinRequest__Sequence * array);

/// Check for msg/JoinRequest message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_swarm_msgs
bool
swarm_msgs__msg__JoinRequest__Sequence__are_equal(const swarm_msgs__msg__JoinRequest__Sequence * lhs, const swarm_msgs__msg__JoinRequest__Sequence * rhs);

/// Copy an array of msg/JoinRequest messages.
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
swarm_msgs__msg__JoinRequest__Sequence__copy(
  const swarm_msgs__msg__JoinRequest__Sequence * input,
  swarm_msgs__msg__JoinRequest__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__FUNCTIONS_H_
