# this is just some hidden stuff.
# only function visable to public should be send()
# not ideal, did not leran oop in Python jet...
# but should work for now to make it more understandable, as the codebase grows

from threading import Thread
import socket
import os # just for now to help debugging

global client_socket, client_sockets, client_address

# to be able to put renderThread into a different thread
def renderThread(): os.system("python render.py")

def startRender():
    # put render.py in different thread
    t = Thread(target=renderThread,)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
# initialises network conneciton to render.py

def initNetwork(SERVER_HOST, SERVER_PORT):
    global s, x, client_socket, client_address, client_sockets

    # initialize list/set of all connected client's sockets
    client_sockets = set()

    s = socket.socket() # create a TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make the port as reusable port
    s.bind((SERVER_HOST, SERVER_PORT)) # bind the socket to the address we specified
    s.listen(5) # listen for upcoming connections
    print(f"SERVER: [*] TCP Socket initialised; Listening as {SERVER_HOST}:{SERVER_PORT}")

    if input("start Render? [y/n]") == "y": startRender()
    
    # put the checking for new clients in different thread
    x = Thread(target=listenClient,)
    # make the thread daemon so it ends whenever the main thread ends
    x.daemon = True
    # start the thread
    x.start()




def listenClient(): # threading
    
    while True:
        # we keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"SERVER: [+] {client_address} connected.")
        # add the new connected client to connected sockets
        client_sockets.add(client_socket)
        print("Client socket remembered. Number of clients: " + str(len(client_sockets)))


def closeSocket(): # stop
    #close single client socket
    global client_socket, client_sockets, s
    
    # close client sockets
    for cs in client_sockets:
        cs.close()
    s.close() # close server side socket


def infoSocket():
    print("Info about the sockets connected:")
    for clientSocket in client_sockets:
        print(str(clientSocket))


# following functions can be used by other code
def sendClient(line):
    for client_socket in client_sockets:
            # send message to all clients
            client_socket.send(line.encode())



def start(SERVERHOST, SERVERPORT):
    initNetwork(SERVERHOST, SERVERPORT)