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
from enum import Enum
from distance_sensors import DistanceSensors
from pwmDriver import PWMDriver

LEFT_A = 2
LEFT_B = 3
RIGHT_A = 26
RIGHT_B = 17
HEADLIGHTS_1 = 25
#HEADLIGHTS_1 = 27
#HEADLIGHTS_2 = 22
HEADLIGHTS_1 = 25
#HEADLIGHTS_2 = 22

# Setup the GPIO pins
GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(LEFT_A, GPIO.OUT) # Heater Pin
GPIO.setup(LEFT_B, GPIO.OUT) # Fan Pin
GPIO.setup(RIGHT_A, GPIO.OUT) # AC Pin
GPIO.setup(RIGHT_B, GPIO.OUT) # Main power line
GPIO.setup(HEADLIGHTS_1, GPIO.OUT) # Main power line
#GPIO.setup(HEADLIGHTS_2, GPIO.OUT) # Main power line

# Clear all relays
GPIO.output(LEFT_A, GPIO.LOW)
GPIO.output(LEFT_B, GPIO.LOW)
GPIO.output(RIGHT_A, GPIO.LOW)
GPIO.output(RIGHT_B, GPIO.LOW)
GPIO.output(HEADLIGHTS_1, GPIO.LOW)
#GPIO.output(HEADLIGHTS_2, GPIO.LOW) # Main power line

class Direction(Enum):
    FORWARD = 1
    REVERSE = 2
    STOP = 3
    LEFT = 4
    RIGHT = 5
    CENTER = 6

class UDPRobotControl:
    def __init__(self):
        #self.dist_sensors = distance_ref
        print("UDP Robot Control listening")
        self.headlight_state = False
        self.last_packet = int(round(time.time() * 1000))
        self.timed_out = False
        self.driver = PWMDriver()

        # Start up the server thread
        self.server_thread = Thread(target = self.UdpServerThread)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.com_thread = Thread(target = self.CheckCOMTimeout)
        self.com_thread.daemon = True
        self.com_thread.start()

    def headlights(self):
        if self.headlight_state:
            GPIO.output(HEADLIGHTS_1, GPIO.LOW)
            self.headlight_state = False
        else:
            GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
            self.headlight_state = True

    def change_movement(self, input):
        moveForwardRev = False
        if input == Direction.FORWARD:
            self.driver.set_throttle(0.5, 0.0)
            #self.driver.main_throttle = 0.5
            #print("Call")
            #self.driver.turn_vector = 0.0
            moveForwardRev = True
        elif input == Direction.REVERSE:
            #self.driver.main_throttle = -0.5
            self.driver.set_throttle(-0.5, 0.0)
            #self.driver.turn_vector = 0.0
            moveForwardRev = True
        elif input == Direction.STOP:
            #self.driver.main_throttle = 0.0
            self.driver.set_throttle(0.0, 0.0)
        elif input == Direction.CENTER:
            self.driver.turn_vector = 0.0
        if input == Direction.LEFT:
            self.driver.turn_vector = -0.5
        elif input == Direction.RIGHT:
            self.driver.turn_vector = 0.5
        elif not moveForwardRev:
            self.driver.turn_vector = 0.0
            self.driver.main_throttle = 0.0

    # Monitors the control system; checking for timeouts
    def CheckCOMTimeout(self):
        time.sleep(1)
        while True:
            delta_t = int(round(time.time() * 1000)) - self.last_packet
            if delta_t > 1000 and self.timed_out == False:
                print("Got no communication for 1 second")
                self.change_movement(Direction.STOP)
                self.change_movement(Direction.CENTER)
                self.timed_out = True
            elif delta_t < 1000 and self.timed_out:
                print("Communication resumed")
                self.timed_out = False
            time.sleep(0.3)

    # Handles recieving UDP timeouts
    def UdpServerThread(self):
        UDP_IP_ADDRESS = "192.168.1.14"
        UDP_PORT_NO = 6789

        msg = [0, 0, 0, 0, 0, 0, 0, 0]
        data = bytearray(msg)
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

        while True:
            rec_len = serverSock.recv_into(data, 8)
            # Ensure we have a valid control code
            if data[0] == 81 and data[1] == 12:
                self.last_packet = int(round(time.time() * 1000))
                if (data[2] == 1):
                    self.change_movement(Direction.FORWARD)
                elif (data[2] == 2):
                    self.change_movement(Direction.STOP)
                elif (data[2] == 3):
                    self.change_movement(Direction.REVERSE)
                elif (data[2] == 4):
                    self.change_movement(Direction.STOP)
                elif (data[2] == 5):
                    self.change_movement(Direction.CENTER)
                elif (data[2] == 6):
                    self.change_movement(Direction.LEFT)
                elif (data[2] == 7):
                    self.change_movement(Direction.RIGHT)
                elif (data[2] == 8):
                    self.change_movement(7)
                elif (data[2] == 9):
                    self.change_movement(8)
                elif (data[3] == 1):
                    GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
                    self.headlight_state = True
                elif (data[3] == 0):
                    GPIO.output(HEADLIGHTS_1, GPIO.LOW)
                    self.headlight_state = False
                else:
                    print("No cmd: ")
                    print(data)

if __name__ == "__main__":
    ctrl = UDPRobotControl()
    while (True):
        time.sleep(1)
