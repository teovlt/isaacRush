import pygame, sys
from level import Level
from settings import *
from menu import *

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
level = Level(screen, "./map.csv")

# Fonction pour démarrer le jeu
def startGame():
    level.setupLevel("./map.csv")
    run()

# cycle du jeu
def run():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        # Code de jeu va ici
        screen.fill('black')
        level.run()

        pygame.display.update()
        clock.tick(60) # limiter à 60fps

    pygame.quit()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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

def quit():
    mainMenu()

def mainMenu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in menu.buttons:
                    if button.rect.collidepoint(event.pos) and button.action:
                        button.action()

        # Effacer l'écran
        screen.fill('black')

        # Afficher le titre du jeu dans le menu
        displayText(screen, "Menu Mystère", 100, screenWidth // 2, 150, 'white')

        # Afficher le menu
        menu.displayButtons(screen)

        # Mettre à jour l'affichage
        pygame.display.flip()

# Créer le menu et les boutons
menu = Menu()
buttonPlay = Button(screenWidth // 2 - 150, screenHeight // 2, 300, 75, "Jouer", 'black', 'white', startGame)
menu.addButton(buttonPlay)

# Créer le menu pause et les boutons
menuPause = Menu()
buttonResume = Button(screenWidth // 2 - 150, screenHeight // 2 - 50, 300, 75, "Reprendre", 'black', 'white', resume)
buttonQuit = Button(screenWidth // 2 - 150, screenHeight // 2 + 50, 300, 75, "Quitter", 'black', 'white', quit)
menuPause.addButton(buttonResume)
menuPause.addButton(buttonQuit)

# Démarrer le menu principal
mainMenu()