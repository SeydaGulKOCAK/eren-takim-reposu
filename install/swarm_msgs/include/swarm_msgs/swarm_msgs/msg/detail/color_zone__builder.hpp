// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/ColorZone.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/color_zone__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_ColorZone_radius
{
public:
  explicit Init_ColorZone_radius(::swarm_msgs::msg::ColorZone & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::ColorZone radius(::swarm_msgs::msg::ColorZone::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::ColorZone msg_;
};

class Init_ColorZone_color
{
public:
  explicit Init_ColorZone_color(::swarm_msgs::msg::ColorZone & msg)
  : msg_(msg)
  {}
  Init_ColorZone_radius color(::swarm_msgs::msg::ColorZone::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_ColorZone_radius(msg_);
  }

private:
  ::swarm_msgs::msg::ColorZone msg_;
};

class Init_ColorZone_position
{
public:
  Init_ColorZone_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ColorZone_color position(::swarm_msgs::msg::ColorZone::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_ColorZone_color(msg_);
  }

private:
  ::swarm_msgs::msg::ColorZone msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::ColorZone>()
{
  return swarm_msgs::msg::builder::Init_ColorZone_position();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE__BUILDER_HPP_
