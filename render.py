import pygame
from util import connection, presenter


Fps = 10

# init socket connection
client1 = connection.Client()
client1.connect()


def listen_for_messages(): # thread
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
        try:
            window.update(text)
        except: pass
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
            window.start()
            window.changeBackground()
            window.update("")

i = 0
run = True
while run:
    window = presenter.Window()
    window.clock.tick(Fps)

    listen_for_messages()
    