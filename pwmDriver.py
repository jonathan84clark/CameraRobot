#******************************************************
# PWM DRIVER
# DESC: Communicates with the Arduino-based PWM module.
# Author: Jonathan L Clark
# Date: 3/7/2020
#******************************************************
import serial
import time

index = 0

ser = serial.Serial(port='COM6', baudrate=9600)
time.sleep(3)
ser.write(bytearray([0x54, 2, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]))
#time.sleep(1)
#ser.write(bytearray([0x54, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]))
#ser.write(bytearray([0x54, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]))

#while index < 30:
#    print("Call")
#    time.sleep(0.5)
