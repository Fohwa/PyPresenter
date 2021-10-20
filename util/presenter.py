import os
import pygame

# some constant colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def resolution():
    f = open(os.path.join('config', 'resolution.dat'))
    a = f.readline()
    f.close()
    x = y = ""
    isY = False
    for i in a:
        if i == ":": isY = True
        else:
            if isY: y += i
            else: x += i
    
    return [int(x), int(y)]


class Window:

    def __init__(self, name="PyPresenter"):
        # get resolution from function resolution()
        self.Width, self.Height = resolution()
        self.name = name
        self.backgroundLocation = os.path.join("Assets", "Background", "back.jpg")

        # Font styles
        pygame.font.init()
        self.NormalFont = pygame.font.SysFont('comicsans', 100)

        # clock
        self.clock = pygame.time.Clock()



    def start(self):
        # init the window
        self.Win = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.toggle_fullscreen
        pygame.display.set_caption(self.name)

    def changeBackground(self):
        self.Background = pygame.transform.scale(pygame.image.load(self.backgroundLocation), (self.Width, self.Height))

    def changeBackgroundLocation(self, location):
        self.backgroundLocation = os.path.join("Assets", "Background", location)

        # init basicly:
        # window = presenter.Window()
        # changeBackground()


    def update(self, text): # not updated, needs changes for different templates

        self.Win.blit(self.Background, (0,0))
        line = self.NormalFont.render(text, 1, WHITE)
        self.Win.blit(line, (self.Width//2 - line.get_width()//2, self.Height//2 - line.get_height()//2))

        pygame.display.update()
        