
import pygame as pg


class Npc(pg.sprite.Sprite):
    def __init__(self, color, taille, pos, screen):
        super().__init__()
        self.image = pg.Surface((taille, taille))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.color = color
        self.taille = taille
        self.speed = 8
        self.direction = 1
        self.targetX = 1255
        self.screen = screen
        self.pos = pos

    def draw(self):
        pg.draw.rect(self.screen, self.color, pg.Rect(self.pos.x, self.pos.y, self.taille, self.taille))

    def move(self):
        self.pos.x += self.speed * self.direction

        if self.pos.x > self.targetX:
            self.direction = -1
        elif self.pos.x < 0:
            self.direction = 1



    def get_rect(self):
        return pg.Rect(self.pos.x, self.pos.y, self.taille, self.taille)

