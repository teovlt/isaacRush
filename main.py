import pygame as pg

# Initialisation de Pygame
pg.init()

# Définir les dimensions de la fenêtre
widthScreen, heightScreen = 1280, 720
screen = pg.display.set_mode((widthScreen, heightScreen))
pg.display.set_caption("Menu Mystère")

# Classe pour représenter un bouton
class Button():
    def __init__(self, x, y, widthButton, heightButton, text, colorText, colorBackground, action=None):
        self.rect = pg.Rect(x, y, widthButton, heightButton)
        self.text = text
        self.colorText = colorText
        self.colorBackground = colorBackground
        self.action = action

    def displayButton(self, screen):
        pg.draw.rect(screen, self.colorBackground, self.rect)
        displayText(self.text, 36, self.rect.centerx, self.rect.centery, self.colorText)

# Classe pour représenter le menu
class Menu():
    def __init__(self):
        self.buttons = []

    def addButton(self, button):
        self.buttons.append(button)

    def displayButton(self, screen):
        for button in self.buttons:
            button.displayButton(screen)

# Fonction pour afficher du texte sur l'écran
def displayText(text, size, x, y, color):
    police = pg.font.SysFont('Times New Roman', size)
    textSurface = police.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurface, textRect)

# Action à effectuer lorsque le bouton "Jouer" est cliqué
def actionPlay():
    startGame()  # Lancer la fonction pour démarrer le jeu

def actionResume():
    unpause()

# Action à effectuer lorsque le bouton "Quitter" est cliqué
def actionQuit():
    mainMenu()

# Fonction pour démarrer le jeu
def startGame():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                quit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pause()

        # Code de jeu va ici

        # Afficher le titre du jeu pendant le jeu
        screen.fill('black')
        displayText("Jeu en cours...", 100, widthScreen // 2, heightScreen // 2, 'white')

        # Mettre à jour l'affichage
        pg.display.flip()

    pg.quit()

menuPause = Menu()
buttonResume = Button(widthScreen // 2 - 150, heightScreen // 2 - 50, 300, 75, "Reprendre", 'black', 'white', actionResume)
buttonQuit = Button(widthScreen // 2 - 150, heightScreen // 2 + 50, 300, 75, "Quitter", 'black', 'white', actionQuit)
menuPause.addButton(buttonResume)
menuPause.addButton(buttonQuit)

def pause():
    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = False  # Mettre paused à False pour reprendre le jeu
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in menuPause.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.action:
                                button.action()
                                paused = False 
        screen.fill('#ffffff')
        displayText("Pause", 150, widthScreen // 2, 200, 'black')

        # Afficher le menu pause
        menuPause.displayButton(screen)

        pg.display.update()


# Fonction pour reprendre le jeu depuis la pause
def unpause():
    # Efface le menu pause
    screen.fill('black')

    # Reprend le jeu
    startGame()


def mainMenu():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in menu.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.action:
                                button.action()

        # Effacer l'écran
        screen.fill('black')

        # Afficher le titre du jeu dans le menu
        displayText("Menu Mystère", 100, widthScreen // 2, 150, 'white')

        # Afficher le menu
        menu.displayButton(screen)

        # Mettre à jour l'affichage
        pg.display.flip()

# Créer le menu et les boutons
menu = Menu()
buttonPlay = Button(widthScreen // 2 - 150, heightScreen // 2, 300, 75, "Jouer", 'black', 'white', actionPlay)
menu.addButton(buttonPlay)

# Démarrer le menu principal
mainMenu()