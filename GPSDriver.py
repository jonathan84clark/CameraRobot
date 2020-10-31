###################################################################
# GPS DRIVER
# DESC: The GPS driver interacts with a ubox GPS device. It is intended to
# provide simple read-only values for GPS data
# Author: Jonathan L Clark
# Date: 10/30/2020
###################################################################
import serial
import time
from threading import Thread

class GPSDriver:
    def __init__(self):
        self.ser = serial.Serial('COM4')
        self.time = ""
        self.latitude = 0.0
        self.gps_fix = 0
        self.num_sats = 0
        self.hdop = 0.0
        self.altitude = 0.0
        self.track_made_good = 0.0
        self.magnetic_track_good = 0.0
        self.ground_speed_knots = 0.0
        self.ground_speed_kmh = 0.0
        self.pdop = 0.0
        self.hdop = 0.0
        self.vdop = 0.0

        # Start up the server thread
        self.read_thread = Thread(target = self.ReadGPS)
        self.read_thread.daemon = True
        self.read_thread.start()

    def ProcessGPSString(self, degreesStr, directionStr):
        degrees = float(degreesStr)
        intDegrees = int(degrees / 100.0)
        minutes = degrees - float(intDegrees) * 100.0

        decimal_degrees = float(intDegrees) + (minutes / 60.0)
        if directionStr == 'S' or directionStr == 'W':
            decimal_degrees *= -1.0

        return decimal_degrees
    
    # Processes the GPGGA message
    def ProcessGPGGA(self, splitMessage):
        time_stamp = splitMessage[1][0] + splitMessage[1][1] + ":"
        time_stamp += splitMessage[1][2] + splitMessage[1][3] + ":"
        time_stamp += splitMessage[1][3] + splitMessage[1][4]
        self.time = time_stamp
        self.latitude = self.ProcessGPSString(splitMessage[2], splitMessage[3])
        self.longitude = self.ProcessGPSString(splitMessage[4], splitMessage[5])
        self.gps_fix = int(splitMessage[6])
        self.num_sats = int(splitMessage[7])
        self.hdop = float(splitMessage[8])
        self.altitude = float(splitMessage[9]) * 3.28084
       
    # Process the GPVTG message  
    def ProcessGPVTG(self, splitMessage):
        #self.track_made_good = float(splitMessage[1])
        #self.magnetic_track_good = float(splitMessage[3])
        self.ground_speed_knots = float(splitMessage[5])
        self.ground_speed_kmh = float(splitMessage[7])

    # Proces the GPRMC message
    def ProcessGPRMC(self, splitMessage):
        pass

    # Process the GPGSA message
    def ProcessGPGSA(self, splitMessage):
        self.pdop = float(splitMessage[15])
        self.hdop = float(splitMessage[16])
        vdopSplit = splitMessage[17].split('*')
        self.vdop = float(vdopSplit[0])

    # Reads the GPS unit data
    def ReadGPS(self):
        while (True):
            data = self.ser.readline().strip()
            splitMessages = data.split(",")
            if splitMessages[0] == '$GPGGA':
                self.ProcessGPGGA(splitMessages)
            elif splitMessages[0] == '$GPGSV': # Desc of each sat in view
                pass
            elif splitMessages[0] == '$GPTXT': # Data about the Ubox GPS
                pass
            elif splitMessages[0] == '$GPGLL': # latitude and longitude
                pass
            elif splitMessages[0] == '$GPVTG':
                self.ProcessGPVTG(splitMessages)
            elif splitMessages[0] == '$GPRMC':
                self.ProcessGPRMC(splitMessages)
            elif splitMessages[0] == '$GPGSA':
                self.ProcessGPGSA(splitMessages)
            else:
                print(splitMessages[0])

if __name__ == "__main__":
    ctrl = GPSDriver()
    while (True):
        time.sleep(1)
