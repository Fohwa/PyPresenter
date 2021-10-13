import pygame
import os
from threading import Thread
import socket

pygame.font.init()

# Display hight final is full screen, for debugging smaller
# Reading this info from /config/resolution.dat to change it

# Colors ; just yanked some from other project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font styles
NormalFont = pygame.font.SysFont('comicsans', 100)



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

    # Some important constants
    global Fps
    Fps = 10

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

# server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

s = socket.socket() # initialize TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # connect

def listen_for_messages():
    while True:
        global text
        text = s.recv(1024).decode()
        
# threading listening for messages
t = Thread(target=listen_for_messages)
t.daemon = True # daemon thread ends, when main ends
t.start()

# main function
init()
clock = pygame.time.Clock()
drawWindow("") # render it ones at the start
global text
text = ""
line = ""
i = 0
run = True
while run:
   clock.tick(Fps)

   try:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    # some console level interpretation of text:
    # I am using letters at the beginning to indicate, what to do with the message
    # standart syntax: "O: CMD" + u"\u0352" + TEXT + "+ u"\u0352"
    # CMDs: "txt": output line in TEXT to screen
    #       

    if text[:7] == "O: txt" + u"\u0352":
        isLine = False
        for i in text:
            if i == u"\u0352": isLine = True
            elif isLine: line += i
        drawWindow(line)
    elif text[:7] == "O: cmd" + u"\u0352":
        isLine = False
        for i in text:
            if i == u"\u0352": isLine = True
            elif isLine: line += i
        
        # line is command, see which one:
        if line == "stop": pygame.quit()


    line = ""
   except:
       exit()
