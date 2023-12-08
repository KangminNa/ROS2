import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("MyNode")
        self.running = True

        self.get_logger().info("call __init__")

        self.work()

    def work(self):
        time_difference = 0
        old = None
        start = self.get_clock( ).now().seconds_nanoseconds()[0]

        while True:
            end = self.get_clock( ).now().seconds_nanoseconds()[0]
            time_difference = end - start 

            if time_difference != old:
                old = time_difference
                print(f"{time_difference = }")

            if end - start >= 5:
                break

        self.running = False

    def __del__(self):
        self.get_logger().info("call __del__")

def main():
    rclpy.init()
    
    node = MyNode()
    node.get_logger().info("call main")
    
    while node.running and rclpy.ok():
        rclpy.spin_once(node)

    node.destroy_node()
    rclpy.shutdown()    

    node.get_logger().info("-The End-")

if __name__ == '__main__':
    main()
