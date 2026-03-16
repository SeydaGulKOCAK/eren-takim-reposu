// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from swarm_msgs:msg/SwarmIntent.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__TRAITS_HPP_
#define SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "swarm_msgs/msg/detail/swarm_intent__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'target_pos'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'wait_until'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace swarm_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const SwarmIntent & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: seq
  {
    out << "seq: ";
    rosidl_generator_traits::value_to_yaml(msg.seq, out);
    out << ", ";
  }

  // member: leader_id
  {
    out << "leader_id: ";
    rosidl_generator_traits::value_to_yaml(msg.leader_id, out);
    out << ", ";
  }

  // member: task_id
  {
    out << "task_id: ";
    rosidl_generator_traits::value_to_yaml(msg.task_id, out);
    out << ", ";
  }

  // member: formation_type
  {
    out << "formation_type: ";
    rosidl_generator_traits::value_to_yaml(msg.formation_type, out);
    out << ", ";
  }

  // member: drone_spacing
  {
    out << "drone_spacing: ";
    rosidl_generator_traits::value_to_yaml(msg.drone_spacing, out);
    out << ", ";
  }

  // member: target_yaw
  {
    out << "target_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.target_yaw, out);
    out << ", ";
  }

  // member: target_pos
  {
    out << "target_pos: ";
    to_flow_style_yaml(msg.target_pos, out);
    out << ", ";
  }

  // member: drone_altitude
  {
    out << "drone_altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.drone_altitude, out);
    out << ", ";
  }

  // member: detach_drone_id
  {
    out << "detach_drone_id: ";
    rosidl_generator_traits::value_to_yaml(msg.detach_drone_id, out);
    out << ", ";
  }

  // member: zone_color
  {
    out << "zone_color: ";
    rosidl_generator_traits::value_to_yaml(msg.zone_color, out);
    out << ", ";
  }

  // member: maneuver_active
  {
    out << "maneuver_active: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_active, out);
    out << ", ";
  }

  // member: maneuver_pitch_deg
  {
    out << "maneuver_pitch_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_pitch_deg, out);
    out << ", ";
  }

  // member: maneuver_roll_deg
  {
    out << "maneuver_roll_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_roll_deg, out);
    out << ", ";
  }

  // member: active_drone_count
  {
    out << "active_drone_count: ";
    rosidl_generator_traits::value_to_yaml(msg.active_drone_count, out);
    out << ", ";
  }

  // member: join_drone_id
  {
    out << "join_drone_id: ";
    rosidl_generator_traits::value_to_yaml(msg.join_drone_id, out);
    out << ", ";
  }

  // member: qr_seq
  {
    out << "qr_seq: ";
    rosidl_generator_traits::value_to_yaml(msg.qr_seq, out);
    out << ", ";
  }

  // member: wait_until
  {
    out << "wait_until: ";
    to_flow_style_yaml(msg.wait_until, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SwarmIntent & msg,
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

  // member: seq
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "seq: ";
    rosidl_generator_traits::value_to_yaml(msg.seq, out);
    out << "\n";
  }

  // member: leader_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "leader_id: ";
    rosidl_generator_traits::value_to_yaml(msg.leader_id, out);
    out << "\n";
  }

  // member: task_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task_id: ";
    rosidl_generator_traits::value_to_yaml(msg.task_id, out);
    out << "\n";
  }

  // member: formation_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "formation_type: ";
    rosidl_generator_traits::value_to_yaml(msg.formation_type, out);
    out << "\n";
  }

  // member: drone_spacing
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drone_spacing: ";
    rosidl_generator_traits::value_to_yaml(msg.drone_spacing, out);
    out << "\n";
  }

  // member: target_yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.target_yaw, out);
    out << "\n";
  }

  // member: target_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_pos:\n";
    to_block_style_yaml(msg.target_pos, out, indentation + 2);
  }

  // member: drone_altitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "drone_altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.drone_altitude, out);
    out << "\n";
  }

  // member: detach_drone_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "detach_drone_id: ";
    rosidl_generator_traits::value_to_yaml(msg.detach_drone_id, out);
    out << "\n";
  }

  // member: zone_color
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "zone_color: ";
    rosidl_generator_traits::value_to_yaml(msg.zone_color, out);
    out << "\n";
  }

  // member: maneuver_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "maneuver_active: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_active, out);
    out << "\n";
  }

  // member: maneuver_pitch_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "maneuver_pitch_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_pitch_deg, out);
    out << "\n";
  }

  // member: maneuver_roll_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "maneuver_roll_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_roll_deg, out);
    out << "\n";
  }

  // member: active_drone_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active_drone_count: ";
    rosidl_generator_traits::value_to_yaml(msg.active_drone_count, out);
    out << "\n";
  }

  // member: join_drone_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "join_drone_id: ";
    rosidl_generator_traits::value_to_yaml(msg.join_drone_id, out);
    out << "\n";
  }

  // member: qr_seq
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "qr_seq: ";
    rosidl_generator_traits::value_to_yaml(msg.qr_seq, out);
    out << "\n";
  }

  // member: wait_until
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wait_until:\n";
    to_block_style_yaml(msg.wait_until, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SwarmIntent & msg, bool use_flow_style = false)
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
  const swarm_msgs::msg::SwarmIntent & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::msg::SwarmIntent & msg)
{
  return swarm_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::msg::SwarmIntent>()
{
  return "swarm_msgs::msg::SwarmIntent";
}

template<>
inline const char * name<swarm_msgs::msg::SwarmIntent>()
{
  return "swarm_msgs/msg/SwarmIntent";
}

template<>
struct has_fixed_size<swarm_msgs::msg::SwarmIntent>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::msg::SwarmIntent>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::msg::SwarmIntent>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SWARM_MSGS__MSG__DETAIL__SWARM_INTENT__TRAITS_HPP_
