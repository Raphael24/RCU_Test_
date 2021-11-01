#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#NMEA stream auslesen
#https://fishandwhistle.net/post/2016/using-pyserial-pynmea2-and-raspberry-pi-to-log-nmea-output/

# Libs
import serial
import pynmea2

# Built-in/Generic Imports
import socket
import sys
import os
print('adsf')


def init_gps():
    with serial.Serial('/dev/ttyUSB3', baudrate=9600, timeout=5) as ser:
        print('Succesfully Connected to ttyUSB3')
        ser.write('AT$GPSP=1')
        print('GPS Power on')
        ser.write('AT$GPSAT=1')
        print('GPS power on')
        ser.write('AT$GPSNMUN=0,1,1,1,1,1,1')
        print('GPS output format')

def start_deamon():
    os.system('sudo service gpsd start')
    #os.system('sudo service gpsd status')

"""
with serial.Serial('/dev/ttyUSB2', baudrate=9600, timeout=5) as ser:
    print('Succesfully Connected to ttyUSB2')
    # read 10 lines from the serial output
    for i in range(10):
        line = ser.readline().decode('ascii', errors='replace')
        print(line.strip())
"""


gps_server = socket.Socket(socket.AF_INET, SOCK_STREAM)
gps_server.connect(('127.0.0.0', 2947))

def connect_gps():
    try:
        while True:
            cord = s.recv(1024)
            print(cord)
    finally:
        gps_server.close()
