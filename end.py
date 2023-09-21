# end.py

import tile
import pygame


class End(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load("Graphics/CheckPoints/end.png")
        self.image = pygame.transform.scale(self.image, (size * 3, size * 3))  # Redimensionner si nécessaire
        self.rect = self.image.get_rect(topleft=pos)
        self.end = True
        self.direction = pygame.Vector2(0, 0)

    def up(self):
        self.rect.y += self.direction.y
