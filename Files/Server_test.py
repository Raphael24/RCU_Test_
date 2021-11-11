import socket
import time


def test_server():
    print('test server')
    time.sleep(10)



def ETH_server():
    print('Server Init')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 50001))
    s.listen(1)
    try:
        while True:
            print("Server waiting")
            komm, addr = s.accept()
            while True:
                data = komm.recv(1024)
                if not data:
                    komm.close()
                    break

                print("[{}] {}".format(addr[0], data.decode()))
                komm.send(data)
                s.close()

    finally:
        s.close()
