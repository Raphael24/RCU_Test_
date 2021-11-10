import socket


def ETH_server():
    print('Server Init')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 50021))
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

    finally:
        s.close()

if __name__ == '__main__':
    ETH_server()
