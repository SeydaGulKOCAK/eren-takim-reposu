// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/SafetyEvent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/safety_event__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_SafetyEvent_severity
{
public:
  explicit Init_SafetyEvent_severity(::swarm_msgs::msg::SafetyEvent & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::SafetyEvent severity(::swarm_msgs::msg::SafetyEvent::_severity_type arg)
  {
    msg_.severity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::SafetyEvent msg_;
};

class Init_SafetyEvent_description
{
public:
  explicit Init_SafetyEvent_description(::swarm_msgs::msg::SafetyEvent & msg)
  : msg_(msg)
  {}
  Init_SafetyEvent_severity description(::swarm_msgs::msg::SafetyEvent::_description_type arg)
  {
    msg_.description = std::move(arg);
    return Init_SafetyEvent_severity(msg_);
  }

private:
  ::swarm_msgs::msg::SafetyEvent msg_;
};

class Init_SafetyEvent_event_type
{
public:
  explicit Init_SafetyEvent_event_type(::swarm_msgs::msg::SafetyEvent & msg)
  : msg_(msg)
  {}
  Init_SafetyEvent_description event_type(::swarm_msgs::msg::SafetyEvent::_event_type_type arg)
  {
    msg_.event_type = std::move(arg);
    return Init_SafetyEvent_description(msg_);
  }

private:
  ::swarm_msgs::msg::SafetyEvent msg_;
};

class Init_SafetyEvent_drone_id
{
public:
  explicit Init_SafetyEvent_drone_id(::swarm_msgs::msg::SafetyEvent & msg)
  : msg_(msg)
  {}
  Init_SafetyEvent_event_type drone_id(::swarm_msgs::msg::SafetyEvent::_drone_id_type arg)
  {
    msg_.drone_id = std::move(arg);
    return Init_SafetyEvent_event_type(msg_);
  }

private:
  ::swarm_msgs::msg::SafetyEvent msg_;
};

class Init_SafetyEvent_header
{
public:
  Init_SafetyEvent_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SafetyEvent_drone_id header(::swarm_msgs::msg::SafetyEvent::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_SafetyEvent_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::SafetyEvent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::SafetyEvent>()
{
  return swarm_msgs::msg::builder::Init_SafetyEvent_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__SAFETY_EVENT__BUILDER_HPP_
