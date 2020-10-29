###################################################################
# DRIVE
# DESC: The drive system controls the hardware drive controls for the 
# main system.
# Author: Jonathan L Clark
# Date: 10/28/2020
###################################################################
import RPi.GPIO as GPIO
from Motor import Motor

class DriveSystem:
    def __init__(self, main_a, main_b, steer_a, steer_b, in_headlight_pin, frequency):
        self.steering = Motor(steer_a, steer_b, frequency)
        self.main_motor = Motor(main_a, main_b, frequency)
        self.headlight_pin = in_headlight_pin
        GPIO.setup(self.headlight_pin, GPIO.OUT)
        GPIO.output(self.headlight_pin, GPIO.LOW)

    # Takes the steering and throttle inputs and applies them to the drive
    def manual_control(self, throttle, steering):
        self.steering.set_throttle(steering)
        self.main_motor.set_throttle(throttle)

    # Sets or clears the headlights
    def set_headlights(self, state):
        if state:
            GPIO.output(self.headlight_pin, GPIO.HIGH)
        else:
            GPIO.output(self.headlight_pin, GPIO.LOW)

    # Destructor handles the class being destroyed
    def __del__(self):
        pass

if __name__ == "__main__":
    pass
