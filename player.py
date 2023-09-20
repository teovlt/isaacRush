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
        self.spacePressed = False

        # état
        self.onGround = False
        self.canJump = False
        self.canJumpOnLeft = False
        self.canJumpOnRight = False
        self.collideOnLeft= False
        self.collideOnRight= False
        self.collisionLadder = False

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.spacePressed:
            self.jump()
            self.spacePressed = True
        elif not keys[pygame.K_SPACE]:
            self.spacePressed = False

        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.ladderClimb()

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        print(self.collideOnRight)
        if self.onGround and self.canJump:
            self.direction.y = self.jumpSpeed
            self.canJumpOnLeft = True
            self.canJumpOnRight = True
            self.canJump = False

        elif self.collideOnLeft and self.canJumpOnLeft:
            self.direction.y = self.jumpSpeed
            self.canJumpOnLeft = False
            self.canJumpOnRight = True

        elif self.collideOnRight and self.canJumpOnRight:
            self.direction.y = self.jumpSpeed
            self.canJumpOnRight = False
            self.canJumpOnLeft = True

    def ladderClimb(self):
        if self.collisionLadder:
            self.direction.y = self.jumpSpeed

    def update(self, shift):
        self.getInput()
        self.rect.y += shift.y