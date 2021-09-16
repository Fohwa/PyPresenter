import socket
import os
import threading

# Networking:
SERVER_HOST, SERVER_PORT = "127.0.0.1", 1234
separator_token = "<SEP>" # used to separate the client name & message

# starting client presenting window in another thread
def startRender(): os.system("python render.pyw")

def setResolution(res):
    f = open(os.path.join('config', 'resolution.dat'), "w")
    f.write(res)
    f.close()


def initNetwork():
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

# interface with user to get info to display
print("PyPresenter [Version 0.0.1]")
print("© All rights reserved.")
print("To start the window: 'win start'\n")
while True:
    ui = input("$ ")
    if ui == "stop":
        killWindow()
        exit()
    elif ui == "win start" or ui == "win 1" or ui == "out 1": # starts output
        try:
            closeSocket()
        except:
            print("[@] first launch:")
        initNetwork()
    elif ui == "win stop" or ui == "out 0":
        try: killWindow() 
        except: print("[x] Error: Could not restart Window; Try 'out 1'")#closeSocket()
        killWindow()
    elif ui == "res":
        f = open(os.path.join('config', 'resolution.dat'), "r")
        print("Resolution: " + f.read())
        f.close()
    elif ui == "res fhd": setResolution("1920:1080"), print("Resolution set to 1920 by 1080")# sets resolution
    elif ui == "res debug": setResolution("900:500"), print("Resolution set to 900 by 500")
    elif ui == "res qhd": setResolution("2560:1440"), print("Resolution set to 2560 by 1440")
    elif ui == "win restart":
        try:
            #closeSocket()
            killWindow()
            initNetwork()
        except: print("[x] Error: Could not restart Window; Try 'out 1'")
    elif ui[:4] == "cmd ": # redirects commands to render
        send("cmd", ui.removeprefix("cmd "))
    # send text to Window
    elif ui[:4] == "txt ": # redirects commands to render
        send("txt", ui.removeprefix("txt "))
    else:
        print("[x] Error: Command not found")
