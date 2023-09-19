# tile.py
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
        self.deadly = False
        self.end = False
        self.powerup = False
        self.checkpoint = False

    def update(self, x_shift):
        self.rect.x += x_shift