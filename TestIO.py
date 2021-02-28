###################################################################
# GPS DRIVER
# DESC: The GPS driver interacts with a ubox GPS device. It is intended to
# provide simple read-only values for GPS data
# Author: Jonathan L Clark
# Date: 10/30/2020
###################################################################
import serial
import time
import RPi.GPIO as GPIO

RIGHT_HEADLIGHT = 8
LEFT_HEADLIGHT = 25

LEFT_A1 = 17
LEFT_B1 = 18

LEFT_A2 = 19
LEFT_B2 = 27

RIGHT_A1 = 12
RIGHT_B1 = 13 

RIGHT_A2 = 6
RIGHT_B2 = 26

GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(RIGHT_HEADLIGHT, GPIO.OUT) # Motor A Pin
GPIO.setup(LEFT_HEADLIGHT, GPIO.OUT) # Motor A Pin
#GPIO.setup(in_b, GPIO.OUT) # Motor B Pin

GPIO.output(RIGHT_HEADLIGHT, GPIO.LOW)
GPIO.output(LEFT_HEADLIGHT, GPIO.LOW)



