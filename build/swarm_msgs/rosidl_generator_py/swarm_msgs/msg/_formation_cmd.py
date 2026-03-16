# generated from rosidl_generator_py/resource/_idl.py.em
# with input from swarm_msgs:msg/FormationCmd.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FormationCmd(type):
    """Metaclass of message 'FormationCmd'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('swarm_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'swarm_msgs.msg.FormationCmd')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__formation_cmd
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__formation_cmd
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__formation_cmd
            cls._TYPE_SUPPORT = module.type_support_msg__msg__formation_cmd
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__formation_cmd

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FormationCmd(metaclass=Metaclass_FormationCmd):
    """Message class 'FormationCmd'."""

    __slots__ = [
        '_header',
        '_formation_type',
        '_drone_spacing',
        '_target_yaw',
        '_active_drone_count',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'formation_type': 'string',
        'drone_spacing': 'float',
        'target_yaw': 'float',
        'active_drone_count': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.formation_type = kwargs.get('formation_type', str())
        self.drone_spacing = kwargs.get('drone_spacing', float())
        self.target_yaw = kwargs.get('target_yaw', float())
        self.active_drone_count = kwargs.get('active_drone_count', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.formation_type != other.formation_type:
            return False
        if self.drone_spacing != other.drone_spacing:
            return False
        if self.target_yaw != other.target_yaw:
            return False
        if self.active_drone_count != other.active_drone_count:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def formation_type(self):
        """Message field 'formation_type'."""
        return self._formation_type

    @formation_type.setter
    def formation_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'formation_type' field must be of type 'str'"
        self._formation_type = value

    @builtins.property
    def drone_spacing(self):
        """Message field 'drone_spacing'."""
        return self._drone_spacing

    @drone_spacing.setter
    def drone_spacing(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'drone_spacing' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'drone_spacing' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._drone_spacing = value

    @builtins.property
    def target_yaw(self):
        """Message field 'target_yaw'."""
        return self._target_yaw

    @target_yaw.setter
    def target_yaw(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'target_yaw' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'target_yaw' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._target_yaw = value

    @builtins.property
    def active_drone_count(self):
        """Message field 'active_drone_count'."""
        return self._active_drone_count

    @active_drone_count.setter
    def active_drone_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'active_drone_count' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'active_drone_count' field must be an unsigned integer in [0, 255]"
        self._active_drone_count = value
