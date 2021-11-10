import threading
import Server_test
import Client_test

print('Start main')

class test_server(threading.Thread):
    def run(self):
        print('MAIN: Run Server')
        Server_test.ETH_server()


class test_client(threading.Thread):
    def run(self):
        print('MAIN: Run Client')
        Client_test.ETH_client()

WServer = test_server()
WClient = test_client()

if __name__ == '__main__':
    print('Start ETH-Test')
    WServer.start()
    print('Start Server')
    WClient.start()
    print('Start all Tasks')
    #WClient.join()
    #WServer.join()
