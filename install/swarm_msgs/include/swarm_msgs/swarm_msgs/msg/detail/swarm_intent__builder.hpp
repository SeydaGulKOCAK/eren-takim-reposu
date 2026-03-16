// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/swarm_intent__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_SwarmIntent_wait_until
{
public:
  explicit Init_SwarmIntent_wait_until(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::SwarmIntent wait_until(::swarm_msgs::msg::SwarmIntent::_wait_until_type arg)
  {
    msg_.wait_until = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_qr_seq
{
public:
  explicit Init_SwarmIntent_qr_seq(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_wait_until qr_seq(::swarm_msgs::msg::SwarmIntent::_qr_seq_type arg)
  {
    msg_.qr_seq = std::move(arg);
    return Init_SwarmIntent_wait_until(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_join_drone_id
{
public:
  explicit Init_SwarmIntent_join_drone_id(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_qr_seq join_drone_id(::swarm_msgs::msg::SwarmIntent::_join_drone_id_type arg)
  {
    msg_.join_drone_id = std::move(arg);
    return Init_SwarmIntent_qr_seq(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_active_drone_count
{
public:
  explicit Init_SwarmIntent_active_drone_count(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_join_drone_id active_drone_count(::swarm_msgs::msg::SwarmIntent::_active_drone_count_type arg)
  {
    msg_.active_drone_count = std::move(arg);
    return Init_SwarmIntent_join_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_maneuver_roll_deg
{
public:
  explicit Init_SwarmIntent_maneuver_roll_deg(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_active_drone_count maneuver_roll_deg(::swarm_msgs::msg::SwarmIntent::_maneuver_roll_deg_type arg)
  {
    msg_.maneuver_roll_deg = std::move(arg);
    return Init_SwarmIntent_active_drone_count(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_maneuver_pitch_deg
{
public:
  explicit Init_SwarmIntent_maneuver_pitch_deg(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_maneuver_roll_deg maneuver_pitch_deg(::swarm_msgs::msg::SwarmIntent::_maneuver_pitch_deg_type arg)
  {
    msg_.maneuver_pitch_deg = std::move(arg);
    return Init_SwarmIntent_maneuver_roll_deg(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_maneuver_active
{
public:
  explicit Init_SwarmIntent_maneuver_active(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_maneuver_pitch_deg maneuver_active(::swarm_msgs::msg::SwarmIntent::_maneuver_active_type arg)
  {
    msg_.maneuver_active = std::move(arg);
    return Init_SwarmIntent_maneuver_pitch_deg(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_zone_color
{
public:
  explicit Init_SwarmIntent_zone_color(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_maneuver_active zone_color(::swarm_msgs::msg::SwarmIntent::_zone_color_type arg)
  {
    msg_.zone_color = std::move(arg);
    return Init_SwarmIntent_maneuver_active(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_detach_drone_id
{
public:
  explicit Init_SwarmIntent_detach_drone_id(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_zone_color detach_drone_id(::swarm_msgs::msg::SwarmIntent::_detach_drone_id_type arg)
  {
    msg_.detach_drone_id = std::move(arg);
    return Init_SwarmIntent_zone_color(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_drone_altitude
{
public:
  explicit Init_SwarmIntent_drone_altitude(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_detach_drone_id drone_altitude(::swarm_msgs::msg::SwarmIntent::_drone_altitude_type arg)
  {
    msg_.drone_altitude = std::move(arg);
    return Init_SwarmIntent_detach_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_target_pos
{
public:
  explicit Init_SwarmIntent_target_pos(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_drone_altitude target_pos(::swarm_msgs::msg::SwarmIntent::_target_pos_type arg)
  {
    msg_.target_pos = std::move(arg);
    return Init_SwarmIntent_drone_altitude(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_target_yaw
{
public:
  explicit Init_SwarmIntent_target_yaw(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_target_pos target_yaw(::swarm_msgs::msg::SwarmIntent::_target_yaw_type arg)
  {
    msg_.target_yaw = std::move(arg);
    return Init_SwarmIntent_target_pos(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_drone_spacing
{
public:
  explicit Init_SwarmIntent_drone_spacing(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_target_yaw drone_spacing(::swarm_msgs::msg::SwarmIntent::_drone_spacing_type arg)
  {
    msg_.drone_spacing = std::move(arg);
    return Init_SwarmIntent_target_yaw(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_formation_type
{
public:
  explicit Init_SwarmIntent_formation_type(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_drone_spacing formation_type(::swarm_msgs::msg::SwarmIntent::_formation_type_type arg)
  {
    msg_.formation_type = std::move(arg);
    return Init_SwarmIntent_drone_spacing(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_task_id
{
public:
  explicit Init_SwarmIntent_task_id(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_formation_type task_id(::swarm_msgs::msg::SwarmIntent::_task_id_type arg)
  {
    msg_.task_id = std::move(arg);
    return Init_SwarmIntent_formation_type(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_leader_id
{
public:
  explicit Init_SwarmIntent_leader_id(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_task_id leader_id(::swarm_msgs::msg::SwarmIntent::_leader_id_type arg)
  {
    msg_.leader_id = std::move(arg);
    return Init_SwarmIntent_task_id(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_seq
{
public:
  explicit Init_SwarmIntent_seq(::swarm_msgs::msg::SwarmIntent & msg)
  : msg_(msg)
  {}
  Init_SwarmIntent_leader_id seq(::swarm_msgs::msg::SwarmIntent::_seq_type arg)
  {
    msg_.seq = std::move(arg);
    return Init_SwarmIntent_leader_id(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

class Init_SwarmIntent_header
{
public:
  Init_SwarmIntent_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SwarmIntent_seq header(::swarm_msgs::msg::SwarmIntent::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_SwarmIntent_seq(msg_);
  }

private:
  ::swarm_msgs::msg::SwarmIntent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::SwarmIntent>()
{
  return swarm_msgs::msg::builder::Init_SwarmIntent_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__BUILDER_HPP_
