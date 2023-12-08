import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts

SERVICE = "SumService"

class SumServer(Node):
    def __init__(self):
        super().__init__("SumServer")

        self.service = self.create_service(AddTwoInts, SERVICE, self.sum_callback)

    def sum_callback(self, request, response):
        response.sum = request.a + request.b

        self.get_logger().info(f"{request.a} + {request.b} = {response.sum}")

        return response


def main():
    rclpy.init()
    
    node = SumServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()    

if __name__ == '__main__':
    main()
