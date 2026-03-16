// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from swarm_msgs:msg/ColorZoneList.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__TRAITS_HPP_
#define SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "swarm_msgs/msg/detail/color_zone_list__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'zones'
#include "swarm_msgs/msg/detail/color_zone__traits.hpp"

namespace swarm_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ColorZoneList & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: zones
  {
    if (msg.zones.size() == 0) {
      out << "zones: []";
    } else {
      out << "zones: [";
      size_t pending_items = msg.zones.size();
      for (auto item : msg.zones) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ColorZoneList & msg,
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

  // member: zones
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.zones.size() == 0) {
      out << "zones: []\n";
    } else {
      out << "zones:\n";
      for (auto item : msg.zones) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ColorZoneList & msg, bool use_flow_style = false)
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
  const swarm_msgs::msg::ColorZoneList & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::msg::ColorZoneList & msg)
{
  return swarm_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::msg::ColorZoneList>()
{
  return "swarm_msgs::msg::ColorZoneList";
}

template<>
inline const char * name<swarm_msgs::msg::ColorZoneList>()
{
  return "swarm_msgs/msg/ColorZoneList";
}

template<>
struct has_fixed_size<swarm_msgs::msg::ColorZoneList>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::msg::ColorZoneList>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::msg::ColorZoneList>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SWARM_MSGS__MSG__DETAIL__COLOR_ZONE_LIST__TRAITS_HPP_
