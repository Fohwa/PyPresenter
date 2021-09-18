from pynput.keyboard import Key, Listener
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

def slide(): # the slide mode makes it easy to switch between text
    location = input("please insert the file name: ")

    try:
     # open file with lyrics
     f = open(os.path.join('lyrics/', location + ".txt"))
     
     global lyrics
     lyrics = f.read().splitlines() #puts the file into an array
     global line
     line = 0
     GoNextSlide()
     line += 1
     KeyLog()

    except: print("Could not open file")

def on_press(key):

    global line
    if key == Key.space: GoNextSlide(); line += 1
    if key == Key.right: GoNextSlide(); line += 1
    if key == Key.esc: print("should stop now"), exit()
    #TODO: make these buttons work
    #if key == "f": print("F"); send("txt", "")
    #if key == Key.left: line -= 2; GoNextSlide; line += 1
    else: pass
    
def KeyLog():
# Collect events until released
    with Listener(
           on_press=on_press,
           ) as listener:
        listener.join()

def GoNextSlide():
    # swich text from next to this slide
    global line, lyrics
    thisSlide = lyrics[line]
    # save text of next slide to string
    
    try:
        nextSlide = lyrics[line + 1]
    except:
        print("Song ended")
        send("txt", "")
        exit()
    # print current and next Slide text
    print(f"\n-------------------------------------------------------<{line + 1}/{len(lyrics)}>")
    print("Current: | " + thisSlide)
    print("Next:    | " + nextSlide)
    send("txt", thisSlide)

