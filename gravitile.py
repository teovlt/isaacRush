# gravitile.py
import tile
import pygame as pg
from settings import tileSize

class Gravitile(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('cyan')
        self.agravite = True
        self.antiGravity = True
        self.direction = pg.Vector2(0, 0)
        self.gravity = tileSize / 80
        self.jumpSpeed = -tileSize / 4

    def applyGravity(self):
        if self.agravite:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y

    def update(self, shift):
        self.rect.x += shift.x
        self.rect.y += shift.y






