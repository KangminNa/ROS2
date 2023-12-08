import rclpy
from rclpy.node import Node

from rclpy.action import ActionServer
from autocar_interface.action import UltraSonic

from pop import Pilot

import signal
import sys

ACTION = "autocar/action/parking"
LED_PARAM = "autocar/param/led_state"

class AutocarParkingServer(Node):
    def __init__(self):
        super().__init__("AutocarParkingServer")
        
        self.car = Pilot.AutoCar()
        self.declare_parameter(LED_PARAM, 0)

        self.server = ActionServer(self, UltraSonic, ACTION, self.parking_callback)

        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        led_state = self.get_parameter(LED_PARAM).get_parameter_value().integer_value
        
        if led_state == 0:
            self.car.setLamp(0, 0)
        elif led_state == 1:
            self.car.setLamp(1, 0)
        elif led_state == 2:
            self.car.setLamp(0, 1)
        elif led_state == 3:
            self.car.setLamp(1, 1)

        self.get_logger().info(f"{led_state = }")

    def parking_callback(self, goal_handle):
        goal = goal_handle.request.estimated_distance
        feedback = UltraSonic.Feedback()
        result = UltraSonic.Result()

        self.get_logger().info(f"{goal = }")

        while True:
            front, rear = self.car.getUltrasonic()
            if (rear[0] <= goal or rear[1] <= goal):
                break
            else:
                feedback.front = [front[0], front[1], front[2]]
                feedback.rear = [rear[0], rear[1]]

                goal_handle.publish_feedback(feedback)

        goal_handle.succeed()

        result.distance = rear[1] if rear[0] > rear[1] else rear[0]
        return result


def sigterm_handler(signum, frame):
    sys.exit(0)

def main():
    rclpy.init()
    
    node = AutocarParkingServer()

    signal.signal(signal.SIGINT, sigterm_handler)    

    rclpy.spin(node)

if __name__ == '__main__':
    main()
