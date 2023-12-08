import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from threading import Thread

CHATT_TOPIC = "ex/chatt"

class Chatt(Node):
    def __init__(self):
        super().__init__("Chatt")

        self.publisher = self.create_publisher(String, CHATT_TOPIC, 10)
        self.subscriber = self.create_subscription(String, CHATT_TOPIC, self.subscription_callback, 10)

        Thread(target=self.thread_callback).start()

    def thread_callback(self):
        self.msg = String()

        while True:
            self.msg.data = input("msg: ")
            self.publisher.publish(self.msg)

    def subscription_callback(self, msg):
        self.get_logger().info(f"{msg.data}")


def main():
    rclpy.init()
    
    node = Chatt()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
