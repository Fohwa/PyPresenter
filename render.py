import pygame
import os
import socket
from threading import Thread
import time

from util import server

print("\nRender started")

pygame.font.init()

# Display hight final is full screen, for debugging smaller
# Reading this info from /config/resolution.dat to change it

# Colors ; just yanked some from other project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
Fps = 10
PygameRunning = False

# Font styles
NormalFont = pygame.font.SysFont('comicsans', 100)

# socket connection
# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message


def init():
    f = open(os.path.join('config', 'resolution.dat'))
    resolution = f.readline()
    x = y = ""
    isY = False
    for i in resolution:
        if i == ":": isY = True
        else:
            if isY: y += i
            else: x += i
    
    global Width, Height
    Width = int(x)
    Height = int(y)

    # init the display
    global Win
    Win = pygame.display.set_mode((Width, Height))
    pygame.display.toggle_fullscreen
    pygame.display.set_caption("PyPresenter")

    # function to load Assets for background
    #def loadAsset(name): # for now the location of the Assets folder is hard coded
    global Background
    Background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'back.jpg')), (Width, Height))

    # needs to be changed to be able to use different styles
def drawWindow(text):
    global Win
    global Background
    Win.blit(Background, (0,0))
    lyric = NormalFont.render(text, 1, WHITE)
    Win.blit(lyric, (Width//2 - lyric.get_width()//2, Height//2 - lyric.get_height()//2))

    pygame.display.update()

# main function
print("\nRender: main function started")
# initialize TCP socket
s = socket.socket()
print(f"CLIENT: [*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
connected = False
while not connected:
    try: 
        s.connect((SERVER_HOST, SERVER_PORT))
        print("CLIENT: [+] Connected.")
        connected = True
    except:
        print("Server not found. Trying again...")
        time.sleep(5)


def listen_for_messages(): # thread
    while True:
        line = s.recv(1024).decode()
        # some console level interpretation of text:
        # I am using letters at the beginning to indicate, what to do with the message
        # standart syntax: "O: CMD" + u"\u0352" + TEXT + "+ u"\u0352"
        # CMDs: "txt": output line in TEXT to screen
        #       

        print(line)
        text = ""
        if line[:7] == "O: txt" + u"\u0352":
            isLine = False
            for i in line:
                if i == u"\u0352": isLine = True
                elif isLine: text += i
            drawWindow(text)
        elif line[:7] == "O: cmd" + u"\u0352":
            isLine = False
            for i in line:
                if i == u"\u0352": isLine = True
                elif isLine: text += i

            # line is command, see which one:
            if text == "stop": pygame.quit()
            elif text == "start":
                print("Render: start to render")
                init()
                drawWindow("")

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
print("Render: listen for messages is threaded")

while True:
    try:
        clock = pygame.time.Clock()
        i = 0
        run = True
        while run:
           clock.tick(Fps)
           try:
               for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()


            


           except:
            exit()
           server.closeSocket()
   
    except: pass