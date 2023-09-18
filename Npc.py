import pygame


class Npc():

    def __init__(self):
        self.__init__()
        self.image = pygame.image.load("Assets/Npc's/npc.png", "image")
        self.rect = self.image.get_rect()
