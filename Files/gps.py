#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#NMEA stream auslesen
#https://fishandwhistle.net/post/2016/using-pyserial-pynmea2-and-raspberry-pi-to-log-nmea-output/
#https://github.com/tfeldmann/gpsdclient

# Libs
import serial
import pynmea2
import gpsd
from gpsdclient import GPSDClient

# Built-in/Generic Imports
import socket
import sys
import os
import time
print('Start GPS Test')


def init_gps():
    with serial.Serial('/dev/ttyUSB3', baudrate=9600, timeout=5) as ser:
        print('Succesfully Connected to ttyUSB3')
        ser.write(b'AT$GPSP=1\r')
        print('GPS Ein')
        ser.write(b'AT$GPSAT=1\r')
        print('GPS Power Ein')
        ser.write(b'AT$GPSNMUN=0,1,1,1,1,1,1\r')
        print('GPS set output format\r')
        ser.close()

def start_deamon():
    os.system('sudo service gpsd start')
    print('RCU Test: Start Deamon')
    #os.system('sudo service gpsd status')


def connect_gps():
    gpsd.connect()
    gpsd.connect(host="127.0.0.1", port=2947)
    packet = gpsd.get_current()
    print(packet.position())


def connect_gps_client():
    client = GPSDClient(host="127.0.0.1")
    test_beenden = False
    while test_beenden != True:
        for result in client.dict_stream(convert_datetime=True):
            if result["class"] == "TPV":
                print("Latitude: %s" % result.get("lat", "n/a"),
                "Longitude: %s" % result.get("lon", "n/a"),
                "Speed: %s" % result.get("speed", "n/a"),
                "Time: %s" % result.get("time", "n/a"))

                latitude = result.get("lat")
                longitude = result.get("lon")

                if type(latitude) != type(None) and type(longitude) != type(None):
                    print('Daten Valid')
                    if latitude != 0.0 and longitude != 0.0:
                        print('Standort gefunden -> Test wird beendet')
                        test_beenden = True

                    else:
                        print('Daten nicht gültig -> warten bis gps initialisiert ist.')



if __name__ == '__main__':
    init_gps()
    start_deamon()
    connect_gps_client()
