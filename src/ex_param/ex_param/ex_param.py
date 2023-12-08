import rclpy
from rclpy.node import Node

import numpy as np

SERVER = "ParamNode"
RAND_PARAM = "rand_seed"

class ParamNode(Node):
    def __init__(self):
        super().__init__(SERVER)

        self.timer = self.create_timer(1, self.timer_callback)
        self.declare_parameter(RAND_PARAM, 1.4)

    def timer_callback(self):
        seed = self.get_parameter(RAND_PARAM).get_parameter_value().double_value
        np.random.seed(int(seed))

        r = [item for item in np.random.rand(10)]
        self.get_logger().info(f"{r}")

def main():
    rclpy.init()

    node = ParamNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()