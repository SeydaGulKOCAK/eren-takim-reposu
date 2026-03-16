// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:msg/FormationCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_HPP_
#define SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_HPP_

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
# define DEPRECATED__swarm_msgs__msg__FormationCmd __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__msg__FormationCmd __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FormationCmd_
{
  using Type = FormationCmd_<ContainerAllocator>;

  explicit FormationCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->target_yaw = 0.0f;
      this->active_drone_count = 0;
    }
  }

  explicit FormationCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    formation_type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->target_yaw = 0.0f;
      this->active_drone_count = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _formation_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _formation_type_type formation_type;
  using _drone_spacing_type =
    float;
  _drone_spacing_type drone_spacing;
  using _target_yaw_type =
    float;
  _target_yaw_type target_yaw;
  using _active_drone_count_type =
    uint8_t;
  _active_drone_count_type active_drone_count;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__formation_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->formation_type = _arg;
    return *this;
  }
  Type & set__drone_spacing(
    const float & _arg)
  {
    this->drone_spacing = _arg;
    return *this;
  }
  Type & set__target_yaw(
    const float & _arg)
  {
    this->target_yaw = _arg;
    return *this;
  }
  Type & set__active_drone_count(
    const uint8_t & _arg)
  {
    this->active_drone_count = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::msg::FormationCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::msg::FormationCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::FormationCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::FormationCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__msg__FormationCmd
    std::shared_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__msg__FormationCmd
    std::shared_ptr<swarm_msgs::msg::FormationCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FormationCmd_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->formation_type != other.formation_type) {
      return false;
    }
    if (this->drone_spacing != other.drone_spacing) {
      return false;
    }
    if (this->target_yaw != other.target_yaw) {
      return false;
    }
    if (this->active_drone_count != other.active_drone_count) {
      return false;
    }
    return true;
  }
  bool operator!=(const FormationCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FormationCmd_

// alias to use template instance with default allocator
using FormationCmd =
  swarm_msgs::msg::FormationCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__STRUCT_HPP_
