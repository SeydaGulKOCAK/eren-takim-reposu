// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from swarm_msgs:srv/SetQRMap.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__TRAITS_HPP_
#define SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "swarm_msgs/srv/detail/set_qr_map__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'qr_positions'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace swarm_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetQRMap_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: qr_positions
  {
    if (msg.qr_positions.size() == 0) {
      out << "qr_positions: []";
    } else {
      out << "qr_positions: [";
      size_t pending_items = msg.qr_positions.size();
      for (auto item : msg.qr_positions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: qr_ids
  {
    if (msg.qr_ids.size() == 0) {
      out << "qr_ids: []";
    } else {
      out << "qr_ids: [";
      size_t pending_items = msg.qr_ids.size();
      for (auto item : msg.qr_ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: next_qr_ids
  {
    if (msg.next_qr_ids.size() == 0) {
      out << "next_qr_ids: []";
    } else {
      out << "next_qr_ids: [";
      size_t pending_items = msg.next_qr_ids.size();
      for (auto item : msg.next_qr_ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const SetQRMap_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: qr_positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.qr_positions.size() == 0) {
      out << "qr_positions: []\n";
    } else {
      out << "qr_positions:\n";
      for (auto item : msg.qr_positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: qr_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.qr_ids.size() == 0) {
      out << "qr_ids: []\n";
    } else {
      out << "qr_ids:\n";
      for (auto item : msg.qr_ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: next_qr_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.next_qr_ids.size() == 0) {
      out << "next_qr_ids: []\n";
    } else {
      out << "next_qr_ids:\n";
      for (auto item : msg.next_qr_ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetQRMap_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace swarm_msgs

namespace rosidl_generator_traits
{

[[deprecated("use swarm_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const swarm_msgs::srv::SetQRMap_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::srv::SetQRMap_Request & msg)
{
  return swarm_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::srv::SetQRMap_Request>()
{
  return "swarm_msgs::srv::SetQRMap_Request";
}

template<>
inline const char * name<swarm_msgs::srv::SetQRMap_Request>()
{
  return "swarm_msgs/srv/SetQRMap_Request";
}

template<>
struct has_fixed_size<swarm_msgs::srv::SetQRMap_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::srv::SetQRMap_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::srv::SetQRMap_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace swarm_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetQRMap_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetQRMap_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetQRMap_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace swarm_msgs

namespace rosidl_generator_traits
{

[[deprecated("use swarm_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const swarm_msgs::srv::SetQRMap_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  swarm_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use swarm_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const swarm_msgs::srv::SetQRMap_Response & msg)
{
  return swarm_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<swarm_msgs::srv::SetQRMap_Response>()
{
  return "swarm_msgs::srv::SetQRMap_Response";
}

template<>
inline const char * name<swarm_msgs::srv::SetQRMap_Response>()
{
  return "swarm_msgs/srv/SetQRMap_Response";
}

template<>
struct has_fixed_size<swarm_msgs::srv::SetQRMap_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<swarm_msgs::srv::SetQRMap_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<swarm_msgs::srv::SetQRMap_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<swarm_msgs::srv::SetQRMap>()
{
  return "swarm_msgs::srv::SetQRMap";
}

template<>
inline const char * name<swarm_msgs::srv::SetQRMap>()
{
  return "swarm_msgs/srv/SetQRMap";
}

template<>
struct has_fixed_size<swarm_msgs::srv::SetQRMap>
  : std::integral_constant<
    bool,
    has_fixed_size<swarm_msgs::srv::SetQRMap_Request>::value &&
    has_fixed_size<swarm_msgs::srv::SetQRMap_Response>::value
  >
{
};

template<>
struct has_bounded_size<swarm_msgs::srv::SetQRMap>
  : std::integral_constant<
    bool,
    has_bounded_size<swarm_msgs::srv::SetQRMap_Request>::value &&
    has_bounded_size<swarm_msgs::srv::SetQRMap_Response>::value
  >
{
};

template<>
struct is_service<swarm_msgs::srv::SetQRMap>
  : std::true_type
{
};

template<>
struct is_service_request<swarm_msgs::srv::SetQRMap_Request>
  : std::true_type
{
};

template<>
struct is_service_response<swarm_msgs::srv::SetQRMap_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__TRAITS_HPP_
