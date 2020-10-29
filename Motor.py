###################################################################
# MOTOR
# DESC: The motor class handles controlling a single motor, by applying
# PWM throttle values to it.
# Author: Jonathan L Clark
# Date: 10/28/2020
###################################################################
import RPi.GPIO as GPIO

# Setup the GPIO pins
GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

class Motor:
    def __init__(self, in_a, in_b, frequency):
        GPIO.setup(in_a, GPIO.OUT) # Motor A Pin
        GPIO.setup(in_b, GPIO.OUT) # Motor B Pin

        self.motor_a = GPIO.PWM(in_a, frequency)
        self.motor_b = GPIO.PWM(in_b, frequency)

        self.motor_a.start(0)
        self.motor_b.start(0)

    # Takes a throttle value between -1.0 <= 0 <= 1.0
    def set_throttle(self, throttle):
        if throttle >= 0.0:
            self.motor_a.ChangeDutyCycle(throttle * 100.0)
            self.motor_b.ChangeDutyCycle(0)
        else:
            self.motor_a.ChangeDutyCycle(0)
            self.motor_b.ChangeDutyCycle(abs(throttle) * 100.0)

    # Destructor handles the class being destroyed
    def __del__(self):
        self.motor_a.ChangeDutyCycle(0)
        self.motor_b.ChangeDutyCycle(0)
        

if __name__ == "__main__":
    pass
