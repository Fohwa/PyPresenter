import socket
from time import sleep
import os
from threading import Thread


class Client:
    # socket connection
    # server's IP address
    # if the server is not on this machine, 
    # put the private (network) IP address (e.g 192.168.1.2)
    def __init__(self):
        self.SERVER_HOST = "127.0.0.1"
        self.SERVER_PORT = 1234
        
        # initialize TCP socket
        self.s = socket.socket()

    
    
    def connect(self):
        print(f"CLIENT: [*] Connecting to {self.SERVER_HOST}:{self.SERVER_PORT}...")
        # connect to the server
        connected = False
        while not connected:
            try: 
                self.s.connect((self.SERVER_HOST, self.SERVER_PORT))
                print("CLIENT: [+] Connected.")
                connected = True
            except:
                print("Server not found. Trying again...")
                sleep(5)


class Server:
    def __init__(self):
        self.SERVER_HOST = "127.0.0.1"
        self.SERVER_PORT = 1234

        self.s = socket.socket() # creates a TCP socket
        # make port reusable
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to address
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        # listen for upcoming connections
        self.s.listen(5)

        print(f"[*] TCP Socket initialised; Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")

        self.clientSocket = None
        self.clientSockets = set()
        self.clientAddress = None
    

    def listen(self): # for threading #pre listenClient()
        
        while True:
            # we keep listening for new connections all the time
            self.clientSocket, self.clientAddress = self.s.accept()
            print(f"SERVER: [+] {self.clientAddress} connected.")
            # add the new connected client to connected sockets
            self.clientSockets.add(self.clientSocket)
            print("Client socket remembered. Number of clients: " + str(len(self.clientSockets)))

    def start(self): #pre start()
 
        # start a thread
        t = Thread(target=self.listen, name="listenServer")
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()
 

    def send(self, prefix, message):
        line = "O: " + prefix + u"\u0352" + message + u"\u0352"
        try:
            for cs in self.clientSockets:
                # send messages to all clients
                cs.send(line.encode())
        except: print("[x] Error: Could not talk to Window; start renderer")

    def info(self): #pre infoSocket()
        print("Info about the clients connected")
        for cs in self.clientAddress:
            print(str(cs))

    def close(self): # pre closeSocket()
        for cs in self.clientSockets:
            cs.close()
        self.s.close()

    