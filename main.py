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

supported_files = {".html" : 'text/html', ".css" : 'text/css', "jpeg" : 'image/jpeg',
                   ".js" : 'text/javascript'}

dataSet = {"mode" : 0.0 }

# Setup the GPIO pins
GPIO.setwarnings(False) # Disable unused warnings
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(2, GPIO.OUT) # Heater Pin
GPIO.setup(3, GPIO.OUT) # Fan Pin
GPIO.setup(4, GPIO.OUT) # AC Pin
GPIO.setup(17, GPIO.OUT) # Main power line
GPIO.setup(27, GPIO.OUT) # Main power line
GPIO.setup(22, GPIO.OUT) # Main power line

# Clear all relays
GPIO.output(2, GPIO.LOW)
GPIO.output(3, GPIO.LOW)
GPIO.output(4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.HIGH)
GPIO.output(22, GPIO.LOW)

headlight_state = False

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if (self.path == "/"):
            self.path = "/index.html"
        
        curdir = "/home/pi/CameraRobot"
        file_path = curdir + sep + self.path
        filename, file_extension = os.path.splitext(file_path)
        if (self.path == "/data.js"):
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
        # Doesn't do anything with posted data
        output = "Submitted"
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_list = post_data.split("&") # Extract the individual post commands
        for post_str in post_list:
            key_value = post_str.split("=")
            if (len(key_value) == 2):
                if (key_value[0] == "forward"):
                    self.change_movement(0)
                elif (key_value[0] == "stopforward"):
                    self.change_movement(1)
                elif (key_value[0] == "reverse"):
                    self.change_movement(2)
                elif (key_value[0] == "stopreverse"):
                    self.change_movement(3)
                elif (key_value[0] == "center"):
                    self.change_movement(4)
                elif (key_value[0] == "left"):
                    self.change_movement(5)
                elif (key_value[0] == "right"):
                    self.change_movement(6)
                elif (key_value[0] == "stopleft"):
                    self.change_movement(7)
                elif (key_value[0] == "stopright"):
                    self.change_movement(8)
                elif (key_value[0] == "toggle_lights"):
                    self.headlights()
            else:
                pass#write_log("SERVER", 1, "ERROR: Invalid command format: " + post_str)
            
        self._set_headers()
        self.wfile.write("<html><body><h1>" + output + "</h1></body></html>")

    def headlights(self):
        global headlight_state
        if headlight_state:
            GPIO.output(27, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            headlight_state = False
        else:
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            headlight_state = True

    def change_movement(self, input):
        if input == 0:
            GPIO.output(2, GPIO.HIGH)
            GPIO.output(3, GPIO.LOW)
        elif input == 2:
            GPIO.output(2, GPIO.LOW)
            GPIO.output(3, GPIO.HIGH)
        elif input == 1 or input == 3:
            GPIO.output(2, GPIO.LOW)
            GPIO.output(3, GPIO.LOW)
        elif input == 4:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
        elif input == 5:
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
        elif input == 6:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.HIGH)
        print("Got movement post: " +  str(input))

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
    thread = Thread(target = runServer)
    thread.daemon = True
    thread.start()

    while (True):
        time.sleep(1)
        
