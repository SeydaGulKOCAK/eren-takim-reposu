// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:msg/LocalState.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__BUILDER_HPP_
#define SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/msg/detail/local_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace msg
{

namespace builder
{

class Init_LocalState_seq
{
public:
  explicit Init_LocalState_seq(::swarm_msgs::msg::LocalState & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::msg::LocalState seq(::swarm_msgs::msg::LocalState::_seq_type arg)
  {
    msg_.seq = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::msg::LocalState msg_;
};

class Init_LocalState_state
{
public:
  explicit Init_LocalState_state(::swarm_msgs::msg::LocalState & msg)
  : msg_(msg)
  {}
  Init_LocalState_seq state(::swarm_msgs::msg::LocalState::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_LocalState_seq(msg_);
  }

private:
  ::swarm_msgs::msg::LocalState msg_;
};

class Init_LocalState_drone_id
{
public:
  explicit Init_LocalState_drone_id(::swarm_msgs::msg::LocalState & msg)
  : msg_(msg)
  {}
  Init_LocalState_state drone_id(::swarm_msgs::msg::LocalState::_drone_id_type arg)
  {
    msg_.drone_id = std::move(arg);
    return Init_LocalState_state(msg_);
  }

private:
  ::swarm_msgs::msg::LocalState msg_;
};

class Init_LocalState_header
{
public:
  Init_LocalState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LocalState_drone_id header(::swarm_msgs::msg::LocalState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_LocalState_drone_id(msg_);
  }

private:
  ::swarm_msgs::msg::LocalState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::msg::LocalState>()
{
  return swarm_msgs::msg::builder::Init_LocalState_header();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__MSG__DETAIL__LOCAL_STATE__BUILDER_HPP_
