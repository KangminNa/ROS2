import rclpy, sys
from rclpy.node import Node
from rcl_interfaces.msg import Parameter
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterValue
from rcl_interfaces.srv import SetParameters

import random

SERVER = "ParamNode"
RAND_PARAM = "rand_seed"

class ParamSetNode(Node):
    def __init__(self):
        super().__init__("ParamSetNode")

        self.client = self.create_client(SetParameters,  '/'+SERVER+'/' + "set_parameters")

        while not self.client.wait_for_service(1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.request = SetParameters.Request()
        parameter = ParameterValue(type=ParameterType.PARAMETER_DOUBLE, double_value=random.random()*100)
        self.request.parameters = [Parameter(name=RAND_PARAM, value=parameter)]

    def send_request(self):
        self.future = self.client.call_async(self.request)

def main(args=None):
    rclpy.init(args=args)
    node = ParamSetNode()
    node.send_request()

    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                node.future.result()
            except Exception as e:
                node.get_logger().info(f"Service call failed {e,}")
            break

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
