from pop import Pilot
import time

def main():
    car = Pilot.AutoCar()

    car.setLamp(1, 1)
    time.sleep(2)
    car.setLamp(1, 0)
    time.sleep(2)
    car.setLamp(0, 0)    
    time.sleep(2)
    for _ in range(10):
        u = car.getUltrasonic()
        print(u[0], u[1])
        time.sleep(0.1)

if __name__ == "__main__":
    main()
