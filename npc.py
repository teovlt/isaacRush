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
        self.speed = 5

        # état
        self.onGround = False

    def update(self, xShift):
        self.rect.x += xShift
        self.rect.x += self.speed * self.direction.x
