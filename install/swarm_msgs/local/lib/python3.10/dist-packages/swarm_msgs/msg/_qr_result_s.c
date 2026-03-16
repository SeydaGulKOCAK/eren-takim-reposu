// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from swarm_msgs:msg/QRResult.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "swarm_msgs/msg/detail/qr_result__struct.h"
#include "swarm_msgs/msg/detail/qr_result__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__point__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__point__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__point__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__point__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool swarm_msgs__msg__qr_result__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[35];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("swarm_msgs.msg._qr_result.QRResult", full_classname_dest, 34) == 0);
  }
  swarm_msgs__msg__QRResult * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // team_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "team_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->team_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // qr_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "qr_id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->qr_id = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // formation_active
    PyObject * field = PyObject_GetAttrString(_pymsg, "formation_active");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->formation_active = (Py_True == field);
    Py_DECREF(field);
  }
  {  // formation_type
    PyObject * field = PyObject_GetAttrString(_pymsg, "formation_type");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->formation_type, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // drone_spacing
    PyObject * field = PyObject_GetAttrString(_pymsg, "drone_spacing");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->drone_spacing = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // altitude_active
    PyObject * field = PyObject_GetAttrString(_pymsg, "altitude_active");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->altitude_active = (Py_True == field);
    Py_DECREF(field);
  }
  {  // altitude
    PyObject * field = PyObject_GetAttrString(_pymsg, "altitude");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->altitude = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // maneuver_active
    PyObject * field = PyObject_GetAttrString(_pymsg, "maneuver_active");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->maneuver_active = (Py_True == field);
    Py_DECREF(field);
  }
  {  // pitch_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "pitch_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->pitch_deg = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // roll_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "roll_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->roll_deg = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // detach_active
    PyObject * field = PyObject_GetAttrString(_pymsg, "detach_active");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->detach_active = (Py_True == field);
    Py_DECREF(field);
  }
  {  // detach_drone_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "detach_drone_id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->detach_drone_id = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // zone_color
    PyObject * field = PyObject_GetAttrString(_pymsg, "zone_color");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->zone_color, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // next_qr_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "next_qr_id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->next_qr_id = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // qr_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "qr_position");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__point__convert_from_py(field, &ros_message->qr_position)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // next_qr_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "next_qr_position");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__point__convert_from_py(field, &ros_message->next_qr_position)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // wait_seconds
    PyObject * field = PyObject_GetAttrString(_pymsg, "wait_seconds");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->wait_seconds = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * swarm_msgs__msg__qr_result__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of QRResult */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("swarm_msgs.msg._qr_result");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "QRResult");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  swarm_msgs__msg__QRResult * ros_message = (swarm_msgs__msg__QRResult *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // team_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->team_id.data,
      strlen(ros_message->team_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "team_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // qr_id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->qr_id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "qr_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // formation_active
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->formation_active ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "formation_active", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // formation_type
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->formation_type.data,
      strlen(ros_message->formation_type.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "formation_type", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // drone_spacing
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->drone_spacing);
    {
      int rc = PyObject_SetAttrString(_pymessage, "drone_spacing", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // altitude_active
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->altitude_active ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "altitude_active", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // altitude
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->altitude);
    {
      int rc = PyObject_SetAttrString(_pymessage, "altitude", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // maneuver_active
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->maneuver_active ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "maneuver_active", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pitch_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->pitch_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pitch_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // roll_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->roll_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "roll_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // detach_active
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->detach_active ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "detach_active", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // detach_drone_id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->detach_drone_id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "detach_drone_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // zone_color
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->zone_color.data,
      strlen(ros_message->zone_color.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "zone_color", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // next_qr_id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->next_qr_id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "next_qr_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // qr_position
    PyObject * field = NULL;
    field = geometry_msgs__msg__point__convert_to_py(&ros_message->qr_position);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "qr_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // next_qr_position
    PyObject * field = NULL;
    field = geometry_msgs__msg__point__convert_to_py(&ros_message->next_qr_position);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "next_qr_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // wait_seconds
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->wait_seconds);
    {
      int rc = PyObject_SetAttrString(_pymessage, "wait_seconds", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
