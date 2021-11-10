import threading
import Server_test
import Client_test
from concurrent import futures

print('Start main')

#WServer = threading.Thread(target=Server_test.server())
#WClient = threading.Thread(target=Client_test.testc())

e = futures.ThreadPoolExecutor(max_workers=2)

if __name__ == '__main__':
    print('Start ETH-Test')
    e.submit(Client_test.ETH_client())
    print('Start Client')
    e.submit(Server_test.ETH_server())
    print('Start all Tasks')
    #WServer.start()
    #WClient.start()
    #WClient.join()
    #WServer.join()
