// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_HPP_
#define SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_HPP_

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
// Member 'qr_position'
// Member 'next_qr_position'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__swarm_msgs__msg__QRResult __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__msg__QRResult __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct QRResult_
{
  using Type = QRResult_<ContainerAllocator>;

  explicit QRResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    qr_position(_init),
    next_qr_position(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->team_id = "";
      this->qr_id = 0ul;
      this->formation_active = false;
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->altitude_active = false;
      this->altitude = 0.0f;
      this->maneuver_active = false;
      this->pitch_deg = 0.0f;
      this->roll_deg = 0.0f;
      this->detach_active = false;
      this->detach_drone_id = 0;
      this->zone_color = "";
      this->next_qr_id = 0ul;
      this->wait_seconds = 0.0f;
    }
  }

  explicit QRResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    team_id(_alloc),
    formation_type(_alloc),
    zone_color(_alloc),
    qr_position(_alloc, _init),
    next_qr_position(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->team_id = "";
      this->qr_id = 0ul;
      this->formation_active = false;
      this->formation_type = "";
      this->drone_spacing = 0.0f;
      this->altitude_active = false;
      this->altitude = 0.0f;
      this->maneuver_active = false;
      this->pitch_deg = 0.0f;
      this->roll_deg = 0.0f;
      this->detach_active = false;
      this->detach_drone_id = 0;
      this->zone_color = "";
      this->next_qr_id = 0ul;
      this->wait_seconds = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _team_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _team_id_type team_id;
  using _qr_id_type =
    uint32_t;
  _qr_id_type qr_id;
  using _formation_active_type =
    bool;
  _formation_active_type formation_active;
  using _formation_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _formation_type_type formation_type;
  using _drone_spacing_type =
    float;
  _drone_spacing_type drone_spacing;
  using _altitude_active_type =
    bool;
  _altitude_active_type altitude_active;
  using _altitude_type =
    float;
  _altitude_type altitude;
  using _maneuver_active_type =
    bool;
  _maneuver_active_type maneuver_active;
  using _pitch_deg_type =
    float;
  _pitch_deg_type pitch_deg;
  using _roll_deg_type =
    float;
  _roll_deg_type roll_deg;
  using _detach_active_type =
    bool;
  _detach_active_type detach_active;
  using _detach_drone_id_type =
    uint8_t;
  _detach_drone_id_type detach_drone_id;
  using _zone_color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _zone_color_type zone_color;
  using _next_qr_id_type =
    uint32_t;
  _next_qr_id_type next_qr_id;
  using _qr_position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _qr_position_type qr_position;
  using _next_qr_position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _next_qr_position_type next_qr_position;
  using _wait_seconds_type =
    float;
  _wait_seconds_type wait_seconds;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__team_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->team_id = _arg;
    return *this;
  }
  Type & set__qr_id(
    const uint32_t & _arg)
  {
    this->qr_id = _arg;
    return *this;
  }
  Type & set__formation_active(
    const bool & _arg)
  {
    this->formation_active = _arg;
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
  Type & set__altitude_active(
    const bool & _arg)
  {
    this->altitude_active = _arg;
    return *this;
  }
  Type & set__altitude(
    const float & _arg)
  {
    this->altitude = _arg;
    return *this;
  }
  Type & set__maneuver_active(
    const bool & _arg)
  {
    this->maneuver_active = _arg;
    return *this;
  }
  Type & set__pitch_deg(
    const float & _arg)
  {
    this->pitch_deg = _arg;
    return *this;
  }
  Type & set__roll_deg(
    const float & _arg)
  {
    this->roll_deg = _arg;
    return *this;
  }
  Type & set__detach_active(
    const bool & _arg)
  {
    this->detach_active = _arg;
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
  Type & set__next_qr_id(
    const uint32_t & _arg)
  {
    this->next_qr_id = _arg;
    return *this;
  }
  Type & set__qr_position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->qr_position = _arg;
    return *this;
  }
  Type & set__next_qr_position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->next_qr_position = _arg;
    return *this;
  }
  Type & set__wait_seconds(
    const float & _arg)
  {
    this->wait_seconds = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::msg::QRResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::msg::QRResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::QRResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::msg::QRResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__msg__QRResult
    std::shared_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__msg__QRResult
    std::shared_ptr<swarm_msgs::msg::QRResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QRResult_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->team_id != other.team_id) {
      return false;
    }
    if (this->qr_id != other.qr_id) {
      return false;
    }
    if (this->formation_active != other.formation_active) {
      return false;
    }
    if (this->formation_type != other.formation_type) {
      return false;
    }
    if (this->drone_spacing != other.drone_spacing) {
      return false;
    }
    if (this->altitude_active != other.altitude_active) {
      return false;
    }
    if (this->altitude != other.altitude) {
      return false;
    }
    if (this->maneuver_active != other.maneuver_active) {
      return false;
    }
    if (this->pitch_deg != other.pitch_deg) {
      return false;
    }
    if (this->roll_deg != other.roll_deg) {
      return false;
    }
    if (this->detach_active != other.detach_active) {
      return false;
    }
    if (this->detach_drone_id != other.detach_drone_id) {
      return false;
    }
    if (this->zone_color != other.zone_color) {
      return false;
    }
    if (this->next_qr_id != other.next_qr_id) {
      return false;
    }
    if (this->qr_position != other.qr_position) {
      return false;
    }
    if (this->next_qr_position != other.next_qr_position) {
      return false;
    }
    if (this->wait_seconds != other.wait_seconds) {
      return false;
    }
    return true;
  }
  bool operator!=(const QRResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QRResult_

// alias to use template instance with default allocator
using QRResult =
  swarm_msgs::msg::QRResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__QR_RESULT__STRUCT_HPP_
