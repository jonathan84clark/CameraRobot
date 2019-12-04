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

FORWARD_A = 2
FORWARD_B = 3
STEERING_A = 4
STEERING_B = 17
HEADLIGHTS_1 = 27
HEADLIGHTS_2 = 22

# Setup the GPIO pins
GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(FORWARD_A, GPIO.OUT) # Heater Pin
GPIO.setup(FORWARD_B, GPIO.OUT) # Fan Pin
GPIO.setup(STEERING_A, GPIO.OUT) # AC Pin
GPIO.setup(STEERING_B, GPIO.OUT) # Main power line
GPIO.setup(HEADLIGHTS_1, GPIO.OUT) # Main power line
GPIO.setup(HEADLIGHTS_2, GPIO.OUT) # Main power line

# Clear all relays
GPIO.output(FORWARD_A, GPIO.LOW)
GPIO.output(FORWARD_B, GPIO.LOW)
GPIO.output(STEERING_A, GPIO.LOW)
GPIO.output(STEERING_B, GPIO.LOW)
GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
GPIO.output(HEADLIGHTS_2, GPIO.LOW)

class Direction(Enum):
    FORWARD = 1
    REVERSE = 2
    STOP = 3
    LEFT = 4
    RIGHT = 5
    CENTER = 6

class UDPRobotControl:
    def __init__(self):
        print("UDP Robot Control listening")
        self.headlight_state = False
        self.last_packet = int(round(time.time() * 1000))
        self.timed_out = False

        # Start up the server thread
        self.server_thread = Thread(target = self.UdpServerThread)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.com_thread = Thread(target = self.CheckCOMTimeout)
        self.com_thread.daemon = True
        self.com_thread.start()

    def headlights(self):
        if self.headlight_state:
            GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
            GPIO.output(HEADLIGHTS_2, GPIO.LOW)
            self.headlight_state = False
        else:
            GPIO.output(HEADLIGHTS_1, GPIO.LOW)
            GPIO.output(HEADLIGHTS_2, GPIO.HIGH)
            self.headlight_state = True

    def change_movement(self, input):
        if input == Direction.FORWARD:
            GPIO.output(FORWARD_A, GPIO.HIGH)
            GPIO.output(FORWARD_B, GPIO.LOW)
        elif input == Direction.REVERSE:
            GPIO.output(FORWARD_A, GPIO.LOW)
            GPIO.output(FORWARD_B, GPIO.HIGH)
        elif input == Direction.STOP:
            GPIO.output(FORWARD_A, GPIO.LOW)
            GPIO.output(FORWARD_B, GPIO.LOW)
        elif input == Direction.CENTER:
            GPIO.output(STEERING_A, GPIO.LOW)
            GPIO.output(STEERING_B, GPIO.LOW)
        elif input == Direction.LEFT:
            GPIO.output(STEERING_A, GPIO.LOW)
            GPIO.output(STEERING_B, GPIO.HIGH)
        elif input == Direction.RIGHT:
            GPIO.output(STEERING_A, GPIO.HIGH)
            GPIO.output(STEERING_B, GPIO.LOW)

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
        UDP_IP_ADDRESS = "127.0.0.1"
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
                elif (data[2] == 5:
                    self.change_movement(Direction.CENTER)
                elif (data[2] == 6):
                    self.change_movement(Direction.LEFT)
                elif (data[2] == 7):
                    self.change_movement(Direction.RIGHT)
                elif (data[2] == 8):
                    self.change_movement(7)
                elif (data[2] == 9):
                    self.change_movement(8)
                elif (data[2] == 10):
                    self.headlights()

if __name__ == "__main__":
    ctrl = UDPRobotControl()
    while (True):
        time.sleep(1)
