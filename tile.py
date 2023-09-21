# tile.py
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, condition=False):
        super().__init__()
        if condition:
            self.image = pygame.image.load("Graphics/Blocks/block.png")
        else:
            self.image = pygame.image.load("Graphics/Blocks/block2.png")
        self.image = pygame.transform.scale(self.image, (size, size))  # Redimensionner si nécessaire
        self.rect = self.image.get_rect(topleft=pos)
        self.deadly = False
        self.end = False
        self.powerup = False
        self.checkpoint = False
        self.ladder = False
        self.antiGravity = False

    def update(self, worldShift):
        self.rect.y += worldShift.y
        self.rect.x += worldShift.x