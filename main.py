#!/usr/bin/python
#################################################################
# ROBOT
# DESC: The robot webserver is a simple server designed to control a robot
# from the raspberry PI3
# Author: Jonathan L Clark
# Date: 10/27/2019, Modified the server to support posts and gets.
##################################################################
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
from os import curdir, sep
import time
from threading import Thread
from time import sleep
import datetime
import json
import time
from os.path import expanduser
import RPi.GPIO as GPIO
import subprocess
from enum import Enum
from udpRobotCtrl import UDPRobotControl
from distance_sensors import DistanceSensors

supported_files = {".html" : 'text/html', ".css" : 'text/css', "jpeg" : 'image/jpeg',
                   ".js" : 'text/javascript'}

dataSet = {"mode" : 0.0 , "left_sensor" : 0.0, "mid_sensor" : 0.0, "right_sensor" : 0.0}

headlight_state = False
HEADLIGHTS_1 = 25

class Direction(Enum):
    FORWARD = 1
    REVERSE = 2
    STOP = 3
    LEFT = 4
    RIGHT = 5
    CENTER = 6

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global distanceSensors

        if (self.path == "/"):
            self.path = "/index.html"
        
        curdir = "/home/pi/CameraRobot"
        file_path = curdir + sep + self.path
        filename, file_extension = os.path.splitext(file_path)
        if (self.path == "/data.json"):
            dataSet["left_sensor"] = distanceSensors.left_sensor.distance
            dataSet["mid_sensor"] = distanceSensors.middle_sensor.distance
            dataSet["right_sensor"] = distanceSensors.right_sensor.distance
            self.send_response(200)
            self.send_header('Content-type', "text/json")
            self.end_headers()
            jsonString = json.dumps(dataSet)
            self.wfile.write(jsonString)
        elif (os.path.isfile(file_path) and file_extension in supported_files):
            f = open(file_path, 'rb')
            self.send_response(200)
            self.send_header('Content-type', supported_files[file_extension])
            self.end_headers()
            self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        global dataSet
        global udpControl
        # Doesn't do anything with posted data
        output = "Submitted"
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_list = post_data.split("&") # Extract the individual post commands
        for post_str in post_list:
            key_value = post_str.split("=")
            if (len(key_value) == 2):
                if (key_value[0] == "forward"):
                    udpControl.set_throttle(0.8, 0.0)
                elif (key_value[0] == "stopforward"):
                    udpControl.set_throttle(0.0, 0.0)
                elif (key_value[0] == "reverse"):
                    udpControl.set_throttle(-0.8, 0.0)
                elif (key_value[0] == "stopreverse"):
                    udpControl.set_throttle(0.0, 0.0)
                elif (key_value[0] == "center"):
                    udpControl.set_throttle(0.0, 0.0)
                elif (key_value[0] == "left"):
                    udpControl.set_throttle(0.0, -0.8)
                elif (key_value[0] == "right"):
                    udpControl.set_throttle(0.0, 0.8)
                elif (key_value[0] == "stopleft"):
                    udpControl.set_throttle(0.0, 0.0)
                elif (key_value[0] == "stopright"):
                    udpControl.set_throttle(0.0, 0.0)
                elif (key_value[0] == "toggle_lights"):
                    self.headlights()
            else:
                pass#write_log("SERVER", 1, "ERROR: Invalid command format: " + post_str)
            
        self._set_headers()
        self.wfile.write("<html><body><h1>" + output + "</h1></body></html>")

    def headlights(self):
        global headlight_state
        if headlight_state:
            GPIO.output(HEADLIGHTS_1, GPIO.HIGH)
            headlight_state = False
        else:
            GPIO.output(HEADLIGHTS_1, GPIO.LOW)
            headlight_state = True

def runServer(server_class=HTTPServer, handler_class=S, port=5000):
    global dataSet
    
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd...'
        httpd.serve_forever()
    except:
       write_log("SERVER", 1, "ERROR: Unable to start server, trying again")
       sleep(5)
       runServer()
        

if __name__ == "__main__":
	# Start up the server thread
    #thread = Thread(target = runServer)
    #thread.daemon = True
    #thread.start()

    #subprocess.call('python3 /home/pi/CameraRobot/rpi_camera.py &', shell=True)
    udpControl = UDPRobotControl()
    #distanceSensors = DistanceSensors()

    while (True):
        time.sleep(1)
        
