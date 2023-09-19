# main.py
import pygame, sys
from settings import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

while True:
    for event in pygame.eveng.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill("black")

    pygame.display.update()
    clock.tick(60) # limiter à 60fps