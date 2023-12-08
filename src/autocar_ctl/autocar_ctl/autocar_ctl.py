import rclpy
from rclpy.node import Node

from autocar_interface.srv import Drive

SERVICE = "autocar/srv/drive"

class AutocarController(Node):
    def __init__(self):
        super().__init__("AutocarController")

        self.client = self.create_client(Drive, SERVICE)

        while not self.client.wait_for_service(0.5):
            self.get_logger().info("Service not available...")
        
    def send_request(self, speed, direction, steering):
        request = Drive.Request()

        request.speed = speed
        request.direction = direction
        request.steering = steering
        future = self.client.call_async(request)

        return (future, request)


def user_input():
    speed = int(input("enter of speed (10 ~ 100): "))
    direction = bool(int(input("enter of direction (0 or 1): ")))
    steering = float(input("enter of steering (-1.0 ~ 1.0): "))

    return speed, direction, steering

def main():
    rclpy.init()
    
    node = AutocarController()

    speed, direction, steering = user_input()

    future, request = node.send_request(speed, direction, steering)
    trigger = True

    while rclpy.ok():    
        if trigger:
            rclpy.spin_once(node)
            if future.done():
                response = future.result()
                node.get_logger().info(f"{request.speed}, {request.direction}, {request.steering}")
                trigger = False
        else:
            speed, direction, steering = user_input()

            future, request = node.send_request(speed, direction, steering)
            trigger = True

    node.destroy_node()
    rclpy.shutdown()   

if __name__ == '__main__':
    main()
