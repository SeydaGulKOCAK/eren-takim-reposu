// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:msg/JoinRequest.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_HPP_
#define SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__swarm_msgs__msg__JoinRequest __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__msg__JoinRequest __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct JoinRequest_
{
  using Type = JoinRequest_<ContainerAllocator>;

  explicit JoinRequest_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->drone_id = 0;
      this->battery_pct = 0.0f;
      this->ready = false;
    }
  }

  explicit JoinRequest_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->drone_id = 0;
      this->battery_pct = 0.0f;
      this->ready = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _drone_id_type =
    uint8_t;
  _drone_id_type drone_id;
  using _battery_pct_type =
    float;
  _battery_pct_type battery_pct;
  using _ready_type =
    bool;
  _ready_type ready;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__drone_id(
    const uint8_t & _arg)
  {
    this->drone_id = _arg;
    return *this;
  }
  Type & set__battery_pct(
    const float & _arg)
  {
    this->battery_pct = _arg;
    return *this;
  }
  Type & set__ready(
    const bool & _arg)
  {
    this->ready = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::msg::JoinRequest_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::msg::JoinRequest_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::JoinRequest_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::JoinRequest_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__msg__JoinRequest
    std::shared_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__msg__JoinRequest
    std::shared_ptr<swarm_msgs::msg::JoinRequest_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const JoinRequest_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->drone_id != other.drone_id) {
      return false;
    }
    if (this->battery_pct != other.battery_pct) {
      return false;
    }
    if (this->ready != other.ready) {
      return false;
    }
    return true;
  }
  bool operator!=(const JoinRequest_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct JoinRequest_

// alias to use template instance with default allocator
using JoinRequest =
  swarm_msgs::msg::JoinRequest_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__STRUCT_HPP_
