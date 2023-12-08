import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt64

TOPIC = "ex/count"

class MySubscription(Node):
    def __init__(self):
        super().__init__("MySubscription")
        self.subscriber = self.create_subscription(UInt64, TOPIC, self.subscription_callback, 10)

    def subscription_callback(self, msg):
        self.get_logger().info(f"{msg.data}")

def main():
    rclpy.init()
    
    node = MySubscription()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
