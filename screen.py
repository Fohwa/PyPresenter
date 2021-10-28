import pygame
import socket
from threading import Thread

message = ""

# socket
# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

def listen_for_messages():
    while True:
        global message
        message = s.recv(1024).decode()

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()


# # close the socket
# s.close()








# pygame
pygame.init()
WHITE = (255, 255, 255)

Width, Height = 900, 500

Fps = 60

# text stores value of current text on slide
text = text1 = text2 = ""
# mode is the mode of render, decides what layout the screen will have
mode = 1

# Font styles
pygame.font.init()
NormalFont = pygame.font.SysFont('comicsans', 100)
smallFont = pygame.font.SysFont('comicsans', 70)


screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("PyPresenter")
clock = pygame.time.Clock()

# just for testing
Background = pygame.transform.scale(pygame.image.load("assets/back.png"), (Width, Height))


# the part of actually bliting and updating the display
# is moved to a function to make it easier to switch modes
def render():
    # this functions gets different modes to decide what to project
    if mode == 0: pass #display nothing if mode is 0
    elif mode == 1: # one line mode
        global text
        screen.blit(Background, (0,0))
        line = NormalFont.render(text, 1, WHITE)
        screen.blit(line, (Width//2 - line.get_width()//2, Height//2 - line.get_height()//2))
    elif mode == 2: # two line mode
        distanz = 50
        global text1, text2
        screen.blit(Background, (0,0))
        line1 = NormalFont.render(text1, 1, WHITE)
        line2 = smallFont.render(text2, 1, WHITE) 
        screen.blit(line1, (Width//2 - line1.get_width()//2, Height//2 - distanz//2 - line1.get_height()//2))
        screen.blit(line2, (Width//2 - line2.get_width()//2, Height//2 + distanz//2 - line2.get_height()//2))
    


run = True
while run:
    clock.tick(60)
    render()
    if message[:4] == "txt:":
        text = message[4:]
        mode = 1
    if message[:4] == "cmd:":
        cmd = message[4:]
        if cmd == "stop": exit()
        if cmd[:5] == "mode:": mode == int(cmd[5:])
    if message[:4] == "tra:":
        text1 = message[4:]
        text2 = message[4:]
        mode = 2



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()