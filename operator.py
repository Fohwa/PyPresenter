import socket
from threading import Thread
import json
from pynput.keyboard import Key, Listener
from os import listdir
from os.path import isfile, join



# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1234 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

def listen_for_new_clients():
    while True:
        # we keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        # add the new connected client to connected sockets
        client_sockets.add(client_socket)
        # start a new thread that listens for each client's messages
        t = Thread(target=listen_for_client, args=(client_socket,))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()


x = Thread(target=listen_for_new_clients)
# make the thread daemon so it ends whenever the main thread ends
x.daemon = True
# start the thread
x.start()


# this code is from the old operator, connecting to its own server


# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
serverHost = "127.0.0.1"
serverPort = 1234 # server's port

# initialize TCP socket
sc = socket.socket()
print(f"[*] Connecting to {serverHost}:{serverPort}...")
# connect to the server
sc.connect((serverHost, serverPort))
print("[+] Connected.")

def listen_for_messages():
    while True:
        message = sc.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

def send(text):
    sc.send(text.encode())

def img():
        global i, z
        i = z = 0

        files = [f for f in listdir("assets")]


        def on_press(key):
            global i, z

# switch slides
            if str(key) == "Key.right" and i < len([f for f in listdir(f"assets/{files[z]}")]): i += 1; send(f"img:assets/{files[z]}/{i}.jpg")
            if str(key) == "Key.left": i -= 1 and i != 0 and i != 1; send(f"img:assets/{files[z]}/{i}.jpg")
# switch directories
            if str(key) == "Key.up" and z != 0: i = 0; z -= 1; print(files[z])
            if str(key) == "Key.down" and z < len(files): i = 0; z += 1; print(files[z])
# stop img mode
            if str(key) == "Key.esc": listener.stop(); return; exit()

        with Listener(on_press=on_press) as listener:
            listener.join()






while True:
    # input message we want to send to the server
    cmd = input("@ ")
    if cmd == "img": img()
    else:
        send("txt:" + cmd)
    
    

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()