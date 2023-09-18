
import pygame as pg


class Npc(pg.sprite.Sprite):
    def __init__(self, color, taille, pos, screen):
        super().__init__()
        self.image = pg.Surface((taille, taille))
        self.image.fill(color)
        self.color = color
        self.taille = taille
        self.speed = 3
        self.direction = 1
        self.targetX = 1255
        self.screen = screen
        self.pos = pos

    def draw(self):
        pg.draw.rect(self.screen, self.color, pg.Rect(self.pos.x, self.pos.y, self.taille, self.taille))

    def move(self):
        pass


