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
import urllib.request
print('Start GPS Test')


# Variablen

result = {
            "MAC_Adresse" : "",
            "Latitude" : "",
            "Longitude" : "",
            "Speed" : "",
            "Time" : "",
            "GSM" : "",
            "ETH1" : "",
            "ETH2" : "",
            "Memory" : "",
}

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


def connect_gps_client():
    print("----- Start GPS test -----")
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
                    print('Daten sind gültig')

                    if latitude != 0.0 and longitude != 0.0:
                        print('Standort gefunden -> Test wird beendet')
                        test_beenden = True
                        result["Latitude"] = str(latitude)
                        result["Longitude"] = str(longitude)
                        result["Speed"] = str(result.get("speed"))
                        result["Time"] = str(result.get("time"))

                        break

                    else:
                        print('Daten sind gültig es wurde aber kein Standort gefunden')

                else:
                    print('Daten nicht gültig -> warten bis gps initialisiert ist.')


def check_ping():
    print("----- Start ping -----")
    try:
        urllib.request.open('https://www.stadlerrail.com/de/')
        print('URL OK')
        os.system('ping stadlerrail.com')
        time.sleep(5)
        #os.system('sudo cmd .') -> überprüfen
        print('Ping OK')
        result["GSM"] = "OK"
        print('Test finished')
    except:
        print('URL fail: No connection -> Check sim and repeat test')


def memory_test():
    print("----- Start memory test -----")
    #os.system('sudo hdparm -t /dev/sda')
    cmd = os.popen('sudo hdparm -t /dev/sda')
    result["Memory"] = cmd[2]


def show_macaddr():
    print("----- Show MAC-Adresse -----")
    os.system('ip -brief link')

def get_result():
    for i in result:
        print(i)



if __name__ == '__main__':
    init_gps()
    start_deamon()
    connect_gps_client()
    check_ping()
    get_result()
