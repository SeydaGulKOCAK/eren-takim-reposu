// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from swarm_msgs:msg/TeleopCmd.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__TRAITS_HPP_
#define SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "swarm_msgs/msg/detail/teleop_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'execute_at'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace swarm_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const TeleopCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << ", ";
  }

  // member: vx
  {
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << ", ";
  }

  // member: vy
  {
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << ", ";
  }

  // member: vz
  {
    out << "vz: ";
    rosidl_generator_traits::value_to_yaml(msg.vz, out);
    out << ", ";
  }

  // member: yaw_rate
  {
    out << "yaw_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_rate, out);
    out << ", ";
  }

  // member: execute_at
  {
    out << "execute_at: ";
    to_flow_style_yaml(msg.execute_at, out);
    out << ", ";
  }

  // member: new_formation_type
  {
    out << "new_formation_type: ";
    rosidl_generator_traits::value_to_yaml(msg.new_formation_type, out);
    out << ", ";
  }

  // member: new_spacing
  {
    out << "new_spacing: ";
    rosidl_generator_traits::value_to_yaml(msg.new_spacing, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TeleopCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }

  // member: vx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << "\n";
  }

  // member: vy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << "\n";
  }

  // member: vz
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vz: ";
    rosidl_generator_traits::value_to_yaml(msg.vz, out);
    out << "\n";
  }

  // member: yaw_rate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_rate, out);
    out << "\n";
  }

  // member: execute_at
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "execute_at:\n";
    to_block_style_yaml(msg.execute_at, out, indentation + 2);
  }

  // member: new_formation_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "new_formation_type: ";
    rosidl_generator_traits::value_to_yaml(msg.new_formation_type, out);
    out << "\n";
  }

  // member: new_spacing
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "new_spacing: ";
    rosidl_generator_traits::value_to_yaml(msg.new_spacing, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TeleopCmd & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace swarm_msgs

namespace rosidl_generator_traits
{

[[deprecated("use swarm_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const swarm_msgs::msg::TeleopCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::msg::TeleopCmd & msg)
{
  return swarm_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::msg::TeleopCmd>()
{
  return "swarm_msgs::msg::TeleopCmd";
}

template<>
inline const char * name<swarm_msgs::msg::TeleopCmd>()
{
  return "swarm_msgs/msg/TeleopCmd";
}

template<>
struct has_fixed_size<swarm_msgs::msg::TeleopCmd>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::msg::TeleopCmd>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::msg::TeleopCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SWARM_MSGS__MSG__DETAIL__TELEOP_CMD__TRAITS_HPP_
