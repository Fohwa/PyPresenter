import pygame
from util import connection, presenter


client1 = connection.Client()
client1.connect()


window = presenter.Window()
window.changeBackground()
window.update("")

window.Fps = 60
window.startGameLoop()

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
                        