import socket




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.17.120.211', 50001))

try:
    while True:
        antwort = client.recv(1024)
        print("[{}] {}".format(ip, antwort.decode()))

finally:
    s.close()
