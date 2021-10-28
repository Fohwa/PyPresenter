import os
from util import functions, connection, helper

# starting client presenting window in another thread
# interface with user to get info to display
print("PyPresenter [Version 0.0.1]")
print("© All rights reserved.")
print("\n\n")

client = connection.Server()
client.start()
 
while True:
    ui = input("Ø ") # spacing char before every argument of the user
    if ui == "stop":
        client.sendAll("O: cmd" + u"\u0352" + "stop" + u"\u0352")
        exit()
    elif ui == "win stop" or ui == "out 0":
        try: client.sendAll("O: cmd" + u"\u0352" + "stop" + u"\u0352") 
        except: print("[x] Error: Could not restart Window; Try 'start'")#closeSocket()
        client.sendAll("O: cmd" + u"\u0352" + "stop" + u"\u0352")
    elif ui == "res":
        f = open(os.path.join('config', 'resolution.dat'), "r")
        print("Resolution: " + f.read())
        f.close()
    elif ui == "res fhd": helper.setResolution("1920:1080"), print("Resolution set to 1920 by 1080")# sets resolution
    elif ui == "res debug": helper.setResolution("900:500"), print("Resolution set to 900 by 500")
    elif ui == "res qhd": helper.setResolution("2560:1440"), print("Resolution set to 2560 by 1440")
    #elif ui == "slide": helper.slide()
    elif ui == "reconnect":
        try: client.listen() 
        except: pass
    elif ui == "clients":
        try: client.info()
        except: print("Error: No info")

    elif ui[:4] == "cmd ": # redirects commands to render
        client.send("cmd", ui.removeprefix("cmd "))
        print("[+] command redirected")
    # send text to Window
    elif ui[:4] == "txt ": # redirects commands to render
        client.send("txt", ui.removeprefix("txt "))
        print("[+] text redirected")
    else:
        print("[x] Error: Command not found")
