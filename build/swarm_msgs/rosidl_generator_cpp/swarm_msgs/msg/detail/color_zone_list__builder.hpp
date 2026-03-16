// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/ColorZoneList.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/color_zone_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_ColorZoneList_zones
{
public:
  explicit Init_ColorZoneList_zones(::swarm_msgs::msg::ColorZoneList & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::ColorZoneList zones(::swarm_msgs::msg::ColorZoneList::_zones_type arg)
  {
    msg_.zones = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::ColorZoneList msg_;
};

class Init_ColorZoneList_header
{
public:
  Init_ColorZoneList_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ColorZoneList_zones header(::swarm_msgs::msg::ColorZoneList::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ColorZoneList_zones(msg_);
  }

private:
  ::swarm_msgs::msg::ColorZoneList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::ColorZoneList>()
{
  return swarm_msgs::msg::builder::Init_ColorZoneList_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__BUILDER_HPP_
