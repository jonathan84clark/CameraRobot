###################################################################
# DRIVE
# DESC: The drive system controls the hardware drive controls for the 
# main system.
# Author: Jonathan L Clark
# Date: 10/28/2020
###################################################################
import RPi.GPIO as GPIO
from Motor import Motor
import time

#GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
FRONT_LEFT_A1 = 17
FRONT_LEFT_B1 = 18

BACK_LEFT_A = 19
BACK_LEFT_B = 27

FRONT_RIGHT_A1 = 12
FRONT_RIGHT_B1 = 13 

BACK_RIGHT_A = 6
BACK_RIGHT_B = 26

RIGHT_HEADLIGHT = 8
LEFT_HEADLIGHT = 25

class DriveSystem:
    def __init__(self, frequency):
        self.front_left = Motor(FRONT_LEFT_A1, FRONT_LEFT_B1, frequency)
        self.front_right = Motor(FRONT_RIGHT_A1, FRONT_RIGHT_B1, frequency)
        self.back_left = Motor(BACK_LEFT_A, BACK_LEFT_B, frequency)
        self.back_right = Motor(BACK_RIGHT_A, BACK_RIGHT_B, frequency)
        
        GPIO.setup(RIGHT_HEADLIGHT, GPIO.OUT) # Motor A Pin
        GPIO.setup(LEFT_HEADLIGHT, GPIO.OUT) # Motor A Pin
        
        self.set_headlights(0)

    # Takes the steering and throttle inputs and applies them to the drive
    def manual_control(self, throttle, steering, slide):
        left_throttle = throttle
        right_throttle = throttle
        
        left_throttle += steering
        right_throttle -= steering 

        # Handle standard throttle configuration
        left_front = left_throttle
        left_rear = left_throttle
        right_front = right_throttle
        right_rear = right_throttle 

        # Handle macanum wheel configuration
        left_front += slide
        right_rear += slide
        right_front -= slide
        left_rear -= slide        
        
        self.front_left.set_throttle(left_front)
        self.front_right.set_throttle(right_front)
        self.back_left.set_throttle(left_rear)
        self.back_right.set_throttle(right_rear)
        

    # Sets or clears the headlights
    def set_headlights(self, state):
        if state:
            GPIO.output(LEFT_HEADLIGHT, GPIO.HIGH)
            GPIO.output(RIGHT_HEADLIGHT, GPIO.HIGH)
        else:
            GPIO.output(LEFT_HEADLIGHT, GPIO.LOW)
            GPIO.output(RIGHT_HEADLIGHT, GPIO.LOW)

    # Destructor handles the class being destroyed
    def __del__(self):
        pass

if __name__ == "__main__":
    drive = DriveSystem(1000)
    
    while (True):
        time.sleep(1)
    pass
