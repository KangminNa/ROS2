import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts

import random
import time

SERVICE = "SumService"

class SumClient(Node):
    def __init__(self):
        super().__init__("SumClient")

        self.client = self.create_client(AddTwoInts, SERVICE)

        while not self.client.wait_for_service(0.5):
            self.get_logger().info("Service not available...")
        
    def send_request(self):
        request = AddTwoInts.Request()

        request.a = random.randint(1, 10000)
        request.b = random.randint(1, 10000)
        future = self.client.call_async(request)

        return (future, request)


def main():
    rclpy.init()
    
    node = SumClient()
    future, request = node.send_request()
    trigger = True

    while rclpy.ok():    
        if trigger:
            rclpy.spin_once(node)
            if future.done():
                response = future.result()
                node.get_logger().info(f"{request.a} + {request.a} = {response.sum}")
                trigger = False
        else:
            time.sleep(0.1)
            future, request = node.send_request()
            trigger = True

    node.destroy_node()
    rclpy.shutdown()    

if __name__ == '__main__':
    main()
