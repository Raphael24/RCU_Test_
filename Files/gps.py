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
import threading
import Server_test
import Client_test

# Built-in/Generic Imports
import socket
import sys
import os
import time
import urllib.request

# Variablen

Test_result = {
            "Latitude" : "NOK",
            "Longitude" : "NOK",
            "Speed" : "NOK",
            "Time" : "NOK",
            "GSM" : "NOK",
            "ETH1" : "NOK",
            "ETH2" : "NOK",
            "Memory" : "NOK",
}


class test_server(threading.Thread):
    def run(self):
        print('----- MAIN: Run Server -----')
        Server_test.ETH_server()


class test_client(threading.Thread):
    def run(self):
        print('MAIN: Run Client')
        ETH1 = Client_test.ETH_client(ip="192.168.2.101")  # "192.168.2.101"
        ETH2 = Client_test.ETH_client(ip="192.168.2.102")  # "192.168.2.102"
        Test_result.update({"ETH1": ETH1, "ETH2": ETH2})


WServer = test_server()
WClient = test_client()


def init_gps():
    print("----- Init GPS -----\n")
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
    print('RCU Test: Start Deamon\n')
    #os.system('sudo service gpsd status')

def connect_gps_client():
    print("----- Start GPS test -----\n")
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
                        Test_result["Latitude"] = str(latitude)
                        Test_result["Longitude"] = str(longitude)
                        Test_result["Speed"] = str(result.get("speed"))
                        Test_result["Time"] = str(result.get("time"))
                        print('Standort gefunden -> Test wird beendet\n')
                        #print(Test_result, "\n")
                        test_beenden = True

                        break

                    else:
                        print('Daten sind gültig es wurde aber kein Standort gefunden')

                else:
                    print('Daten nicht gültig -> warten bis gps initialisiert ist.')


def check_ping():
    print("----- Start Ping -----")
    try:
        urllib.request.urlopen('https://www.stadlerrail.com')
        print('URL OK:  [https://www.stadlerrail.com]')
        Test_result["GSM"] = "OK"
    except:
        print('URL fail: No connection -> Check sim and repeat test\n')
        Test_result["GSM"] = "NOT OK"

def memory_test():
    print("----- Start memory test -----")
    #os.system('sudo hdparm -t /dev/sda')
    cmd = os.popen('sudo hdparm -t /dev/sda')
    for i in cmd:
        print(i)
        Test_result.update({"Memory" : i })

def show_macaddr():
    print("----- MAC-Adresse -----\n")
    os.system('ip -brief link')
    a = os.popen('ip -brief link')
    print("\n")


def get_result():
    print("----- Start Test Result -----\n")
    for i in Test_result:
        print(i, ":", Test_result[i])
    print("----- End Test Result -----\n")


if __name__ == '__main__':
    init_gps()
    start_deamon()
    connect_gps_client()
    check_ping()
    show_macaddr()
    memory_test()
    #print('Start ETH-Test')
    WServer.start()
    #print('Server online')
    WClient.start()
    #print('Client online')
    WServer.join()
    WClient.join()
    print('Test fertig')
    get_result()
