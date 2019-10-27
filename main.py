#!/usr/bin/python
#################################################################
# THERMOSTAT
# DESC: The thermostat application is a multi-threaded python program
# designed to manage the temperature system of a house.
# The server must run on Python 2.7
# Modifier: Jonathan L Clark
# Date: 11/3/2018. Started fleshing out basic thermostat operating
# code.
# Update: 11/8/2018, Added the statistics measurement system as well
# as the other needed threads and sub systems. Validated that all systems
# are working.
# Update: 11/10/2018, The relay board uses LOW values to enable relays.
# On boot the GPIO pins are low which would turn on all relays. So 
# what we will do is have the 4th really switch the power. The power will
# only be applied if that relay is in the off position (high). This will
# allow us to control when the system is working.
# Update: 2/21/2019, Cleaned up the code. Also added the code for the new 
# Yahoo weather API.
##################################################################
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from weather import Weather, Unit
import SocketServer
import os
from os import curdir, sep
import time
from sys import argv
from threading import Thread
from time import sleep
import datetime
import json
import time, uuid, urllib, urllib2
import hmac, hashlib
from base64 import b64encode
from os.path import expanduser


location = 'spokane,wa'
variance = 1
app_id = ''
consumer_key = ''
consumer_secret = ''

logFilePath = "C:\\Users\\jonat\\Desktop\\"
#logFilePath = "/home/pi/GitHub/Server/Thermastat"
supported_files = {".html" : 'text/html', ".css" : 'text/css', "jpeg" : 'image/jpeg',
                   ".js" : 'text/javascript'}

dataSet = {"target" : 69.0, "temperature" : 60, "humidity" : 20, "weatherTemp": 70.0, "weatherHumid": 30.0, "windspd": 20,
           "acStatus" : False, "fanStatus" : False, "heaterStatus": False, "autoStatus": True}

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def statusToString(self, status):
        if (status == True):
            return "On"
        else:
            return "Off"

    def do_GET(self):
        if (self.path == "/"):
            self.path = "/index.html"
        print(self.path)
        
        curdir = "C:\Users\jonat\Desktop\CameraRobot"
        file_path = curdir + sep + self.path
        filename, file_extension = os.path.splitext(file_path)
        print(file_extension)
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
                if (key_value[0] == "off"):
                    self.toggle_off()
                elif (key_value[0] == "ac"):
                    self.toggle_ac()
                elif (key_value[0] == "fan"):
                    self.toggle_fan()
                elif (key_value[0] == "heat"):
                    self.toggle_heat()
                elif (key_value[0] == "auto"):
                    self.toggle_auto()
                elif (key_value[0] == "target"):
                    dataSet["target"] = float(key_value[1])
                    pass#write_log("SERVER", 2, "Target temp set to: " + str(key_value[1]))
                else:
                    pass#write_log("SERVER", 1, "ERROR: Invalid command: " + post_str)
            else:
                pass#write_log("SERVER", 1, "ERROR: Invalid command format: " + post_str)
            
        self._set_headers()
        self.wfile.write("<html><body><h1>" + output + "</h1></body></html>")

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
    #sleep(50)

	# Start up the server thread
    thread = Thread(target = runServer)
    thread.daemon = True
    thread.start()
    home = expanduser("~")

    print(home)
    while (True):
        pass
        
