import rclpy
from rclpy.node import Node

from autocar_interface.msg import Battery
from autocar_interface.msg import Imu

TOPIC_IMU_ACCEL = "autocar/imu/accel"
TOPIC_IMU_GYRO = "autocar/imu/gyro"

TOPIC_BATTERY = "autocar/battery"

class AutocarTestSubscription(Node):
    def __init__(self):
        super().__init__("AutocarTestSubscription")
        self.accel = self.create_subscription(Imu, TOPIC_IMU_ACCEL, self.accel_callback, 10)
        self.gyro = self.create_subscription(Imu, TOPIC_IMU_GYRO, self.gyro_callback, 10)
        self.battery = self.create_subscription(Battery, TOPIC_BATTERY, self.battery_callback, 10)

    def accel_callback(self, msg):
        self.get_logger().info(f"{msg.x=}, {msg.y=}, {msg.z=}")

    def gyro_callback(self, msg):
        self.get_logger().info(f"{msg.x=}, {msg.y=}, {msg.z=}")

    def battery_callback(self, msg):
        self.get_logger().info(f"{msg.volt=}, {msg.ntc=}")


def main():
    rclpy.init()
    
    node = AutocarTestSubscription()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()