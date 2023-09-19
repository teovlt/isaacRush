import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # déplacements
        self.direction = pygame.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16

        # état
        self.onGround = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jumpSpeed

    def update(self):
        self.get_input()