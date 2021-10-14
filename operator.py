import os
from util import functions
from util import server
import time

# Networking:
SERVER_HOST, SERVER_PORT = "127.0.0.1", 1234

# starting client presenting window in another thread
# interface with user to get info to display
print("PyPresenter [Version 0.0.1]")
print("© All rights reserved.")
print("To start the window: 'start'\n")
while True:
    ui = input("Ø ") # spacing char before every argument of the user
    if ui == "stop":
        functions.killWindow()
        exit()
    elif ui == "start": # starts output
        print("[@] first launch:")
        server.start(SERVER_HOST, SERVER_PORT)
        time.sleep(1)
    elif ui == "out": functions.send("cmd", "start")
    elif ui == "win stop" or ui == "out 0":
        try: functions.killWindow() 
        except: print("[x] Error: Could not restart Window; Try 'start'")#closeSocket()
        functions.killWindow()
    elif ui == "res":
        f = open(os.path.join('config', 'resolution.dat'), "r")
        print("Resolution: " + f.read())
        f.close()
    elif ui == "res fhd": functions.setResolution("1920:1080"), print("Resolution set to 1920 by 1080")# sets resolution
    elif ui == "res debug": functions.setResolution("900:500"), print("Resolution set to 900 by 500")
    elif ui == "res qhd": functions.setResolution("2560:1440"), print("Resolution set to 2560 by 1440")
    elif ui == "slide": functions.slide()
    elif ui == "reconnect":
        try: server.listenClient()
        except: pass
    elif ui == "clients":
        try: server.infoSocket()
        except: print("Error: No info")
    elif ui == "win restart":
        try:
            #closeSocket()
            functions.killWindow()
            server.start()
        except: print("[x] Error: Could not restart Window; Try 'out 1'")
    elif ui[:4] == "cmd ": # redirects commands to render
        functions.send("cmd", ui.removeprefix("cmd "))
        print("[+] command redirected")
    # send text to Window
    elif ui[:4] == "txt ": # redirects commands to render
        functions.send("txt", ui.removeprefix("txt "))
        print("[+] text redirected")
    else:
        print("[x] Error: Command not found")
