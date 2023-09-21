# main.py
import pygame, sys, os, time, pandas
from level import Level
from menu import Menu, Button, displayText
from settings import *
from timer import Timer

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

timer = Timer()

if not "-c" in sys.argv:
    df = pandas.read_excel('./map.ods')
    df.to_csv('map.csv', header=False, index=False)

level = Level(screen, "./map.csv")
pygame.display.set_caption("")
pygame.mixer.music.set_volume(0.4)

bg = pygame.image.load("Graphics/Backgrounds/bg.png")
bgA = pygame.transform.scale(bg, (screenWidth, screenHeight))


# Music


# Fonction pour démarrer le jeu
def startGame():
    level.setupLevel()
    timer.start()
    run()


# cycle du jeu
def run():
    running = True
    pygame.mixer.music.load("Audio/game.mp3")
    pygame.mixer.music.play(-1)  # Le paramètre -1 indique de jouer en boucle
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause()
                timer.startTime = time.monotonic() - elapsed_time
            if not level.finish:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    level.setupLevel()
                    level.loose = True

        current_time = time.monotonic()
        elapsed_time = current_time - timer.startTime

        # Verification timer
        if timer.bestTime is None or level.finish:
            timer.update_best_time(elapsed_time)
            screen.set_alpha()
        elif level.loose:
            timer.start()
            level.loose = False

        screen.blit(bgA, (0, 0))
        level.run()
        # Affichage du temps
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
        screen.fill('black')
        displayText(screen, "Pause", 150, screenWidth // 2, 200, 'white')

        # Afficher le menu pause
        menuPause.displayButtons(screen)

        pygame.display.update()


# Fonction pour reprendre le jeu depuis la pause
def unpause():
    pass


def quitGame():
    mainMenu()


def quit():
    pygame.quit()
    sys.exit()


def mainMenu():
    running = True
    pygame.mixer.music.load("Audio/menu.mp3")
    pygame.mixer.music.play(-1)  # Le paramètre -1 indique de jouer en boucle
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
        displayText(screen, "Isaac Rush", 150, screenWidth // 2, 150, 'white')

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
