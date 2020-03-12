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
        time.sleep(5)

        #self.heart_thread = Thread(target = self.heart_beat)
        #self.heart_thread.daemon = True
        #self.heart_thread.start()

 
    # Handles communication with the main motor
    def set_throttle(self, set_forward, set_turn):
        left_turn_vector = 0.0
        right_turn_vector = 0.0
        if set_turn < 0.0:
            left_turn_vector = abs(set_turn)
            if set_forward < 0.0:
                left_turn_vector *= -1.0
            elif set_turn > 0.0:
                right_turn_vector = set_turn
                if set_forward < 0.0:
                    right_turn_vector *= -1.0

        left_throttle = 0x00 | int((set_forward * 255.0) - (left_turn_vector * 255.0))
        right_throttle = 0x00 | int((set_forward * 255.0) - (right_turn_vector * 255.0))
        right_forward = 0
        left_forward = 0
        right_reverse = 0
        left_reverse = 0
        if right_throttle > 0.0:
            right_forward = right_throttle
        elif right_throttle < 0.0:
            right_reverse = abs(right_throttle)

        if left_throttle > 0.0:
            left_forward = left_throttle
        elif left_throttle < 0.0:
            left_reverse = abs(left_throttle)
        #self.ser.flush()
        #self.ser.write(bytearray([0x54, 2, right_forward, 0, 0, 0, 0, 2, right_reverse, 2, left_forward, 2, left_reverse, 0, 0, 10]))
        if right_forward > 0:
            self.ser.write(bytearray([0x01, right_forward, 0x00]))
        elif right_reverse > 0:
            self.ser.write(bytearray([0x08, right_reverse, 0x00]))
        else:
            self.ser.write(bytearray([0x01, 0, 0x00]))
            self.ser.write(bytearray([0x08, 0, 0x00]))
        #time.sleep(0.1)
        if left_forward > 0:
            self.ser.write(bytearray([0x10, left_forward, 0x00]))
        elif left_reverse > 0:
            self.ser.write(bytearray([0x20, left_reverse, 0x00]))
        else:
            self.ser.write(bytearray([0x10, 0, 0x00]))
            self.ser.write(bytearray([0x20, 0, 0x00]))
        #time.sleep(0.5)

if __name__ == "__main__":
    ctrl = PWMDriver()
    ctrl.set_throttle(0.0, 0.0)
    #while (True):
        #time.sleep(1)