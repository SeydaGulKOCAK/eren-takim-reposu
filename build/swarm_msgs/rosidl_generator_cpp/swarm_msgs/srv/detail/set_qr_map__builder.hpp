// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from swarm_msgs:srv/SetQRMap.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__BUILDER_HPP_
#define SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "swarm_msgs/srv/detail/set_qr_map__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace swarm_msgs
{

namespace srv
{

namespace builder
{

class Init_SetQRMap_Request_next_qr_ids
{
public:
  explicit Init_SetQRMap_Request_next_qr_ids(::swarm_msgs::srv::SetQRMap_Request & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::srv::SetQRMap_Request next_qr_ids(::swarm_msgs::srv::SetQRMap_Request::_next_qr_ids_type arg)
  {
    msg_.next_qr_ids = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::srv::SetQRMap_Request msg_;
};

class Init_SetQRMap_Request_qr_ids
{
public:
  explicit Init_SetQRMap_Request_qr_ids(::swarm_msgs::srv::SetQRMap_Request & msg)
  : msg_(msg)
  {}
  Init_SetQRMap_Request_next_qr_ids qr_ids(::swarm_msgs::srv::SetQRMap_Request::_qr_ids_type arg)
  {
    msg_.qr_ids = std::move(arg);
    return Init_SetQRMap_Request_next_qr_ids(msg_);
  }

private:
  ::swarm_msgs::srv::SetQRMap_Request msg_;
};

class Init_SetQRMap_Request_qr_positions
{
public:
  Init_SetQRMap_Request_qr_positions()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetQRMap_Request_qr_ids qr_positions(::swarm_msgs::srv::SetQRMap_Request::_qr_positions_type arg)
  {
    msg_.qr_positions = std::move(arg);
    return Init_SetQRMap_Request_qr_ids(msg_);
  }

private:
  ::swarm_msgs::srv::SetQRMap_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::srv::SetQRMap_Request>()
{
  return swarm_msgs::srv::builder::Init_SetQRMap_Request_qr_positions();
}

}  // namespace swarm_msgs


namespace swarm_msgs
{

namespace srv
{

namespace builder
{

class Init_SetQRMap_Response_message
{
public:
  explicit Init_SetQRMap_Response_message(::swarm_msgs::srv::SetQRMap_Response & msg)
  : msg_(msg)
  {}
  ::swarm_msgs::srv::SetQRMap_Response message(::swarm_msgs::srv::SetQRMap_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::swarm_msgs::srv::SetQRMap_Response msg_;
};

class Init_SetQRMap_Response_success
{
public:
  Init_SetQRMap_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetQRMap_Response_message success(::swarm_msgs::srv::SetQRMap_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetQRMap_Response_message(msg_);
  }

private:
  ::swarm_msgs::srv::SetQRMap_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::swarm_msgs::srv::SetQRMap_Response>()
{
  return swarm_msgs::srv::builder::Init_SetQRMap_Response_success();
}

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__BUILDER_HPP_
