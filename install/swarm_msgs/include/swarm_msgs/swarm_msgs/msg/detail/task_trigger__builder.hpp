// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/TaskTrigger.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/task_trigger__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_TaskTrigger_team_id
{
public:
  explicit Init_TaskTrigger_team_id(::swarm_msgs::msg::TaskTrigger & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::TaskTrigger team_id(::swarm_msgs::msg::TaskTrigger::_team_id_type arg)
  {
    msg_.team_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::TaskTrigger msg_;
};

class Init_TaskTrigger_start
{
public:
  explicit Init_TaskTrigger_start(::swarm_msgs::msg::TaskTrigger & msg)
  : msg_(msg)
  {}
  Init_TaskTrigger_team_id start(::swarm_msgs::msg::TaskTrigger::_start_type arg)
  {
    msg_.start = std::move(arg);
    return Init_TaskTrigger_team_id(msg_);
  }

private:
  ::swarm_msgs::msg::TaskTrigger msg_;
};

class Init_TaskTrigger_task_type
{
public:
  explicit Init_TaskTrigger_task_type(::swarm_msgs::msg::TaskTrigger & msg)
  : msg_(msg)
  {}
  Init_TaskTrigger_start task_type(::swarm_msgs::msg::TaskTrigger::_task_type_type arg)
  {
    msg_.task_type = std::move(arg);
    return Init_TaskTrigger_start(msg_);
  }

private:
  ::swarm_msgs::msg::TaskTrigger msg_;
};

class Init_TaskTrigger_header
{
public:
  Init_TaskTrigger_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TaskTrigger_task_type header(::swarm_msgs::msg::TaskTrigger::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TaskTrigger_task_type(msg_);
  }

private:
  ::swarm_msgs::msg::TaskTrigger msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::TaskTrigger>()
{
  return swarm_msgs::msg::builder::Init_TaskTrigger_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__TASK_TRIGGER__BUILDER_HPP_
