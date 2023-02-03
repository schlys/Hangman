from socket import *
import sys

if len(sys.argv) != 3 :
    print('ERROR: Invalid number of command line arguments')
    sys.exit('Usage: python3 client.py <port number> <host name>')

serverPort = int(sys.argv[1])
serverName = sys.argv[2]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
confirm = clientSocket.recv(1024).decode()
print(f'Connected to {confirm}\n')

command = input('Input server command: ').upper()
while command != 'LEAVE':

   
    clientSocket.send(command.encode())
    msg = clientSocket.recv(1024).decode()
    print(msg)
    if msg == 'RESTART':
        command = 'test'
        pass

    command = input('\nInput server command: ').upper()

print('\n\nShutting down client...')
clientSocket.send(command.encode())
clientSocket.close()
print('Client closed successfully')
    
