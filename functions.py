import socket
import os
import threading

# This funciton starts the render.py; this must happen in a function.
# otherwise it would be impossible to thread this task
def startRender(): os.system("python render.pyw")

# this funciton sets the resolution, by writing it to a file.
# this is a really bad way of doing it, but it works for now
# possible back and forth communication for render and operator could make this possible
# without a file
def setResolution(res):
    f = open(os.path.join('config', 'resolution.dat'), "w")
    f.write(res)
    f.close()

# initialises network conneciton to render.py
def initNetwork(SERVER_HOST, SERVER_PORT):
    global s
    global x
    global client_socket
    global client_address
    s = socket.socket() # create a TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make the port as reusable port
    s.bind((SERVER_HOST, SERVER_PORT)) # bind the socket to the address we specified
    s.listen(5) # listen for upcoming connections
    print(f"[*] TCP Socket initialised; Listening as {SERVER_HOST}:{SERVER_PORT}")

    x = threading.Thread(target=startRender)
    x.start()

    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")

def closeSocket():
    #close single client socket
    global client_socket
    global s
    client_socket.close()
    s.close()

def killWindow():
    try:
        line = "O: cmd" + u"\u0352" + "stop" + u"\u0352"
        client_socket.send(line.encode())
    except:
        print("[x] Error: Could not close window. Propaly already closed")

def send(prefix, message): # helper function to send messages to the render.py
    line = "O: " + prefix + u"\u0352" + message + u"\u0352"
    try: client_socket.send(line.encode())
    except: print("[x] Error: Could not talk to Window; Try 'out 1'")
    print(f"[+] {prefix} redirected")

def slide(): # the slide mode makes it easy to switch between text
    while True:
        ui = input("$ ")
        if ui == "stop": break
        send("txt", ui)