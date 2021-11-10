import socket
import time


def ETH_client():
    print('Client Init')
    ip = "172.17.120.59"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 50021))
    try:
        while True:
            nachricht = "works"
            s.send(nachricht.encode())
            antwort = s.recv(1024)
            print("[{}] {}".format(ip, antwort.decode()))
            if antwort.decode() == "works":
                print("success")
                break
    finally:
        s.close()

if __name__ == '__main__':
    ETH_client()
