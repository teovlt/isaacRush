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
        self.gravity = 0.1
        self.jumpSpeed = -tileSize / 4
        self.onGround = False

    def applyGravity(self):
        if self.agravite:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y