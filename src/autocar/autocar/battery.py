import rclpy
from rclpy.node import Node

from autocar_interface.msg import Battery

from pop import Pilot

TOPIC_BATTERY = "autocar/battery"

class AutoCarBatteryPublisher(Node):
    def __init__(self):
        super().__init__("AutoCarImuPublisher")
        
        self.car = Pilot.AutoCar()
        self.car.setSensorStatus(accel=1, gyro=1, quat=1, battery=1)

        self.battery = self.create_publisher(Battery, TOPIC_BATTERY, 10)

        self.msg = Battery()

        self.timer_period = 0.01
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        self.msg.volt, self.msg.ntc = self.car.getBattery()

        self.battery.publish(self.msg)

        self.get_logger().info(f"{self.msg.volt=}, {self.msg.ntc=}")

def main():
    rclpy.init()
    
    node = AutoCarBatteryPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
