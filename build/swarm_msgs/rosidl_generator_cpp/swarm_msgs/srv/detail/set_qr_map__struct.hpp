// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from swarm_msgs:srv/SetQRMap.idl
// generated code does not contain a copyright notice

#ifndef SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_HPP_
#define SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'qr_positions'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__swarm_msgs__srv__SetQRMap_Request __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__srv__SetQRMap_Request __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetQRMap_Request_
{
  using Type = SetQRMap_Request_<ContainerAllocator>;

  explicit SetQRMap_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit SetQRMap_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _qr_positions_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _qr_positions_type qr_positions;
  using _qr_ids_type =
    std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>>;
  _qr_ids_type qr_ids;
  using _next_qr_ids_type =
    std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>>;
  _next_qr_ids_type next_qr_ids;

  // setters for named parameter idiom
  Type & set__qr_positions(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->qr_positions = _arg;
    return *this;
  }
  Type & set__qr_ids(
    const std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>> & _arg)
  {
    this->qr_ids = _arg;
    return *this;
  }
  Type & set__next_qr_ids(
    const std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>> & _arg)
  {
    this->next_qr_ids = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__srv__SetQRMap_Request
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__srv__SetQRMap_Request
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetQRMap_Request_ & other) const
  {
    if (this->qr_positions != other.qr_positions) {
      return false;
    }
    if (this->qr_ids != other.qr_ids) {
      return false;
    }
    if (this->next_qr_ids != other.next_qr_ids) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetQRMap_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetQRMap_Request_

// alias to use template instance with default allocator
using SetQRMap_Request =
  swarm_msgs::srv::SetQRMap_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace swarm_msgs


#ifndef _WIN32
# define DEPRECATED__swarm_msgs__srv__SetQRMap_Response __attribute__((deprecated))
#else
# define DEPRECATED__swarm_msgs__srv__SetQRMap_Response __declspec(deprecated)
#endif

namespace swarm_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetQRMap_Response_
{
  using Type = SetQRMap_Response_<ContainerAllocator>;

  explicit SetQRMap_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit SetQRMap_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__swarm_msgs__srv__SetQRMap_Response
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__swarm_msgs__srv__SetQRMap_Response
    std::shared_ptr<swarm_msgs::srv::SetQRMap_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetQRMap_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetQRMap_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetQRMap_Response_

// alias to use template instance with default allocator
using SetQRMap_Response =
  swarm_msgs::srv::SetQRMap_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace swarm_msgs

namespace swarm_msgs
{

namespace srv
{

struct SetQRMap
{
  using Request = swarm_msgs::srv::SetQRMap_Request;
  using Response = swarm_msgs::srv::SetQRMap_Response;
};

}  // namespace srv

}  // namespace swarm_msgs

#endif  // SWARM_MSGS__SRV__DETAIL__SET_QR_MAP__STRUCT_HPP_
