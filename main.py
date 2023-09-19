# main.py
import pygame, sys
from level import Level
from settings import *
import pygame.mixer

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

#Temps
startTime = 0


level = Level(screen, "./map.csv")
pygame.display.set_caption("NOM DU JEU")
#son
pygame.mixer.init()
son = pygame.mixer.Sound("Audio/song.mp3")
son.set_volume(0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            son.stop()
            pygame.quit()
            sys.exit()

    screen.fill("black")
    if startTime is None or level.finish:
        startTime = pygame.time.get_ticks()
        level.finish = False
    level.run()
    son.play()

    font = pygame.font.Font(None, 36)
    current_time = pygame.time.get_ticks() - startTime
    current_time_str = f"Time: {current_time // 1000} s"
    #best_time_str = f"Best Time: {bestTime // 1000} s"
    current_time_text = font.render(current_time_str, True, "white")
    #best_time_text = font.render(best_time_str, True, "white")
    screen.blit(current_time_text, (10, 10))
    #screen.blit(best_time_text, (10, 50))


    pygame.display.update()
    clock.tick(60) # limiter à 60fps


