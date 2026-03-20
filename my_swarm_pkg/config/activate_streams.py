#!/usr/bin/env python3
"""25s sonra otomatik çalışır, LOCAL_POSITION_NED aktif eder, kapanır."""
import rclpy
from mavros_msgs.srv import CommandLong


def activate_for_drone(node, i, max_retry=5):
    client = node.create_client(CommandLong, f'/drone{i}/mavros/cmd/command')
    for attempt in range(1, max_retry + 1):
        if not client.wait_for_service(timeout_sec=10.0):
            node.get_logger().error(f'drone{i}: MAVROS servisi yok! (deneme {attempt})')
            continue
        req = CommandLong.Request()
        req.command = 511       # MAV_CMD_SET_MESSAGE_INTERVAL
        req.param1 = 32.0       # LOCAL_POSITION_NED (msg id=32)
        req.param2 = 100000.0   # 100ms = 10 Hz
        future = client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=8.0)
        r = future.result()
        if r is not None:
            node.get_logger().info(f'drone{i}: LOCAL_POSITION_NED aktif (ok={r.success})')
            return True
        else:
            node.get_logger().warn(f'drone{i}: timeout (deneme {attempt}/{max_retry}), tekrar...')
    node.get_logger().error(f'drone{i}: {max_retry} denemeden sonra başarısız!')
    return False


def main():
    rclpy.init()
    node = rclpy.create_node('stream_activator')
    for i in [1, 2, 3]:
        activate_for_drone(node, i)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
