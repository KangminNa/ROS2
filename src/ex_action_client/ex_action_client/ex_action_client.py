import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci

import random
import signal
import sys

ACTION = "Fibonacci"

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("FibonacciActionClient")
        
        self.stop = False

        self.client = ActionClient(self, Fibonacci, ACTION)

    def send_goal(self, order):
        goal = Fibonacci.Goal()
        goal.order = order

        self.client.wait_for_server()
        self._send_goal_future = self.client.send_goal_async(goal, self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return

        self.get_logger().info("Goal accepted")

        self._ret_future = goal_handle.get_result_async()
        self._ret_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result

        gaol = result.sequence[0]
        last_result = result.sequence[1]
        self.get_logger().info(f"Result: {gaol = }, {last_result = }")

        self.stop = True

    def feedback_callback(self, feedback):
        self.get_logger().info(f"{[item for item in feedback.feedback.partial_sequence]}")


def sigterm_handler(signum, frame):
    sys.exit(0)

def main():   
    rclpy.init()
    
    node = FibonacciActionClient()
    node.send_goal(random.randint(9, 30))

    signal.signal(signal.SIGINT, sigterm_handler)    

    while True:
        if not node.stop:
            rclpy.spin_once(node)
        else:
            node.stop = False
            node.send_goal(random.randint(9, 30))
            
if __name__ == '__main__':
    main()
