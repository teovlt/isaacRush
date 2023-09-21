# npc.py
import pygame
from settings import tileSize


class Npc(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tileSize/2, tileSize/2))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=pos)

        # déplacements
        self.direction = pygame.Vector2(1, 0)
        self.gravity = tileSize/80
        self.speed = tileSize/32

        # état
        self.onGround = False

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, worldShift):
        self.rect.x += worldShift.x
        self.rect.y += worldShift.y