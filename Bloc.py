import pygame as pg

class Bloc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pg.draw.rect(screen, "white", pg.Rect(self.x, self.y, 25, 25))



