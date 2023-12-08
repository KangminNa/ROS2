from pop import Pilot

def main():
    car = Pilot.AutoCar()
    car.setSensorStatus(accel=1, gyro=1, quat=1, battery=1)

    for _ in range(10):
        accel_msg = car.getAccel()
        gyro_msg = car.getGyro()
        quat_msg = car.getQuat()
        battery_msg = car.getBattery()

        print(accel_msg, gyro_msg, quat_msg, battery_msg)

if __name__ == "__main__":
    main()