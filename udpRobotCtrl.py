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
from pwmDriver import PWMDriver

LEFT_A = 19
LEFT_B = 13
RIGHT_A = 18
RIGHT_B = 12
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
left_a = GPIO.PWM(LEFT_A, 50)
left_b = GPIO.PWM(LEFT_B, 50)

right_a = GPIO.PWM(RIGHT_A, 50)
right_b = GPIO.PWM(RIGHT_B, 50)

left_a.start(0) 
left_b.start(0)

right_a.start(0) 
right_b.start(0)

#left_a.ChangeDutyCycle(0)

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
        self.throttle = 0.0
        self.steering = 0.0
        #self.dist_sensors = distance_ref
        print("UDP Robot Control listening")
        self.headlight_state = False
        self.last_packet = int(round(time.time() * 1000))
        self.timed_out = False
        #self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

        # Start up the server thread
        self.server_thread = Thread(target = self.UdpServerThread)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.com_thread = Thread(target = self.CheckCOMTimeout)
        self.com_thread.daemon = True
        self.com_thread.start()

    # Handles communication with the main motor
    def set_throttle(self, set_forward, set_turn):
        left_turn_vector = 0.0
        right_turn_vector = 0.0
        if set_turn < 0.0:
            left_turn_vector = abs(set_turn)
            if set_forward < 0.0:
                left_turn_vector *= -1.0
            elif set_turn > 0.0:
                right_turn_vector = set_turn
                if set_forward < 0.0:
                    right_turn_vector *= -1.0

        left_throttle = 0x00 | int((set_forward * 100.0) - (left_turn_vector * 100.0))
        right_throttle = 0x00 | int((set_forward * 100.0) - (right_turn_vector * 100.0))
        if right_throttle >= 0.0:
            right_a.ChangeDutyCycle(right_throttle)
            right_b.ChangeDutyCycle(0)
        elif right_throttle < 0.0:
            right_a.ChangeDutyCycle(0)
            right_b.ChangeDutyCycle(abs(right_throttle))

        if left_throttle >= 0.0:
            left_a.ChangeDutyCycle(left_throttle)
            left_b.ChangeDutyCycle(0)
        elif left_throttle < 0.0:
            left_a.ChangeDutyCycle(0)
            left_b.ChangeDutyCycle(abs(left_throttle))

    def headlights(self):
        if self.headlight_state:
            GPIO.output(HEADLIGHTS_1, GPIO.LOW)
            self.headlight_state = False
        else:
            GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
            self.headlight_state = True

    def change_movement(self, input):
        moveForwardRev = False
        forward_throttle = 0.0
        steering_angle = 0.0
        if input == Direction.FORWARD:
            forward_throttle = 0.8
        elif input == Direction.REVERSE:
            forward_throttle = -0.8
        elif input == Direction.STOP:
            forward_throttle = 0.0
            #print("Stop")
        elif input == Direction.CENTER:
            steering_angle = 0.0
        if input == Direction.LEFT:
            steering_angle = 0.8
        elif input == Direction.RIGHT:
            steering_angle = -0.8

        self.set_throttle(forward_throttle, steering_angle)

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
