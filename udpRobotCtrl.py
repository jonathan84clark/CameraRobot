###################################################################
# UDP ROBOT CONTROL
# DESC: The UDP robot control system controls the robot using UDP
# packets.
# Author: Jonathan L Clark
# Date: 12/3/2019
###################################################################
import socket
import time
import serial
from threading import Thread
from time import sleep
import datetime
import RPi.GPIO as GPIO
from enum import Enum
from distance_sensors import DistanceSensors
from Drive import DriveSystem

STEER_A = 19
STEER_B = 18
MAIN_A = 12
MAIN_B = 13
HEADLIGHTS = 25

# Setup the GPIO pins
GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

class UDPRobotControl:
    def __init__(self):
        self.drive = DriveSystem(MAIN_A, MAIN_B, STEER_A, STEER_B, HEADLIGHTS, 1000)
        self.drive.manual_control(0.0, 0.0)

        #self.dist_sensors = distance_ref
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

    # Monitors the control system; checking for timeouts
    def CheckCOMTimeout(self):
        time.sleep(1)
        while True:
            delta_t = int(round(time.time() * 1000)) - self.last_packet
            if delta_t > 1000 and self.timed_out == False:
                print("Got no communication for 1 second")
                self.drive.manual_control(0.0, 0.0)
                self.timed_out = True
            elif delta_t < 1000 and self.timed_out:
                print("Communication resumed")
                self.timed_out = False
            time.sleep(0.3)

    # Handles recieving UDP timeouts
    def UdpServerThread(self):
        UDP_IP_ADDRESS = "192.168.1.19"
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
                xThrottle = float(data[2]) / 100.0
                yThrottle = float(data[4]) / 100.0
                if data[3] == 1:
                    xThrottle *= -1.0
                if data[5] == 1:
                    yThrottle *= -1.0
                if data[6] == 1 and self.headlight_state != True:
                    self.headlight_state = True
                    self.drive.set_headlights(True)
                elif data[6] == 0 and self.headlight_state != False:
                    self.headlight_state = False
                    self.drive.set_headlights(False)
                forward_throttle = yThrottle
                steering_throttle = xThrottle
                self.drive.manual_control(forward_throttle, steering_throttle)

if __name__ == "__main__":
    ctrl = UDPRobotControl()
    while (True):
        time.sleep(1)
