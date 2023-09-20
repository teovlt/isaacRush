import pygame as pg
import game

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

# Boucle de jeu
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in menu.buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.action:
                            button.action()


    # Action à effectuer lorsque le bouton "Jouer" est cliqué
    def actionPlay():
        game.Game()  # Exécute la fonction principale du module de jeu


    # Créer le menu et les boutons
    menu = Menu()

    buttonPlay = Button(widthScreen // 2 - 150, heightScreen // 2, 300, 75, "Jouer", 'black', 'white', actionPlay)
    menu.addButton(buttonPlay)

    #buttonSettings = Button(widthScreen/2-100, heightScreen/2, 200, 50, "Options", 'black', 'white')
    #menu.addButton(buttonSettings)



    # Effacer l'écran
    screen.fill('black')

    # Afficher le titre du jeu
    displayText("Menu Mystère", 100, widthScreen // 2, 150, 'white')

    # Afficher le menu
    menu.displayButton(screen)

    # Mettre à jour l'affichage
    pg.display.flip()

# Quitter Pygame
pg.quit()