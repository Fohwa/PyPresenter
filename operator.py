import os
from functions import setResolution, closeSocket, killWindow, initNetwork, send, slide

# Networking:
SERVER_HOST, SERVER_PORT = "127.0.0.1", 1234

# starting client presenting window in another thread
# interface with user to get info to display
print("PyPresenter [Version 0.0.1]")
print("© All rights reserved.")
print("To start the window: 'win start'\n")
while True:
    ui = input("Ø ") # spacing char before every argument of the user
    if ui == "stop":
        killWindow()
        exit()
    elif ui == "win start" or ui == "win 1" or ui == "out 1": # starts output
        try:
            closeSocket()
        except:
            print("[@] first launch:")
        initNetwork(SERVER_HOST, SERVER_PORT)
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
    elif ui == "slide": slide()
    elif ui == "win restart":
        try:
            #closeSocket()
            killWindow()
            initNetwork()
        except: print("[x] Error: Could not restart Window; Try 'out 1'")
    elif ui[:4] == "cmd ": # redirects commands to render
        send("cmd", ui.removeprefix("cmd "))
        print("[+] command redirected")
    # send text to Window
    elif ui[:4] == "txt ": # redirects commands to render
        send("txt", ui.removeprefix("txt "))
        print("[+] text redirected")
    else:
        print("[x] Error: Command not found")
