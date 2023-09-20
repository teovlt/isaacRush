# main.py
import pygame
import sys
from level import Level
from menu import Menu, Button, displayText
from settings import *
from timer import Timer
import time
import pandas as pd

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

timer = Timer()

df = pd.read_excel('map.ods')
df.to_csv('map.csv', header=False, index=False)
level = Level(screen, "./map.csv")
pygame.display.set_caption("")
# bg = pygame.image.load("Graphics/Backgrounds/RTB_v1.0/background.png")
# bg2 = pygame.image.load("Graphics/Backgrounds/RTB_v1.0/background2.png")
# bg3 = pygame.image.load("Graphics/Backgrounds/RTB_v1.0/background3.png")
# bg4 = pygame.image.load("Graphics/Backgrounds/RTB_v1.0/background4.png")
# bgA = pygame.transform.scale(bg, (1280, 720))
# bgB = pygame.transform.scale(bg2, (1280, 720))
# bgC = pygame.transform.scale(bg3, (1280, 720))
# bgD = pygame.transform.scale(bg3, (1280, 720))
# Music
pygame.mixer.music.load("Audio/3.mp3")
pygame.mixer.music.play(-1)  # Le paramètre -1 indique de jouer en boucle


# Fonction pour démarrer le jeu
def startGame():
    level.setupLevel()
    run()


# cycle du jeu
def run():
    running = True
    timer.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause()
                timer.startTime = time.monotonic() - elapsed_time
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                level.setupLevel()
                level.loose = True

        current_time = time.monotonic()
        elapsed_time = current_time - timer.startTime

        # Verification timer
        if timer.bestTime is None or level.finish:
            timer.start()
            timer.update_best_time(elapsed_time)
            level.finish = False
            timer.update_best_time(elapsed_time)
        elif level.loose:
            timer.start()
            level.loose = False

        screen.fill('black')
        # screen.blit(bgA,(0, 0))
        # screen.blit(bgB,(0, 0))
        # screen.blit(bgC,(0, 0))
        # screen.blit(bgD,(0, 0))
        level.run()
        #Affichage du temps
        current = timer.drawCurrent(elapsed_time)
        best = timer.drawBest()
        screen.blit(current, (10, 10))
        screen.blit(best, (10, 50))

        pygame.display.update()
        clock.tick(60)  # limiter à 60fps

    pygame.quit()


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Mettre paused à False pour reprendre le jeu

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in menuPause.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.action:
                                button.action()
                                paused = False
        screen.fill('#ffffff')
        displayText(screen, "Pause", 150, screenWidth // 2, 200, 'black')

        # Afficher le menu pause
        menuPause.displayButtons(screen)

        pygame.display.update()


# Fonction pour reprendre le jeu depuis la pause
def unpause():
    # Efface le menu pause
    screen.fill('black')

    # Reprend le jeu
    run()


def resume():
    unpause()


def quitGame():
    mainMenu()


def quit():
    pygame.quit()
    sys.exit()


def mainMenu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in menu.buttons:
                    if button.rect.collidepoint(event.pos) and button.action:
                        button.action()

        # Effacer l'écran
        screen.fill('black')

        # Afficher le titre du jeu dans le menu
        displayText(screen, "Menu Mystère", 150, screenWidth // 2, 150, 'white')

        # Afficher le menu
        menu.displayButtons(screen)

        # Mettre à jour l'affichage
        pygame.display.flip()


# Créer le menu principal et ses boutons
menu = Menu()
buttonPlay = Button(screenWidth // 2 - 150, screenHeight // 2 - 70, 300, 75, "Jouer", 'black', 'white', startGame)
menu.addButton(buttonPlay)  #  Ajoute le bouton au menu
buttonQuit = Button(screenWidth // 2 - 150, screenHeight // 2 + 70, 300, 75, "Quitter", 'black', 'white', quit)
menu.addButton(buttonQuit)  #  Ajoute le bouton au menu

# Créer le menu pause et ses boutons
menuPause = Menu()
buttonResume = Button(screenWidth // 2 - 150, screenHeight // 2 - 50, 300, 75, "Reprendre", 'black', 'white', unpause)
menuPause.addButton(buttonResume)  #  Ajoute le bouton au menu
buttonQuit = Button(screenWidth // 2 - 150, screenHeight // 2 + 50, 300, 75, "Quitter", 'black', 'white', quitGame)
menuPause.addButton(buttonQuit)  #  Ajoute le bouton au menu

# Démarrer le menu principal
mainMenu()
