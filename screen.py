import pygame

# socket









# pygame
pygame.init()

Width, Height = 900, 500

Fps = 60

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("PyPresenter")
clock = pygame.time.Clock()


run = True
while run:
    clock.tick(60)


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()