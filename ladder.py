# ladder.py
import tile
import pygame
class Ladder(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load("Graphics/Ladders/ladder.png")
        self.image = pygame.transform.scale(self.image, (size, size))  # Redimensionner si nécessaire
        self.rect = self.image.get_rect(topleft=pos)
        self.ladder = True