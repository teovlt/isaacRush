# main.py
import pygame, sys
from level import Level
from settings import *
import pygame.mixer
from timer import Timer

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

timer = Timer()

level = Level(screen, "./map.csv")
pygame.display.set_caption("NOM DU JEU")
#son
pygame.mixer.init()
pygame.mixer.music.load("Audio/3.mp3")
pygame.mixer.music.play(-1)  # Le paramètre -1 indique de jouer en boucle

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")

    #Verification timer
    current_time = pygame.time.get_ticks() - timer.startTime
    if timer.bestTime is None or level.finish:
        timer.start()
        timer.update_best_time(current_time)
        level.finish = False

    if level.loose:
        timer.start()
        level.loose = False


    level.run()
    current = timer.drawCurrent()
    best = timer.drawBest()
    screen.blit(current, (10, 10))
    screen.blit(best, (10, 50))


    pygame.display.update()
    clock.tick(60) # limiter à 60fps


