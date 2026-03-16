// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/FormationCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/formation_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_FormationCmd_active_drone_count
{
public:
  explicit Init_FormationCmd_active_drone_count(::swarm_msgs::msg::FormationCmd & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::FormationCmd active_drone_count(::swarm_msgs::msg::FormationCmd::_active_drone_count_type arg)
  {
    msg_.active_drone_count = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::FormationCmd msg_;
};

class Init_FormationCmd_target_yaw
{
public:
  explicit Init_FormationCmd_target_yaw(::swarm_msgs::msg::FormationCmd & msg)
  : msg_(msg)
  {}
  Init_FormationCmd_active_drone_count target_yaw(::swarm_msgs::msg::FormationCmd::_target_yaw_type arg)
  {
    msg_.target_yaw = std::move(arg);
    return Init_FormationCmd_active_drone_count(msg_);
  }

private:
  ::swarm_msgs::msg::FormationCmd msg_;
};

class Init_FormationCmd_drone_spacing
{
public:
  explicit Init_FormationCmd_drone_spacing(::swarm_msgs::msg::FormationCmd & msg)
  : msg_(msg)
  {}
  Init_FormationCmd_target_yaw drone_spacing(::swarm_msgs::msg::FormationCmd::_drone_spacing_type arg)
  {
    msg_.drone_spacing = std::move(arg);
    return Init_FormationCmd_target_yaw(msg_);
  }

private:
  ::swarm_msgs::msg::FormationCmd msg_;
};

class Init_FormationCmd_formation_type
{
public:
  explicit Init_FormationCmd_formation_type(::swarm_msgs::msg::FormationCmd & msg)
  : msg_(msg)
  {}
  Init_FormationCmd_drone_spacing formation_type(::swarm_msgs::msg::FormationCmd::_formation_type_type arg)
  {
    msg_.formation_type = std::move(arg);
    return Init_FormationCmd_drone_spacing(msg_);
  }

private:
  ::swarm_msgs::msg::FormationCmd msg_;
};

class Init_FormationCmd_header
{
public:
  Init_FormationCmd_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FormationCmd_formation_type header(::swarm_msgs::msg::FormationCmd::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_FormationCmd_formation_type(msg_);
  }

private:
  ::swarm_msgs::msg::FormationCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::FormationCmd>()
{
  return swarm_msgs::msg::builder::Init_FormationCmd_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__FORMATION_CMD__BUILDER_HPP_
