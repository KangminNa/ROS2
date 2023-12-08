import rclpy
from rclpy.node import Node

from autocar_interface.msg import Imu

from pop import Pilot

TOPIC_IMU_ACCEL = "autocar/imu/accel"
TOPIC_IMU_GYRO = "autocar/imu/gyro"

class AutoCarImuPublisher(Node):
    def __init__(self):
        super().__init__("AutoCarImuPublisher")
        
        self.car = Pilot.AutoCar()
        self.car.setSensorStatus(accel=1, gyro=1, quat=1, battery=1)

        self.accel = self.create_publisher(Imu, TOPIC_IMU_ACCEL, 10)
        self.gyro = self.create_publisher(Imu, TOPIC_IMU_GYRO, 10)

        self.accel_msg = Imu()
        self.gyro_msg = Imu()

        self.timer_period = 0.01
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        self.accel_msg.x, self.accel_msg.y, self.accel_msg.z = self.car.getAccel()
        self.gyro_msg.x, self.gyro_msg.x, self.gyro_msg.z = self.car.getGyro()

        self.accel.publish(self.accel_msg)
        self.gyro.publish(self.gyro_msg)

        self.get_logger().info(f"{self.accel_msg.x=}, {self.accel_msg.y=}, {self.accel_msg.z=}")
        self.get_logger().info(f"{self.gyro_msg.x=}, {self.gyro_msg.y=}, {self.gyro_msg.z=}")

def main():
    rclpy.init()
    
    node = AutoCarImuPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
