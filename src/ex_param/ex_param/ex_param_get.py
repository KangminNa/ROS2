import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import GetParameters

SERVER = "ParamNode"
RAND_PARAM = "rand_seed"

class ParamGetNode(Node):
    def __init__(self):
        super().__init__("ParamGetNode")
        
        self.client = self.create_client(GetParameters, '/'+SERVER+'/' + "get_parameters")
        
        while not self.client.wait_for_service(1.0):
            self.get_logger().info('service not available, waiting again...')

        self.request = GetParameters.Request()
        self.request.names = [RAND_PARAM]

    def send_request(self):
        self.future = self.client.call_async(self.request)

def main(args=None): 
    rclpy.init(args=args)

    node = ParamGetNode()
    node.send_request()

    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                response = node.future.result()
                node.get_logger().info(f"{response.values[0].double_value}")
            except Exception as e:
                node.get_logger().info(f"Service call failed {e,}")
            break

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
