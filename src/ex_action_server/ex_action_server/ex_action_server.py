import rclpy
from rclpy.node import Node

from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci

import time
import signal
import sys

ACTION = "Fibonacci"

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__("FibonacciActionServer")

        self.server = ActionServer(self, Fibonacci, ACTION, self.execute_callback)

    def execute_callback(self, goal_handle):
        goal = goal_handle.request.order
        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        self.get_logger().info(f"{goal = }")

        feedback.partial_sequence = [0, 1]

        for i in range(1, goal):
            next = feedback.partial_sequence[i] + feedback.partial_sequence[i-1]
            feedback.partial_sequence.append(next)
            
            self.get_logger().info(f"{[item for item in feedback.partial_sequence]}")

            goal_handle.publish_feedback(feedback)
            time.sleep(0.5)

        goal_handle.succeed()

        result.sequence = (goal, feedback.partial_sequence[-1])
        return result


def sigterm_handler(signum, frame):
    sys.exit(0)

def main():
    rclpy.init()
    
    node = FibonacciActionServer()

    signal.signal(signal.SIGINT, sigterm_handler)    

    rclpy.spin(node)

if __name__ == '__main__':
    main()
