# checkpoint.py

import tile
import itertools
import pygame


class Checkpoint(tile.Tile):
    id_iter = itertools.count()
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load("Graphics/CheckPoints/flag.png")
        self.image = pygame.transform.scale(self.image, (size*2, size * 3))  # Redimensionner si nécessaire
        self.rect = self.image.get_rect(topleft=pos)
        self.checkpoint = True
        self.id = next(self.id_iter)
