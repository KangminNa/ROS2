from pop import Pilot
import time

def main():
    car = Pilot.AutoCar()

    car.setSpeed(30)
    car.forward()
    time.sleep(3)
    car.steering = -1.0
    time.sleep(3)
    car.backward()
    time.sleep(3)
    car.forward()
    car.setSpeed(90)
    time.sleep(3)
    car.steering = 1.0
    time.sleep(3)
    car.steering = 0.0
    time.sleep(3)
    car.stop()

if __name__ == "__main__":
    main()