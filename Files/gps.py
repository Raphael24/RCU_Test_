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
import time
print('adsf')


def init_gps():
    with serial.Serial('/dev/ttyUSB3', baudrate=9600, timeout=5) as ser:
        print('Succesfully Connected to ttyUSB3')
        ser.write(b'AT$GPSP=1\r')
        print('GPS Power on')
        ser.write(b'AT$GPSAT=1\r')
        print(b'GPS power on')
        ser.write(b'AT$GPSNMUN=0,1,1,1,1,1,1\r')
        print(b'GPS output format\r')

def start_deamon():
    os.system('sudo service gpsd start')
    print('RCU Test: Start Deamon')
    #os.system('sudo service gpsd status')

"""
with serial.Serial('/dev/ttyUSB2', baudrate=9600, timeout=5) as ser:
    print('Succesfully Connected to ttyUSB2')
    # read 10 lines from the serial output
    for i in range(10):
        line = ser.readline().decode('ascii', errors='replace')
        print(line.strip())
"""



def connect_gps():
    print('connect to GPS')
    gps_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gps_server.connect(('127.0.0.1', 2947))
    try:
        while True:
            cord = s.recv(1024)
            print(cord)
            try:

                cord = pynmea2.parse(cord)
                print(cord)
                num_sat = cord.num_sats
                print(num_sat)
                latitude = cord.latitude
                print(latitude)
                longitude = cord.longitude
                print(longitude)
                altitude_units = cord.altitude_units
                print(altitude_units)

            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                continue
    finally:
        gps_server.close()

if __name__ == '__main__':
    init_gps()
    start_deamon()
    print('Wait 5 Sec')
    time.sleep(5)
    connect_gps()
