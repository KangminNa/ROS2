import rclpy
from rclpy.node import Node

from autocar_interface.srv import Drive

from pop import Pilot

SERVICE = "autocar/srv/drive"

class AutocarDriveServer(Node):
    def __init__(self):
        super().__init__("AutocarDriveServer")

        self.car = Pilot.AutoCar()

        self.service = self.create_service(Drive, SERVICE, self.drive_callback)

    def drive_callback(self, request, response):
        if request.speed == 0:
            self.car.stop()
        else:
            self.car.setSpeed(request.speed)

            if request.direction == 1:
                self.car.forward()
            else:
                self.car.backward()

            self.car.steering = request.steering

        self.get_logger().info(f"{request.speed=}, {request.direction=}, {request.steering=}")

        response.success = True

        return response


def main():
    rclpy.init()
    
    node = AutocarDriveServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()    

if __name__ == '__main__':
    main()
