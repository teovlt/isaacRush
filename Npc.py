
import pygame as pg


class Npc(pg.sprite.Sprite):
    def __init__(self, color, taille, pos, screen):
        super().__init__()
        self.image = pg.Surface((taille, taille))
        self.image.fill(color)
        self.color = color
        self.taille = taille
        self.speed = 8
        self.direction = 1
        self.targetX = 1255
        self.screen = screen
        self.pos = pos
        self.rect = pg.Rect(self.pos.x, self.pos.y, taille, taille)


    def draw(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        pg.draw.rect(self.screen, self.color, self.rect)

    def move(self):
        self.pos.x += self.speed * self.direction

        if self.pos.x > self.targetX:
            self.direction = -1
        elif self.pos.x < 0:
            self.direction = 1





