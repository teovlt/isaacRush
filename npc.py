# npc.py
import pygame


class Npc(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=pos)

        # déplacements
        self.direction = pygame.Vector2(1, 0)
        self.gravity = .8
        self.speed = 2

        # état
        self.onGround = False

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, xShift):
        self.rect.x += xShift
