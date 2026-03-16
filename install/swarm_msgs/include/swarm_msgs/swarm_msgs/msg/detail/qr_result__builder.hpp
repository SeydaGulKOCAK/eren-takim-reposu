// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__QR_RESULT__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__QR_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/qr_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_QRResult_wait_seconds
{
public:
  explicit Init_QRResult_wait_seconds(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::QRResult wait_seconds(::swarm_msgs::msg::QRResult::_wait_seconds_type arg)
  {
    msg_.wait_seconds = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_next_qr_position
{
public:
  explicit Init_QRResult_next_qr_position(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_wait_seconds next_qr_position(::swarm_msgs::msg::QRResult::_next_qr_position_type arg)
  {
    msg_.next_qr_position = std::move(arg);
    return Init_QRResult_wait_seconds(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_qr_position
{
public:
  explicit Init_QRResult_qr_position(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_next_qr_position qr_position(::swarm_msgs::msg::QRResult::_qr_position_type arg)
  {
    msg_.qr_position = std::move(arg);
    return Init_QRResult_next_qr_position(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_next_qr_id
{
public:
  explicit Init_QRResult_next_qr_id(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_qr_position next_qr_id(::swarm_msgs::msg::QRResult::_next_qr_id_type arg)
  {
    msg_.next_qr_id = std::move(arg);
    return Init_QRResult_qr_position(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_zone_color
{
public:
  explicit Init_QRResult_zone_color(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_next_qr_id zone_color(::swarm_msgs::msg::QRResult::_zone_color_type arg)
  {
    msg_.zone_color = std::move(arg);
    return Init_QRResult_next_qr_id(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_detach_drone_id
{
public:
  explicit Init_QRResult_detach_drone_id(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_zone_color detach_drone_id(::swarm_msgs::msg::QRResult::_detach_drone_id_type arg)
  {
    msg_.detach_drone_id = std::move(arg);
    return Init_QRResult_zone_color(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_detach_active
{
public:
  explicit Init_QRResult_detach_active(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_detach_drone_id detach_active(::swarm_msgs::msg::QRResult::_detach_active_type arg)
  {
    msg_.detach_active = std::move(arg);
    return Init_QRResult_detach_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_roll_deg
{
public:
  explicit Init_QRResult_roll_deg(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_detach_active roll_deg(::swarm_msgs::msg::QRResult::_roll_deg_type arg)
  {
    msg_.roll_deg = std::move(arg);
    return Init_QRResult_detach_active(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_pitch_deg
{
public:
  explicit Init_QRResult_pitch_deg(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_roll_deg pitch_deg(::swarm_msgs::msg::QRResult::_pitch_deg_type arg)
  {
    msg_.pitch_deg = std::move(arg);
    return Init_QRResult_roll_deg(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_maneuver_active
{
public:
  explicit Init_QRResult_maneuver_active(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_pitch_deg maneuver_active(::swarm_msgs::msg::QRResult::_maneuver_active_type arg)
  {
    msg_.maneuver_active = std::move(arg);
    return Init_QRResult_pitch_deg(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_altitude
{
public:
  explicit Init_QRResult_altitude(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_maneuver_active altitude(::swarm_msgs::msg::QRResult::_altitude_type arg)
  {
    msg_.altitude = std::move(arg);
    return Init_QRResult_maneuver_active(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_altitude_active
{
public:
  explicit Init_QRResult_altitude_active(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_altitude altitude_active(::swarm_msgs::msg::QRResult::_altitude_active_type arg)
  {
    msg_.altitude_active = std::move(arg);
    return Init_QRResult_altitude(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_drone_spacing
{
public:
  explicit Init_QRResult_drone_spacing(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_altitude_active drone_spacing(::swarm_msgs::msg::QRResult::_drone_spacing_type arg)
  {
    msg_.drone_spacing = std::move(arg);
    return Init_QRResult_altitude_active(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_formation_type
{
public:
  explicit Init_QRResult_formation_type(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_drone_spacing formation_type(::swarm_msgs::msg::QRResult::_formation_type_type arg)
  {
    msg_.formation_type = std::move(arg);
    return Init_QRResult_drone_spacing(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_formation_active
{
public:
  explicit Init_QRResult_formation_active(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_formation_type formation_active(::swarm_msgs::msg::QRResult::_formation_active_type arg)
  {
    msg_.formation_active = std::move(arg);
    return Init_QRResult_formation_type(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_qr_id
{
public:
  explicit Init_QRResult_qr_id(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_formation_active qr_id(::swarm_msgs::msg::QRResult::_qr_id_type arg)
  {
    msg_.qr_id = std::move(arg);
    return Init_QRResult_formation_active(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_team_id
{
public:
  explicit Init_QRResult_team_id(::swarm_msgs::msg::QRResult & msg)
  : msg_(msg)
  {}
  Init_QRResult_qr_id team_id(::swarm_msgs::msg::QRResult::_team_id_type arg)
  {
    msg_.team_id = std::move(arg);
    return Init_QRResult_qr_id(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

class Init_QRResult_header
{
public:
  Init_QRResult_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QRResult_team_id header(::swarm_msgs::msg::QRResult::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_QRResult_team_id(msg_);
  }

private:
  ::swarm_msgs::msg::QRResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::QRResult>()
{
  return swarm_msgs::msg::builder::Init_QRResult_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__QR_RESULT__BUILDER_HPP_
