#******************************************************
# PWM DRIVER
# DESC: Communicates with the Arduino-based PWM module.
# Author: Jonathan L Clark
# Date: 3/7/2020
#******************************************************
import serial
import time
from threading import Thread

right_motor_min = 50

class PWMDriver:
    def __init__(self):
        self.main_throttle = 0.0
        self.turn_vector = 0.0
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
        time.sleep(3)

        self.heart_thread = Thread(target = self.heart_beat)
        self.heart_thread.daemon = True
        self.heart_thread.start()

 
    # Handles communication with the main motor
    def heart_beat(self):
        while (True):
            self.ser.write(bytearray([0x54, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]))
            time.sleep(0.1)

if __name__ == "__main__":
    ctrl = PWMDriver()
    while (True):
        time.sleep(1)