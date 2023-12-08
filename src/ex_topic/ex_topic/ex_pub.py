import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt64

TOPIC = "ex/count"

class MyPublisher(Node):
    def __init__(self):
        super().__init__("MyPublisher")
        self.publisher = self.create_publisher(UInt64, TOPIC, 10)

        self.count = 0
        self.msg = UInt64()

        self.timer_period = 0.01
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        self.count += 1

        self.msg.data = self.count
        self.publisher.publish(self.msg)

        self.get_logger().info(f"{self.msg.data}")

def main():
    rclpy.init()
    
    node = MyPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
