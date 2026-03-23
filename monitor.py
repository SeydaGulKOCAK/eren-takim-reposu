#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from geometry_msgs.msg import PoseStamped

best_effort_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=1,
)

class Monitor(Node):
    def __init__(self):
        super().__init__('monitor')
        self.alt = {1: 0.0, 2: 0.0, 3: 0.0}
        for i in [1, 2, 3]:
            self.create_subscription(PoseStamped, f'/drone{i}/mavros/local_position/pose',
                lambda msg, i=i: self.cb(msg, i), best_effort_qos)
        self.create_timer(0.5, self.print_alt)

    def cb(self, msg, i):
        self.alt[i] = msg.pose.position.z

    def print_alt(self):
        print(f"\r  drone1: {self.alt[1]:.2f}m  |  drone2: {self.alt[2]:.2f}m  |  drone3: {self.alt[3]:.2f}m    ", end='', flush=True)

rclpy.init()
rclpy.spin(Monitor())
