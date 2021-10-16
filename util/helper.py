from threading import Thread
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# helper functions which do just one thing

def threading(name: str, func):
    # start a thread
    name = Thread(target=func, name=name)
    # make the thread daemon so it ends whenever the main thread ends
    name.daemon = True
    # start the thread
    name.start()

def setResolution(res):
    f = open(os.path.join('config', 'resolution.dat'), "w")
    f.write(res)
    f.close()