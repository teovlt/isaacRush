# player.py
import pygame
from settings import tileSize, playerSpeed
from timer import Timer
from utils import importFolder

timer = Timer()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        super().__init__()
        self.level = level

        # déplacements
        self.direction = pygame.Vector2(0, 0)
        self.speed = playerSpeed
        self.gravity = tileSize/80
        self.jumpSpeed = -tileSize/3.3
        self.spacePressed = False

        # état
        self.onGround = False
        self.canJump = False
        self.canJumpOnLeft = False
        self.canJumpOnRight = False
        self.collideOnLeft= False
        self.collideOnRight= False
        self.collideOnLadder = False
        self.collideOnAntiGravity = False
        self.lastCheckpoint = None

        # animations
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = "idle"
        self.facingRight = False

        # rect
        self.image = self.animations["idle"][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
    
    def importCharacterAssets(self):
        characterPath = "./Graphics/Character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)

    def animate(self):
        animation = self.animations[self.status]
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pygame.transform.flip(image, True, False)
            self.image = flippedImage

        self.rect = image.get_rect(bottomright = self.rect.bottomright)

    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys:
            timer.start()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
            self.facingRight = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facingRight = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround and not self.collideOnLeft and not self.collideOnRight:
            self.jump()
        elif keys[pygame.K_SPACE] and not self.spacePressed:
            self.jump()
            self.spacePressed = True
        elif not keys[pygame.K_SPACE]:
            self.spacePressed = False

        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.ladderClimb()

        if keys[pygame.K_e]:
            self.level.antiGravite()

    def getStatus(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
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
        if self.collideOnLadder:
            self.direction.y = self.jumpSpeed

    def respawnLastCheckpoint(self):
        self.rect.x = self.lastCheckpoint.rect.x
        self.rect.y = self.lastCheckpoint.rect.y

    def update(self, shift):
        self.getInput()
        self.getStatus()
        self.animate()
        self.rect.y += shift.y

    def die(self):
        if self.lastCheckpoint is None:
            self.level.setupLevel()
            self.level.loose = True
        else:
            self.respawnLastCheckpoint()
