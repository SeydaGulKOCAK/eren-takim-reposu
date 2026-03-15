import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class HoverNode(Node):
    def __init__(self):
        super().__init__('hover_node')

        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/mavros/setpoint_position/local',
            10
        )

        self.timer = self.create_timer(0.05, self.publish_setpoint)  # 20 Hz

    def publish_setpoint(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'

        msg.pose.position.x = 0.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = 2.0   # 2 metre hover

        msg.pose.orientation.w = 1.0

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = HoverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
