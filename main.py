# main.py
import pygame, sys
from level import Level
from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
level = Level(screen, "./map.csv")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("black")
    level.run()

    pygame.display.update()
    clock.tick(60) # limiter à 60fps