// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__QR_RESULT__TRAITS_HPP_
#define SWARM_MSGS__MSG__DETAIL__QR_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "swarm_msgs/msg/detail/qr_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'qr_position'
// Member 'next_qr_position'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace swarm_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const QRResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: team_id
  {
    out << "team_id: ";
    rosidl_generator_traits::value_to_yaml(msg.team_id, out);
    out << ", ";
  }

  // member: qr_id
  {
    out << "qr_id: ";
    rosidl_generator_traits::value_to_yaml(msg.qr_id, out);
    out << ", ";
  }

  // member: formation_active
  {
    out << "formation_active: ";
    rosidl_generator_traits::value_to_yaml(msg.formation_active, out);
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

  // member: altitude_active
  {
    out << "altitude_active: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude_active, out);
    out << ", ";
  }

  // member: altitude
  {
    out << "altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude, out);
    out << ", ";
  }

  // member: maneuver_active
  {
    out << "maneuver_active: ";
    rosidl_generator_traits::value_to_yaml(msg.maneuver_active, out);
    out << ", ";
  }

  // member: pitch_deg
  {
    out << "pitch_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch_deg, out);
    out << ", ";
  }

  // member: roll_deg
  {
    out << "roll_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.roll_deg, out);
    out << ", ";
  }

  // member: detach_active
  {
    out << "detach_active: ";
    rosidl_generator_traits::value_to_yaml(msg.detach_active, out);
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

  // member: next_qr_id
  {
    out << "next_qr_id: ";
    rosidl_generator_traits::value_to_yaml(msg.next_qr_id, out);
    out << ", ";
  }

  // member: qr_position
  {
    out << "qr_position: ";
    to_flow_style_yaml(msg.qr_position, out);
    out << ", ";
  }

  // member: next_qr_position
  {
    out << "next_qr_position: ";
    to_flow_style_yaml(msg.next_qr_position, out);
    out << ", ";
  }

  // member: wait_seconds
  {
    out << "wait_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.wait_seconds, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const QRResult & msg,
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

  // member: team_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "team_id: ";
    rosidl_generator_traits::value_to_yaml(msg.team_id, out);
    out << "\n";
  }

  // member: qr_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "qr_id: ";
    rosidl_generator_traits::value_to_yaml(msg.qr_id, out);
    out << "\n";
  }

  // member: formation_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "formation_active: ";
    rosidl_generator_traits::value_to_yaml(msg.formation_active, out);
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

  // member: altitude_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "altitude_active: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude_active, out);
    out << "\n";
  }

  // member: altitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude, out);
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

  // member: pitch_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch_deg, out);
    out << "\n";
  }

  // member: roll_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.roll_deg, out);
    out << "\n";
  }

  // member: detach_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "detach_active: ";
    rosidl_generator_traits::value_to_yaml(msg.detach_active, out);
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

  // member: next_qr_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "next_qr_id: ";
    rosidl_generator_traits::value_to_yaml(msg.next_qr_id, out);
    out << "\n";
  }

  // member: qr_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "qr_position:\n";
    to_block_style_yaml(msg.qr_position, out, indentation + 2);
  }

  // member: next_qr_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "next_qr_position:\n";
    to_block_style_yaml(msg.next_qr_position, out, indentation + 2);
  }

  // member: wait_seconds
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wait_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.wait_seconds, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const QRResult & msg, bool use_flow_style = false)
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
  const swarm_msgs::msg::QRResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::msg::QRResult & msg)
{
  return swarm_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::msg::QRResult>()
{
  return "swarm_msgs::msg::QRResult";
}

template<>
inline const char * name<swarm_msgs::msg::QRResult>()
{
  return "swarm_msgs/msg/QRResult";
}

template<>
struct has_fixed_size<swarm_msgs::msg::QRResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::msg::QRResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::msg::QRResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SWARM_MSGS__MSG__DETAIL__QR_RESULT__TRAITS_HPP_
