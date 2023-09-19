# player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pos)

        # déplacements
        self.direction = pygame.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16

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

    def update(self):
        self.getInput()