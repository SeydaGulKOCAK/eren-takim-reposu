# generated from rosidl_generator_py/resource/_idl.py.em
# with input from swarm_msgs:msg/QRResult.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_QRResult(type):
    """Metaclass of message 'QRResult'."""

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
                'swarm_msgs.msg.QRResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__qr_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__qr_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__qr_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__qr_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__qr_result

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

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


class QRResult(metaclass=Metaclass_QRResult):
    """Message class 'QRResult'."""

    __slots__ = [
        '_header',
        '_team_id',
        '_qr_id',
        '_formation_active',
        '_formation_type',
        '_drone_spacing',
        '_altitude_active',
        '_altitude',
        '_maneuver_active',
        '_pitch_deg',
        '_roll_deg',
        '_detach_active',
        '_detach_drone_id',
        '_zone_color',
        '_next_qr_id',
        '_qr_position',
        '_next_qr_position',
        '_wait_seconds',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'team_id': 'string',
        'qr_id': 'uint32',
        'formation_active': 'boolean',
        'formation_type': 'string',
        'drone_spacing': 'float',
        'altitude_active': 'boolean',
        'altitude': 'float',
        'maneuver_active': 'boolean',
        'pitch_deg': 'float',
        'roll_deg': 'float',
        'detach_active': 'boolean',
        'detach_drone_id': 'uint8',
        'zone_color': 'string',
        'next_qr_id': 'uint32',
        'qr_position': 'geometry_msgs/Point',
        'next_qr_position': 'geometry_msgs/Point',
        'wait_seconds': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.team_id = kwargs.get('team_id', str())
        self.qr_id = kwargs.get('qr_id', int())
        self.formation_active = kwargs.get('formation_active', bool())
        self.formation_type = kwargs.get('formation_type', str())
        self.drone_spacing = kwargs.get('drone_spacing', float())
        self.altitude_active = kwargs.get('altitude_active', bool())
        self.altitude = kwargs.get('altitude', float())
        self.maneuver_active = kwargs.get('maneuver_active', bool())
        self.pitch_deg = kwargs.get('pitch_deg', float())
        self.roll_deg = kwargs.get('roll_deg', float())
        self.detach_active = kwargs.get('detach_active', bool())
        self.detach_drone_id = kwargs.get('detach_drone_id', int())
        self.zone_color = kwargs.get('zone_color', str())
        self.next_qr_id = kwargs.get('next_qr_id', int())
        from geometry_msgs.msg import Point
        self.qr_position = kwargs.get('qr_position', Point())
        from geometry_msgs.msg import Point
        self.next_qr_position = kwargs.get('next_qr_position', Point())
        self.wait_seconds = kwargs.get('wait_seconds', float())

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
        if self.team_id != other.team_id:
            return False
        if self.qr_id != other.qr_id:
            return False
        if self.formation_active != other.formation_active:
            return False
        if self.formation_type != other.formation_type:
            return False
        if self.drone_spacing != other.drone_spacing:
            return False
        if self.altitude_active != other.altitude_active:
            return False
        if self.altitude != other.altitude:
            return False
        if self.maneuver_active != other.maneuver_active:
            return False
        if self.pitch_deg != other.pitch_deg:
            return False
        if self.roll_deg != other.roll_deg:
            return False
        if self.detach_active != other.detach_active:
            return False
        if self.detach_drone_id != other.detach_drone_id:
            return False
        if self.zone_color != other.zone_color:
            return False
        if self.next_qr_id != other.next_qr_id:
            return False
        if self.qr_position != other.qr_position:
            return False
        if self.next_qr_position != other.next_qr_position:
            return False
        if self.wait_seconds != other.wait_seconds:
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
    def team_id(self):
        """Message field 'team_id'."""
        return self._team_id

    @team_id.setter
    def team_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'team_id' field must be of type 'str'"
        self._team_id = value

    @builtins.property
    def qr_id(self):
        """Message field 'qr_id'."""
        return self._qr_id

    @qr_id.setter
    def qr_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'qr_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'qr_id' field must be an unsigned integer in [0, 4294967295]"
        self._qr_id = value

    @builtins.property
    def formation_active(self):
        """Message field 'formation_active'."""
        return self._formation_active

    @formation_active.setter
    def formation_active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'formation_active' field must be of type 'bool'"
        self._formation_active = value

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
    def altitude_active(self):
        """Message field 'altitude_active'."""
        return self._altitude_active

    @altitude_active.setter
    def altitude_active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'altitude_active' field must be of type 'bool'"
        self._altitude_active = value

    @builtins.property
    def altitude(self):
        """Message field 'altitude'."""
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'altitude' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'altitude' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._altitude = value

    @builtins.property
    def maneuver_active(self):
        """Message field 'maneuver_active'."""
        return self._maneuver_active

    @maneuver_active.setter
    def maneuver_active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'maneuver_active' field must be of type 'bool'"
        self._maneuver_active = value

    @builtins.property
    def pitch_deg(self):
        """Message field 'pitch_deg'."""
        return self._pitch_deg

    @pitch_deg.setter
    def pitch_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'pitch_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'pitch_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._pitch_deg = value

    @builtins.property
    def roll_deg(self):
        """Message field 'roll_deg'."""
        return self._roll_deg

    @roll_deg.setter
    def roll_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'roll_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'roll_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._roll_deg = value

    @builtins.property
    def detach_active(self):
        """Message field 'detach_active'."""
        return self._detach_active

    @detach_active.setter
    def detach_active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'detach_active' field must be of type 'bool'"
        self._detach_active = value

    @builtins.property
    def detach_drone_id(self):
        """Message field 'detach_drone_id'."""
        return self._detach_drone_id

    @detach_drone_id.setter
    def detach_drone_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'detach_drone_id' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'detach_drone_id' field must be an unsigned integer in [0, 255]"
        self._detach_drone_id = value

    @builtins.property
    def zone_color(self):
        """Message field 'zone_color'."""
        return self._zone_color

    @zone_color.setter
    def zone_color(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'zone_color' field must be of type 'str'"
        self._zone_color = value

    @builtins.property
    def next_qr_id(self):
        """Message field 'next_qr_id'."""
        return self._next_qr_id

    @next_qr_id.setter
    def next_qr_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'next_qr_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'next_qr_id' field must be an unsigned integer in [0, 4294967295]"
        self._next_qr_id = value

    @builtins.property
    def qr_position(self):
        """Message field 'qr_position'."""
        return self._qr_position

    @qr_position.setter
    def qr_position(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'qr_position' field must be a sub message of type 'Point'"
        self._qr_position = value

    @builtins.property
    def next_qr_position(self):
        """Message field 'next_qr_position'."""
        return self._next_qr_position

    @next_qr_position.setter
    def next_qr_position(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'next_qr_position' field must be a sub message of type 'Point'"
        self._next_qr_position = value

    @builtins.property
    def wait_seconds(self):
        """Message field 'wait_seconds'."""
        return self._wait_seconds

    @wait_seconds.setter
    def wait_seconds(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'wait_seconds' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'wait_seconds' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._wait_seconds = value
