import pygame
import os
from threading import Thread
from util import helper, connection, presenter

print("\nRender started")

# pygame.font.init()

# Display hight final is full screen, for debugging smaller
# Reading this info from /config/resolution.dat to change it

Fps = 10

# # Font styles
# NormalFont = pygame.font.SysFont('comicsans', 100)


# def init():
    
#     global Width, Height
#     [Width, Height] = presenter.resolution()

#     # init the display
#     global Win
#     Win = pygame.display.set_mode((Width, Height))
#     pygame.display.toggle_fullscreen
#     pygame.display.set_caption("PyPresenter")

#     # function to load Assets for background
#     #def loadAsset(name): # for now the location of the Assets folder is hard coded
#     global Background
#     Background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'back.jpg')), (Width, Height))

#     # needs to be changed to be able to use different styles
# def drawWindow(text):
#     global Win
#     global Background
#     Win.blit(Background, (0,0))
#     lyric = NormalFont.render(text, 1, helper.WHITE)
#     Win.blit(lyric, (Width//2 - lyric.get_width()//2, Height//2 - lyric.get_height()//2))

#     pygame.display.update()

client1 = connection.Client()
client1.connect()


def listen_for_messages(): # thread
    while True:
        line = client1.s.recv(1024).decode()
        # some console level interpretation of text:
        # I am using letters at the beginning to indicate, what to do with the message
        # standart syntax: "O: CMD" + u"\u0352" + TEXT + "+ u"\u0352"
        # CMDs: "txt": output line in TEXT to screen
        #       

        text = ""
        if line[:7] == "O: txt" + u"\u0352":
            isLine = False
            for i in line:
                if i == u"\u0352": isLine = True
                elif isLine: text += i
            window.update(text)
        elif line[:7] == "O: cmd" + u"\u0352":
            isLine = False
            for i in line:
                if i == u"\u0352": isLine = True
                elif isLine: text += i

            # line is command, see which one:
            if text == "stop": pygame.quit()
            elif text == "start":
                print("Render: start to render")
                #init()
                window = presenter.Window()
                window.changeBackground()
                window.update("")

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
           client1.close()
   
    except: pass