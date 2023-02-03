from socket import *
from datetime import *
from _thread import *
from queue import Queue
from thread import *
import sys
import select

#-------------------Server Code----------------------------------#
def acceptClient():
    connectionSocket, address = serverSocket.accept()
    ClientThread(connectionSocket, address, serverName, serverPort, threadQueue).start()

# serverName = gethostname()
#serverName = gethostbyname(gethostname())
serverName = '127.0.0.1'
#serverName = '0.0.0.0'


if len(sys.argv) != 2 :
    print('ERROR: Invalid number of command line arguments\n')
    sys.exit('Usage: python3 server.py <port number>')

serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(2)

print(f'{datetime.now()} {serverName} starting on port {serverPort}')

rlist = [serverSocket]
threadQueue = Queue()

acceptClient()
while not threadQueue.empty():
    
    server_ready, _, _ = select.select(rlist,[],[], .25)
    if serverSocket in server_ready:
        acceptClient()
    
print('\nShutting down gracefully...')
serverSocket.close()
print('Server closed successfully')
       

