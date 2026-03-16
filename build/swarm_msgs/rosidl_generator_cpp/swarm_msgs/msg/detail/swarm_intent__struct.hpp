// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_HPP_
#define SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_HPP_

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
// Member 'target_pos'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'wait_until'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__swarm_msgs__msg__SwarmIntent __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__msg__SwarmIntent __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SwarmIntent_
{
  using Type = SwarmIntent_<ContainerAllocator>;

  explicit SwarmIntent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    target_pos(_init),
    wait_until(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->seq = 0ul;
      this->leader_id = 0;
      this->task_id = "";
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->target_yaw = 0.0f;
      this->drone_altitude = 0.0f;
      this->detach_drone_id = 0;
      this->zone_color = "";
      this->maneuver_active = false;
      this->maneuver_pitch_deg = 0.0f;
      this->maneuver_roll_deg = 0.0f;
      this->active_drone_count = 0;
      this->join_drone_id = 0;
      this->qr_seq = 0ul;
    }
  }

  explicit SwarmIntent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    task_id(_alloc),
    formation_type(_alloc),
    target_pos(_alloc, _init),
    zone_color(_alloc),
    wait_until(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->seq = 0ul;
      this->leader_id = 0;
      this->task_id = "";
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->target_yaw = 0.0f;
      this->drone_altitude = 0.0f;
      this->detach_drone_id = 0;
      this->zone_color = "";
      this->maneuver_active = false;
      this->maneuver_pitch_deg = 0.0f;
      this->maneuver_roll_deg = 0.0f;
      this->active_drone_count = 0;
      this->join_drone_id = 0;
      this->qr_seq = 0ul;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _seq_type =
    uint32_t;
  _seq_type seq;
  using _leader_id_type =
    uint8_t;
  _leader_id_type leader_id;
  using _task_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _task_id_type task_id;
  using _formation_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _formation_type_type formation_type;
  using _drone_spacing_type =
    float;
  _drone_spacing_type drone_spacing;
  using _target_yaw_type =
    float;
  _target_yaw_type target_yaw;
  using _target_pos_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _target_pos_type target_pos;
  using _drone_altitude_type =
    float;
  _drone_altitude_type drone_altitude;
  using _detach_drone_id_type =
    uint8_t;
  _detach_drone_id_type detach_drone_id;
  using _zone_color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _zone_color_type zone_color;
  using _maneuver_active_type =
    bool;
  _maneuver_active_type maneuver_active;
  using _maneuver_pitch_deg_type =
    float;
  _maneuver_pitch_deg_type maneuver_pitch_deg;
  using _maneuver_roll_deg_type =
    float;
  _maneuver_roll_deg_type maneuver_roll_deg;
  using _active_drone_count_type =
    uint8_t;
  _active_drone_count_type active_drone_count;
  using _join_drone_id_type =
    uint8_t;
  _join_drone_id_type join_drone_id;
  using _qr_seq_type =
    uint32_t;
  _qr_seq_type qr_seq;
  using _wait_until_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _wait_until_type wait_until;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__seq(
    const uint32_t & _arg)
  {
    this->seq = _arg;
    return *this;
  }
  Type & set__leader_id(
    const uint8_t & _arg)
  {
    this->leader_id = _arg;
    return *this;
  }
  Type & set__task_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->task_id = _arg;
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
  Type & set__target_pos(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->target_pos = _arg;
    return *this;
  }
  Type & set__drone_altitude(
    const float & _arg)
  {
    this->drone_altitude = _arg;
    return *this;
  }
  Type & set__detach_drone_id(
    const uint8_t & _arg)
  {
    this->detach_drone_id = _arg;
    return *this;
  }
  Type & set__zone_color(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->zone_color = _arg;
    return *this;
  }
  Type & set__maneuver_active(
    const bool & _arg)
  {
    this->maneuver_active = _arg;
    return *this;
  }
  Type & set__maneuver_pitch_deg(
    const float & _arg)
  {
    this->maneuver_pitch_deg = _arg;
    return *this;
  }
  Type & set__maneuver_roll_deg(
    const float & _arg)
  {
    this->maneuver_roll_deg = _arg;
    return *this;
  }
  Type & set__active_drone_count(
    const uint8_t & _arg)
  {
    this->active_drone_count = _arg;
    return *this;
  }
  Type & set__join_drone_id(
    const uint8_t & _arg)
  {
    this->join_drone_id = _arg;
    return *this;
  }
  Type & set__qr_seq(
    const uint32_t & _arg)
  {
    this->qr_seq = _arg;
    return *this;
  }
  Type & set__wait_until(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->wait_until = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::msg::SwarmIntent_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::msg::SwarmIntent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::SwarmIntent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::SwarmIntent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__msg__SwarmIntent
    std::shared_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__msg__SwarmIntent
    std::shared_ptr<swarm_msgs::msg::SwarmIntent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SwarmIntent_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->seq != other.seq) {
      return false;
    }
    if (this->leader_id != other.leader_id) {
      return false;
    }
    if (this->task_id != other.task_id) {
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
    if (this->target_pos != other.target_pos) {
      return false;
    }
    if (this->drone_altitude != other.drone_altitude) {
      return false;
    }
    if (this->detach_drone_id != other.detach_drone_id) {
      return false;
    }
    if (this->zone_color != other.zone_color) {
      return false;
    }
    if (this->maneuver_active != other.maneuver_active) {
      return false;
    }
    if (this->maneuver_pitch_deg != other.maneuver_pitch_deg) {
      return false;
    }
    if (this->maneuver_roll_deg != other.maneuver_roll_deg) {
      return false;
    }
    if (this->active_drone_count != other.active_drone_count) {
      return false;
    }
    if (this->join_drone_id != other.join_drone_id) {
      return false;
    }
    if (this->qr_seq != other.qr_seq) {
      return false;
    }
    if (this->wait_until != other.wait_until) {
      return false;
    }
    return true;
  }
  bool operator!=(const SwarmIntent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SwarmIntent_

// alias to use template instance with default allocator
using SwarmIntent =
  swarm_msgs::msg::SwarmIntent_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__STRUCT_HPP_
