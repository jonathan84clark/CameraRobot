###################################################################
# UDP ROBOT CONTROL
# DESC: The UDP robot control system controls the robot using UDP
# packets.
# Author: Jonathan L Clark
# Date: 12/3/2019
###################################################################
import socket
import time
from threading import Thread
from time import sleep
import datetime
import RPi.GPIO as GPIO

TRIGGER_R = 27
ECHO_R = 22

TRIGGER_M = 23
ECHO_M = 24

TRIGGER_L = 8
ECHO_L = 7

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(TRIGGER_R,GPIO.OUT)
GPIO.setup(ECHO_R,GPIO.IN)
GPIO.output(TRIGGER_R, False)

GPIO.setup(TRIGGER_M,GPIO.OUT)
GPIO.setup(ECHO_M,GPIO.IN)
GPIO.output(TRIGGER_M, False)

GPIO.setup(TRIGGER_L,GPIO.OUT)
GPIO.setup(ECHO_L,GPIO.IN)
GPIO.output(TRIGGER_L, False)

time.sleep(2)

class UDPRobotControl:
    def __init__(self):
        self.left_falling = False
        self.left_triggered = False
        self.left_pulse_start = 0
        self.left_pulse_end = 0
        GPIO.add_event_detect(ECHO_L, GPIO.BOTH, self.left_sensor_interrupt)
        print("UDP Robot Control listening")
        # Start up the server thread
        #self.server_thread = Thread(target = self.RightThread)
        #self.server_thread.daemon = True
        #self.server_thread.start()

        #self.server_thread = Thread(target = self.LeftThread)
        #self.server_thread.daemon = True
        #self.server_thread.start()

        self.server_thread = Thread(target = self.measure_left_sensor)
        self.server_thread.daemon = True
        self.server_thread.start()

    def measure_left_sensor(self):
        while (True):
            self.left_triggered = False
            self.left_falling = False
            GPIO.output(TRIGGER_L, True)
            time.sleep(0.00001)
            GPIO.output(TRIGGER_L, False)
            time.sleep(0.3) # Wait for the sensor to complete a reading
            if self.left_triggered:
                pulse_duration = self.left_pulse_end - self.left_pulse_start
                distance = pulse_duration * 17150
                print(distance)
            else:
                print("Out of range")
            time.sleep(0.5)

    def left_sensor_interrupt(self, pin):
        if self.left_falling:
            self.left_pulse_end = time.time()
            self.left_falling = False
        else:
            self.left_pulse_start = time.time()
            self.left_falling = True
        self.left_triggered = True
            

    def LeftThread(self):
        while (True):
            GPIO.output(TRIGGER_L, True)
            time.sleep(0.00001)
            GPIO.output(TRIGGER_L, False)

            while GPIO.input(ECHO_L) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO_L) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            print(distance)
            time.sleep(0.5)

    def MidThread(self):
        while (True):
            GPIO.output(TRIGGER_M, True)
            time.sleep(0.00001)
            GPIO.output(TRIGGER_M, False)

            while GPIO.input(ECHO_M) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO_M) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            print(distance)
            time.sleep(1)



if __name__ == "__main__":
    ctrl = UDPRobotControl()
    while (True):
        time.sleep(1)
