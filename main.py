import pygame
import random

pygame.init()

main_window = pygame.display.set_mode((1000,750), pygame.RESIZABLE)
clocky = pygame.time.Clock()

running = True
while running:

    clocky.tick(40)

    main_window.fill((random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))
    pygame.display.flip()
    