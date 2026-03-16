// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:msg/TeleopCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_HPP_
#define SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_HPP_

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
// Member 'execute_at'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__swarm_msgs__msg__TeleopCmd __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__msg__TeleopCmd __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TeleopCmd_
{
  using Type = TeleopCmd_<ContainerAllocator>;

  explicit TeleopCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    execute_at(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = "";
      this->vx = 0.0f;
      this->vy = 0.0f;
      this->vz = 0.0f;
      this->yaw_rate = 0.0f;
      this->new_formation_type = "";
      this->new_spacing = 0.0f;
    }
  }

  explicit TeleopCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    mode(_alloc),
    execute_at(_alloc, _init),
    new_formation_type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = "";
      this->vx = 0.0f;
      this->vy = 0.0f;
      this->vz = 0.0f;
      this->yaw_rate = 0.0f;
      this->new_formation_type = "";
      this->new_spacing = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mode_type mode;
  using _vx_type =
    float;
  _vx_type vx;
  using _vy_type =
    float;
  _vy_type vy;
  using _vz_type =
    float;
  _vz_type vz;
  using _yaw_rate_type =
    float;
  _yaw_rate_type yaw_rate;
  using _execute_at_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _execute_at_type execute_at;
  using _new_formation_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _new_formation_type_type new_formation_type;
  using _new_spacing_type =
    float;
  _new_spacing_type new_spacing;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mode = _arg;
    return *this;
  }
  Type & set__vx(
    const float & _arg)
  {
    this->vx = _arg;
    return *this;
  }
  Type & set__vy(
    const float & _arg)
  {
    this->vy = _arg;
    return *this;
  }
  Type & set__vz(
    const float & _arg)
  {
    this->vz = _arg;
    return *this;
  }
  Type & set__yaw_rate(
    const float & _arg)
  {
    this->yaw_rate = _arg;
    return *this;
  }
  Type & set__execute_at(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->execute_at = _arg;
    return *this;
  }
  Type & set__new_formation_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->new_formation_type = _arg;
    return *this;
  }
  Type & set__new_spacing(
    const float & _arg)
  {
    this->new_spacing = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::msg::TeleopCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::msg::TeleopCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::TeleopCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::TeleopCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__msg__TeleopCmd
    std::shared_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__msg__TeleopCmd
    std::shared_ptr<swarm_msgs::msg::TeleopCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TeleopCmd_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->mode != other.mode) {
      return false;
    }
    if (this->vx != other.vx) {
      return false;
    }
    if (this->vy != other.vy) {
      return false;
    }
    if (this->vz != other.vz) {
      return false;
    }
    if (this->yaw_rate != other.yaw_rate) {
      return false;
    }
    if (this->execute_at != other.execute_at) {
      return false;
    }
    if (this->new_formation_type != other.new_formation_type) {
      return false;
    }
    if (this->new_spacing != other.new_spacing) {
      return false;
    }
    return true;
  }
  bool operator!=(const TeleopCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TeleopCmd_

// alias to use template instance with default allocator
using TeleopCmd =
  swarm_msgs::msg::TeleopCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__STRUCT_HPP_
