# player.py
import pygame
from settings import tileSize

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tileSize/2,tileSize))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pos)

        # déplacements
        self.direction = pygame.Vector2(0, 0)
        self.speed = tileSize/8
        self.gravity = tileSize/80
        self.jumpSpeed = -tileSize/4

        # état
        self.onGround = False
        self.canJump = False

        self.lastJump = "sol"

        self.collisionGauche= False
        self.collisionDroite= False

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()


    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.canJump:
            if self.onGround:
                self.direction.y = self.jumpSpeed
                self.lastJump = "sol"
            elif self.collisionDroite or self.collisionGauche:
                # on saute
                self.direction.y = self.jumpSpeed

        self.canJump = False

    def update(self, shift):
        self.getInput()
        self.rect.y += shift.y