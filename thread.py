from _thread import *
from threading import Thread
from hangman import *
from datetime import *

class ClientThread(Thread):

    def __init__(self, connectionSocket, address, serverName, serverPort, queue=None):
        Thread.__init__(self)
        self.connectionSocket = connectionSocket
        self.address = address
        self.queue = queue
        self.serverName = serverName
        self.serverPort = serverPort
    
    def exit(self, command):
        if self.queue:
            self.queue.get_nowait()
        self.connectionSocket.sendall(command.encode())
        self.connectionSocket.close()

    def sendReceive(self, msg):
        self.connectionSocket.send(msg.encode())
        return self.connectionSocket.recv(1024).decode().split()

    def toGuess(self, word, mistakes=0):
        ret = ''.join(part for part in HANGMAN[mistakes]) + '\n'
        for x in range(0, len(word)):
            ret += word[x]
            ret += ' '
        ret += '\nGuess the word or a letter'
        return ret

    def run(self):
        #------------------------add to thread queue---------------------#
        if self.queue:
            self.queue.put(1)

        while True:
            print(f'\nConnection from {self.address} has been established!\n')

            confirm = f'{self.serverName} on port {self.serverPort}'
            self.connectionSocket.send((confirm + '\n\nList of commands:\nPLAY\nLEAVE\n').encode())
            restart = False

            while True:
                if not restart:
                    command = self.connectionSocket.recv(1024).decode().split()
                    print(f'{datetime.now()} Command Entered: {command}\n')

                # ---------------------------- start game --------------------------#
                if command[0] == 'PLAY' or restart:
                    playMsg = '\nPLAY commands:\nGUESS <letter>/<word>\nPREV_GUESS\nRESTART\n'
                    restart = False
                               
                    #----------------- get a random word to guess----------------------------#
                    word = getWord()
                    while not word:
                        word = getWord()

                    word = word.upper()
                    print(f'Word to guess is: {word}')

                    #-----------------------create list to hold user guessed chars-----------------#
                    guessed = ['_'] * len(word)

                    previousGuesses = []
                    userGuess = []
                    mistakes = 0
                    clientMsg = ''
                    guess = ''
                    guessMsg = self.toGuess(guessed)
                    self.connectionSocket.send((playMsg + '\n' + guessMsg).encode())

                    while guess != word and mistakes < 6:

                        guessMsg = self.toGuess(guessed, mistakes)

                        userGuess = self.connectionSocket.recv(1024).decode().split()
                        print(f'\n{datetime.now()} Command Entered: {userGuess}')
                        
                        if userGuess[0] == 'GUESS':

                            while len(userGuess) != 2:
                                userGuess = self.sendReceive('\nERROR: Invalid GUESS usage\nUsage: "GUESS <word>" or "GUESS <letter>"')
                                if userGuess[0] == 'LEAVE':
                                    self.exit('LEAVE')
                                    return

                            guess = userGuess[1]
                            previousGuesses.append(guess)
                            if guess != word and ((len(guess) == 1 and guess not in word) or (len(guess) > 1 and guess != word)):
                                mistakes += 1

                            if len(guess) == 1:                                
                                for char in range(0, len(word)):
                                    if guess == word[char]:
                                        guessed[char] = word[char]
                            
                            clientMsg = '\n' + self.toGuess(guessed, mistakes)
                            
                        elif userGuess[0] == 'PREV_GUESS':
                            clientMsg = 'Previous Guesses: ' + ', '.join(guess for guess in previousGuesses)
                        elif userGuess[0] == 'LEAVE':
                            self.exit('LEAVE')
                            return
                        elif userGuess[0] == 'RESTART':
                            clientMsg = 'RESTART'
                            restart = True
                            break
                        else:
                            clientMsg = '\nERROR: Invalid input\n' + playMsg + '\n'+self.toGuess(guessed, mistakes)
                            
                        self.connectionSocket.send(clientMsg.encode())

                    winLose = '\n'
                    if mistakes < 6 and not restart:
                        winLose += f'Nice! You won with {mistakes} mistakes.'
                        self.connectionSocket.send(winLose.encode())
                    elif not restart:
                        winLose += ''.join(part for part in HANGMAN[6]) + f'\n\nYou lose! the word was {word}'
                        self.connectionSocket.send(winLose.encode())
                 

                elif command[0] == 'LEAVE':
                    self.exit('LEAVE')
                    return
                else:
                    self.connectionSocket.send(('\nERROR: Invalid command entered\n\nList of commands:\nPLAY\nLEAVE\n').encode())