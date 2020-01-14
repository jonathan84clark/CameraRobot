###################################################################
# UDP DISTANCE SENSORS
# DESC: The distance sensors class reads data from the three distance
# sensors on the front of the robot.
# Author: Jonathan L Clark
# Date: 1/10/2019
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

class SensorData:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.falling_edge = False
        self.triggered = False
        self.pulse_start_time = 0
        self.pulse_end_time = 0
        self.distance = 0.0

class DistanceSensors:
    def __init__(self):
        self.left_sensor = SensorData(ECHO_L, TRIGGER_L)
        self.right_sensor = SensorData(ECHO_R, TRIGGER_R)
        self.middle_sensor = SensorData(ECHO_M, TRIGGER_M)
        GPIO.add_event_detect(ECHO_L, GPIO.BOTH, self.left_sensor_interrupt)
        GPIO.add_event_detect(ECHO_R, GPIO.BOTH, self.right_sensor_interrupt)
        GPIO.add_event_detect(ECHO_M, GPIO.BOTH, self.mid_sensor_interrupt)
        print("Distance Sensors operational")

        self.left_thread = Thread(target = self.measure_sensor, args=(self.left_sensor, ))
        self.left_thread.daemon = True
        self.left_thread.start()

        self.right_thread = Thread(target = self.measure_sensor, args=(self.right_sensor, ))
        self.right_thread.daemon = True
        self.right_thread.start()

        self.middle_thread = Thread(target = self.measure_sensor, args=(self.middle_sensor, ))
        self.middle_thread.daemon = True
        self.middle_thread.start()

    def measure_sensor(self, sensor):
        while (True):
            sensor.triggered = False
            sensor.falling_edge = False
            GPIO.output(sensor.trigger, True)
            time.sleep(0.00001)
            GPIO.output(sensor.trigger, False)
            time.sleep(0.3) # Wait for the sensor to complete a reading
            pulse_duration = sensor.pulse_end_time - sensor.pulse_start_time
            distance = pulse_duration * 17150
            if distance > 0:
                sensor.distance = distance

    def handle_interrupt(self, sensor):
        if sensor.falling_edge:
            sensor.pulse_end_time = time.time()
            sensor.falling_edge = False
        else:
            sensor.pulse_start_time = time.time()
            sensor.falling_edge = True

    def left_sensor_interrupt(self, pin):
        self.handle_interrupt(self.left_sensor)

    def right_sensor_interrupt(self, pin):
        self.handle_interrupt(self.right_sensor)

    def mid_sensor_interrupt(self, pin):
        self.handle_interrupt(self.middle_sensor)



if __name__ == "__main__":
    ctrl = DistanceSensors()
    while (True):
        time.sleep(1)
