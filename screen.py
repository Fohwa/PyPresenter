import json
import pygame
import socket
from threading import Thread

# reading settings from sreenMeta.json

f = open("screenMeta.json", "r")
data = f.read()
f.close()

data = json.loads(data)

mode = ""
imglocation = "assets/black.png"

# socket
# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = data['Network']['SERVER_HOST'] # get ip from meta json
SERVER_PORT = data['Network']['SERVER_PORT'] # server's port

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

def listen_for_messages():
    global slide
    while True:
        message = s.recv(1024).decode()

        if message == "mode:img": global mode; mode = "img"
        elif message == "mode:slide": mode = "slide"

        elif message == "stop": exit()
        
        elif mode == "img":
            global imglocation
            imglocation = message
            
        else: slide = json.loads(message)



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

Width, Height = data['Screen']['Resolution']['Width'], data['Screen']['Resolution']['Heigth'] 

Fps = 60


# Font styles
pygame.font.init()
NormalFont = pygame.font.SysFont('comicsans', 100)
smallFont = pygame.font.SysFont('comicsans', 70)


screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("PyPresenter")
clock = pygame.time.Clock()

# the part of actually bliting and updating the display
# is moved to a function to make it easier to switch modes
def render():
        if mode == "img":
            global imglocation
            try:
                Background = pygame.transform.scale(pygame.image.load(imglocation), (Width, Height))
            except: pass
            screen.blit(Background, (0,0))
        else:
        
            # background layer
            Background = pygame.transform.scale(pygame.image.load(data['Background']['imgLocation']), (Width, Height))
            screen.blit(Background, (0,0))
            # slide layer
            try:
                for object in slide['Slide']['objects']:
                    line = NormalFont.render(object['txt'], 1, object['txtcolor'])
                    screen.blit(line, (Width//2 - line.get_width()//2, Height//2 - line.get_height()//2))
            except: pass

run = True
while run:
    clock.tick(60)
    render()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()