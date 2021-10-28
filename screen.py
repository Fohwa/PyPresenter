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

# Font styles
pygame.font.init()
NormalFont = pygame.font.SysFont('comicsans', 100)


screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("PyPresenter")
clock = pygame.time.Clock()

# just for testing
Background = pygame.transform.scale(pygame.image.load("assets/back.png"), (Width, Height))


run = True
while run:
    clock.tick(60)
    screen.blit(Background, (0,0))
    if message[:4] == "txt:":
        text = message[4:]
        line = NormalFont.render(text, 1, WHITE)
        screen.blit(line, (Width//2 - line.get_width()//2, Height//2 - line.get_height()//2))
    if message[:4] == "cmd:":
        text = message[4:]
        if text == "stop": exit()



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()