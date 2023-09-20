import pygame

class Menu:
    def __init__(self):
        self.buttons = []

    def addButton(self, button):
        self.buttons.append(button)

    def displayButtons(self, screen):
        for button in self.buttons:
            button.displayButton(screen)

class Button:
    def __init__(self, x, y, widthButton, heightButton, text, colorText, colorBackground, action=None):
        self.rect = pygame.Rect(x, y, widthButton, heightButton)
        self.text = text
        self.colorText = colorText
        self.colorBackground = colorBackground
        self.action = action

    def displayButton(self, screen):
        pygame.draw.rect(screen, self.colorBackground, self.rect)
        displayText(screen, self.text, 36, self.rect.centerx, self.rect.centery, self.colorText)

# Fonction pour afficher du texte sur l'écran
def displayText(screen, text, size, x, y, color):
    police = pygame.font.SysFont('Times New Roman', size)
    textSurface = police.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurface, textRect)