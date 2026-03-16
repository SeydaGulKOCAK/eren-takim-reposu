// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/JoinRequest.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/join_request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_JoinRequest_ready
{
public:
  explicit Init_JoinRequest_ready(::swarm_msgs::msg::JoinRequest & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::JoinRequest ready(::swarm_msgs::msg::JoinRequest::_ready_type arg)
  {
    msg_.ready = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::JoinRequest msg_;
};

class Init_JoinRequest_battery_pct
{
public:
  explicit Init_JoinRequest_battery_pct(::swarm_msgs::msg::JoinRequest & msg)
  : msg_(msg)
  {}
  Init_JoinRequest_ready battery_pct(::swarm_msgs::msg::JoinRequest::_battery_pct_type arg)
  {
    msg_.battery_pct = std::move(arg);
    return Init_JoinRequest_ready(msg_);
  }

private:
  ::swarm_msgs::msg::JoinRequest msg_;
};

class Init_JoinRequest_drone_id
{
public:
  explicit Init_JoinRequest_drone_id(::swarm_msgs::msg::JoinRequest & msg)
  : msg_(msg)
  {}
  Init_JoinRequest_battery_pct drone_id(::swarm_msgs::msg::JoinRequest::_drone_id_type arg)
  {
    msg_.drone_id = std::move(arg);
    return Init_JoinRequest_battery_pct(msg_);
  }

private:
  ::swarm_msgs::msg::JoinRequest msg_;
};

class Init_JoinRequest_header
{
public:
  Init_JoinRequest_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_JoinRequest_drone_id header(::swarm_msgs::msg::JoinRequest::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_JoinRequest_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::JoinRequest msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::JoinRequest>()
{
  return swarm_msgs::msg::builder::Init_JoinRequest_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__JOIN_REQUEST__BUILDER_HPP_
