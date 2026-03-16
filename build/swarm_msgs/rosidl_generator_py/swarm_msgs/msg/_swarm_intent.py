# generated from rosidl_generator_py/resource/_idl.py.em
# with input from swarm_msgs:msg/SwarmIntent.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SwarmIntent(type):
    """Metaclass of message 'SwarmIntent'."""

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
                'swarm_msgs.msg.SwarmIntent')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__swarm_intent
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__swarm_intent
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__swarm_intent
            cls._TYPE_SUPPORT = module.type_support_msg__msg__swarm_intent
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__swarm_intent

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

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


class SwarmIntent(metaclass=Metaclass_SwarmIntent):
    """Message class 'SwarmIntent'."""

    __slots__ = [
        '_header',
        '_seq',
        '_leader_id',
        '_task_id',
        '_formation_type',
        '_drone_spacing',
        '_target_yaw',
        '_target_pos',
        '_drone_altitude',
        '_detach_drone_id',
        '_zone_color',
        '_maneuver_active',
        '_maneuver_pitch_deg',
        '_maneuver_roll_deg',
        '_active_drone_count',
        '_join_drone_id',
        '_qr_seq',
        '_wait_until',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'seq': 'uint32',
        'leader_id': 'uint8',
        'task_id': 'string',
        'formation_type': 'string',
        'drone_spacing': 'float',
        'target_yaw': 'float',
        'target_pos': 'geometry_msgs/Point',
        'drone_altitude': 'float',
        'detach_drone_id': 'uint8',
        'zone_color': 'string',
        'maneuver_active': 'boolean',
        'maneuver_pitch_deg': 'float',
        'maneuver_roll_deg': 'float',
        'active_drone_count': 'uint8',
        'join_drone_id': 'uint8',
        'qr_seq': 'uint32',
        'wait_until': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.seq = kwargs.get('seq', int())
        self.leader_id = kwargs.get('leader_id', int())
        self.task_id = kwargs.get('task_id', str())
        self.formation_type = kwargs.get('formation_type', str())
        self.drone_spacing = kwargs.get('drone_spacing', float())
        self.target_yaw = kwargs.get('target_yaw', float())
        from geometry_msgs.msg import Point
        self.target_pos = kwargs.get('target_pos', Point())
        self.drone_altitude = kwargs.get('drone_altitude', float())
        self.detach_drone_id = kwargs.get('detach_drone_id', int())
        self.zone_color = kwargs.get('zone_color', str())
        self.maneuver_active = kwargs.get('maneuver_active', bool())
        self.maneuver_pitch_deg = kwargs.get('maneuver_pitch_deg', float())
        self.maneuver_roll_deg = kwargs.get('maneuver_roll_deg', float())
        self.active_drone_count = kwargs.get('active_drone_count', int())
        self.join_drone_id = kwargs.get('join_drone_id', int())
        self.qr_seq = kwargs.get('qr_seq', int())
        from builtin_interfaces.msg import Time
        self.wait_until = kwargs.get('wait_until', Time())

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
        if self.seq != other.seq:
            return False
        if self.leader_id != other.leader_id:
            return False
        if self.task_id != other.task_id:
            return False
        if self.formation_type != other.formation_type:
            return False
        if self.drone_spacing != other.drone_spacing:
            return False
        if self.target_yaw != other.target_yaw:
            return False
        if self.target_pos != other.target_pos:
            return False
        if self.drone_altitude != other.drone_altitude:
            return False
        if self.detach_drone_id != other.detach_drone_id:
            return False
        if self.zone_color != other.zone_color:
            return False
        if self.maneuver_active != other.maneuver_active:
            return False
        if self.maneuver_pitch_deg != other.maneuver_pitch_deg:
            return False
        if self.maneuver_roll_deg != other.maneuver_roll_deg:
            return False
        if self.active_drone_count != other.active_drone_count:
            return False
        if self.join_drone_id != other.join_drone_id:
            return False
        if self.qr_seq != other.qr_seq:
            return False
        if self.wait_until != other.wait_until:
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
    def seq(self):
        """Message field 'seq'."""
        return self._seq

    @seq.setter
    def seq(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'seq' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'seq' field must be an unsigned integer in [0, 4294967295]"
        self._seq = value

    @builtins.property
    def leader_id(self):
        """Message field 'leader_id'."""
        return self._leader_id

    @leader_id.setter
    def leader_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leader_id' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leader_id' field must be an unsigned integer in [0, 255]"
        self._leader_id = value

    @builtins.property
    def task_id(self):
        """Message field 'task_id'."""
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'task_id' field must be of type 'str'"
        self._task_id = value

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
    def target_pos(self):
        """Message field 'target_pos'."""
        return self._target_pos

    @target_pos.setter
    def target_pos(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'target_pos' field must be a sub message of type 'Point'"
        self._target_pos = value

    @builtins.property
    def drone_altitude(self):
        """Message field 'drone_altitude'."""
        return self._drone_altitude

    @drone_altitude.setter
    def drone_altitude(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'drone_altitude' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'drone_altitude' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._drone_altitude = value

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
    def maneuver_pitch_deg(self):
        """Message field 'maneuver_pitch_deg'."""
        return self._maneuver_pitch_deg

    @maneuver_pitch_deg.setter
    def maneuver_pitch_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'maneuver_pitch_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'maneuver_pitch_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._maneuver_pitch_deg = value

    @builtins.property
    def maneuver_roll_deg(self):
        """Message field 'maneuver_roll_deg'."""
        return self._maneuver_roll_deg

    @maneuver_roll_deg.setter
    def maneuver_roll_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'maneuver_roll_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'maneuver_roll_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._maneuver_roll_deg = value

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

    @builtins.property
    def join_drone_id(self):
        """Message field 'join_drone_id'."""
        return self._join_drone_id

    @join_drone_id.setter
    def join_drone_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'join_drone_id' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'join_drone_id' field must be an unsigned integer in [0, 255]"
        self._join_drone_id = value

    @builtins.property
    def qr_seq(self):
        """Message field 'qr_seq'."""
        return self._qr_seq

    @qr_seq.setter
    def qr_seq(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'qr_seq' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'qr_seq' field must be an unsigned integer in [0, 4294967295]"
        self._qr_seq = value

    @builtins.property
    def wait_until(self):
        """Message field 'wait_until'."""
        return self._wait_until

    @wait_until.setter
    def wait_until(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'wait_until' field must be a sub message of type 'Time'"
        self._wait_until = value
