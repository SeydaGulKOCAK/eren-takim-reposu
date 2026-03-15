#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool, SetMode

class TakeoffNode(Node):
    def __init__(self):
        super().__init__('takeoff_node')

        # Publisher: local position setpoint
        self.pub = self.create_publisher(
            PoseStamped,
            '/mavros/setpoint_position/local',
            10
        )

        # Services
        self.arm_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.mode_client = self.create_client(SetMode, '/mavros/set_mode')

        # 20 Hz timer
        self.timer = self.create_timer(0.05, self.timer_cb)

        self.setpoint = PoseStamped()
        self.setpoint.pose.position.x = 0.0
        self.setpoint.pose.position.y = 0.0
        self.setpoint.pose.position.z = 5.0  # hedef yükseklik

        self.sent_mode = False
        self.sent_arm = False

    def timer_cb(self):
        # sürekli setpoint yayınla (ÇOK KRİTİK)
        self.setpoint.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(self.setpoint)

        # GUIDED moda geç
        if not self.sent_mode and self.mode_client.wait_for_service(timeout_sec=0.1):
            req = SetMode.Request()
            req.custom_mode = 'GUIDED'
            self.mode_client.call_async(req)
            self.get_logger().info('GUIDED mode sent')
            self.sent_mode = True
            return

        # ARM et
        if self.sent_mode and not self.sent_arm and self.arm_client.wait_for_service(timeout_sec=0.1):
            req = CommandBool.Request()
            req.value = True
            self.arm_client.call_async(req)
            self.get_logger().info('ARM sent')
            self.sent_arm = True

def main():
    rclpy.init()
    node = TakeoffNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

