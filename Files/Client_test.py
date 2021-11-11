import socket
import time

def test_client():
    print('test client')

def ETH_client(ip):
    print('Client Init')
    #ip = "192.168.2.101"
    ip = ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 50001))
    try:
        while True:
            nachricht = "works"
            s.send(nachricht.encode())
            antwort = s.recv(1024)
            print("[{}] {}".format(ip, antwort.decode()))
            if antwort.decode() == "works":
                print("success")
                return "OK"
                break
            else:
                print("Conection_Error")
                return "NOK"
                break
    finally:
        s.close()
