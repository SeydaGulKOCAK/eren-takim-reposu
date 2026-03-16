// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/TeleopCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/teleop_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_TeleopCmd_new_spacing
{
public:
  explicit Init_TeleopCmd_new_spacing(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::TeleopCmd new_spacing(::swarm_msgs::msg::TeleopCmd::_new_spacing_type arg)
  {
    msg_.new_spacing = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_new_formation_type
{
public:
  explicit Init_TeleopCmd_new_formation_type(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_new_spacing new_formation_type(::swarm_msgs::msg::TeleopCmd::_new_formation_type_type arg)
  {
    msg_.new_formation_type = std::move(arg);
    return Init_TeleopCmd_new_spacing(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_execute_at
{
public:
  explicit Init_TeleopCmd_execute_at(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_new_formation_type execute_at(::swarm_msgs::msg::TeleopCmd::_execute_at_type arg)
  {
    msg_.execute_at = std::move(arg);
    return Init_TeleopCmd_new_formation_type(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_yaw_rate
{
public:
  explicit Init_TeleopCmd_yaw_rate(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_execute_at yaw_rate(::swarm_msgs::msg::TeleopCmd::_yaw_rate_type arg)
  {
    msg_.yaw_rate = std::move(arg);
    return Init_TeleopCmd_execute_at(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_vz
{
public:
  explicit Init_TeleopCmd_vz(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_yaw_rate vz(::swarm_msgs::msg::TeleopCmd::_vz_type arg)
  {
    msg_.vz = std::move(arg);
    return Init_TeleopCmd_yaw_rate(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_vy
{
public:
  explicit Init_TeleopCmd_vy(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_vz vy(::swarm_msgs::msg::TeleopCmd::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return Init_TeleopCmd_vz(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_vx
{
public:
  explicit Init_TeleopCmd_vx(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_vy vx(::swarm_msgs::msg::TeleopCmd::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_TeleopCmd_vy(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_mode
{
public:
  explicit Init_TeleopCmd_mode(::swarm_msgs::msg::TeleopCmd & msg)
  : msg_(msg)
  {}
  Init_TeleopCmd_vx mode(::swarm_msgs::msg::TeleopCmd::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return Init_TeleopCmd_vx(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

class Init_TeleopCmd_header
{
public:
  Init_TeleopCmd_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TeleopCmd_mode header(::swarm_msgs::msg::TeleopCmd::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TeleopCmd_mode(msg_);
  }

private:
  ::swarm_msgs::msg::TeleopCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::TeleopCmd>()
{
  return swarm_msgs::msg::builder::Init_TeleopCmd_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__BUILDER_HPP_
