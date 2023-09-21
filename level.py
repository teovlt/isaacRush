# level.py
import pygame
from settings import *
from checkpoint import Checkpoint
from powerup import Powerup
from tile import Tile
from player import Player
from npc import Npc
from spike import Spike
from end import End
from ladder import Ladder
from gravitile import Gravitile


class Level:
    def __init__(self, surface, csv):
        self.csv = csv
        self.displaySurface = surface
        self.worldShift = pygame.math.Vector2(0, 0)
        self.currentX = 0
        self.finish = False
        self.loose = False
        self.setupLevel()

    def setupLevel(self):
        self.cameraObjects = []
        # Solid blocs
        self.tiles = pygame.sprite.Group()
        # Anti bravity blocks
        self.gravitiles = pygame.sprite.Group()
        # Spikes
        self.spikes = pygame.sprite.Group()
        # Power Ups
        self.powerups = pygame.sprite.Group()
        # Checkpoints
        self.checkpoints = pygame.sprite.Group()
        # Ladders
        self.ladders = pygame.sprite.Group()
        # Npcs
        self.npcs = pygame.sprite.Group()
        # End
        self.endsprite = pygame.sprite.GroupSingle()
        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.lastCheckpoint = None

        file = open(self.csv, "r")
        rows = file.read().split("\n")
        if not rows[len(rows)-1]:
            rows.pop()  # Supprimer la dernière ligne vide

        for rowIndex, row in enumerate(rows):
            row = row.split(",")
            for colIndex, cell in enumerate(row):
                cell = int(cell)
                x = colIndex
                y = rowIndex
                if cell == 1:  # tile -> bloc de mur/sol
                    if rowIndex > 0 and int(rows[rowIndex - 1].split(",")[colIndex]) == 1:
                        tile = Tile((x * tileSize, y * tileSize), tileSize, True)
                    else:
                        tile = Tile((x * tileSize, y * tileSize), tileSize, False)
                    self.tiles.add(tile)
                elif cell == 2:  # Joueur
                    player_sprite = Player((x * tileSize, y * tileSize), self)
                    self.player.add(player_sprite)
                elif cell == 3:  # spike -> pic
                    spike = Spike((x * tileSize, y * tileSize), tileSize)
                    self.spikes.add(spike)
                elif cell == 4:  # npc -> ennemi
                    npc = Npc((x * tileSize, y * tileSize + tileSize / 2))
                    self.npcs.add(npc)
                elif cell == 5:  # fin
                    end = End((x * tileSize, y * tileSize), tileSize)
                    self.endsprite.add(end)
                elif cell == 6:  # powerup
                    powerup = Powerup((x * tileSize, y * tileSize), tileSize)
                    self.powerups.add(powerup)
                elif cell == 7:  # checkpoint
                    checkpoint = Checkpoint((x * tileSize, y * tileSize), tileSize)
                    self.checkpoints.add(checkpoint)
                elif cell == 8:  # échelle
                    ladder = Ladder((x * tileSize, y * tileSize), tileSize)
                    self.ladders.add(ladder)
                elif cell == 9:  # bloc anti gravité
                    gravitile = Gravitile((x * tileSize, y * tileSize), tileSize)
                    self.gravitiles.add(gravitile)
        self.collidTiles = [self.tiles]
        # Camera
        self.cameraObjects.append(self.tiles)
        self.cameraObjects.append(self.gravitiles)
        self.cameraObjects.append(self.spikes)
        self.cameraObjects.append(self.powerups)
        self.cameraObjects.append(self.checkpoints)
        self.cameraObjects.append(self.ladders)
        self.cameraObjects.append(self.npcs)
        self.cameraObjects.append(self.endsprite)
        self.resetCamera()


    def blocCollision(self):
        inLadder = False
        player = self.player.sprite

        if self.endsprite.sprite.rect.colliderect(player.rect) and self.endsprite.sprite.end:
            # son de fin
            end = pygame.mixer.Sound("Audio/end.wav")
            pygame.mixer.Channel(1).play(end)
            # La fusée monte
            self.endsprite.sprite.direction.y -= 0.1
            self.finish = True

        for sprite in self.powerups.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.powerup:
                print("powerup")

        for sprite in self.checkpoints.sprites():
            if sprite.rect.colliderect(player.rect):
                if self.player.sprite.lastCheckpoint != sprite:
                    self.player.sprite.lastCheckpoint = sprite
                    # Changement du look du checkPoint une fois traversé et ajout d'un effet sonore
                    image = pygame.image.load("Graphics/CheckPoints/flagPassed.png")
                    imageF = pygame.transform.scale(image, (80, 120))
                    sprite.image = imageF
                    check = pygame.mixer.Sound("Audio/checkPoint.wav")
                    pygame.mixer.Channel(1).play(check)

        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.player.sprite.die()

        for sprite in self.ladders.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.ladder:
                player.collideOnLadder = sprite.rect.colliderect(player.rect) and sprite.ladder
                inLadder = True

        if not inLadder:
            player.collideOnLadder = False

    def movementCollision(self):
        # gestion des collisions horizontales et verticales
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        listeSprites = []
        for groupe in self.collidTiles:
            for sprite in groupe.sprites():
                listeSprites.append(sprite)
    # collision horizontale
        for sprite in listeSprites:
            if sprite.rect.colliderect(player.rect):
                player.onGravitile = False
                # collisions gauche
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.centerx
                    player.collideOnLeft = True
                    break
                # collisions droite
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.centerx
                    player.collideOnRight = True
                    break
        for sprite in self.gravitiles.sprites():
            if sprite.rect.colliderect(player.rect) and player.onGround:
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.centerx
                    player.collideOnLeft = True
                    break
                # collisions droite
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.centerx
                    player.collideOnRight = True
                    break
                # player.direction.y = sprite.direction.y -1
        # collision verticale
        player.applyGravity()
        for sprite in listeSprites:
            if sprite.rect.colliderect(player.rect):
                player.onGravitile = False
                # sol
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.canJump = True
                    player.lastJumpX = None
                    break
                # plafond
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    break
        for sprite in self.gravitiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGravitile = True
                    player.canJump = True
                    player.lastJumpX = None
                    break
                # plafond
                elif player.direction.y < 0 :
                    player.onGravitile = True
                    break
                else:
                    player.die()
                player.direction.y = sprite.direction.y


        # si le joueur bouge sur l'axe x , on considère qu'il n'est plus en collision avec le mur
        if player.rect.centerx < self.currentX or player.rect.centerx > self.currentX:
            player.collideOnLeft = False
            player.collideOnRight = False
        # si le joueur bouge sur l'axe y , on considère qu'il n'est plus en collision avec le sol
        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False

        for npc in self.npcs.sprites():
            if npc.rect.colliderect(player.rect) and player.direction.y > 0:
                player.rect.bottom = npc.rect.top
                player.direction.y = player.jumpSpeed / 2
                # Son quand un npc est tué
                killNpc = pygame.mixer.Sound("Audio/killNpc.wav")
                pygame.mixer.Channel(1).play(killNpc)
                npc.kill()

    def npcHorizontalMovementCollision(self):
        player = self.player.sprite
        for npc in self.npcs.sprites():
            npc.rect.x += npc.direction.x * npc.speed
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(npc.rect) and npc.direction.x < 0:
                    npc.rect.left = tile.rect.right
                    npc.direction.x = 1
                elif tile.rect.colliderect(npc.rect) and npc.direction.x > 0:
                    npc.rect.right = tile.rect.left
                    npc.direction.x = -1

            if npc.rect.colliderect(player.rect):
                self.player.sprite.die()

    def npcVerticalMovementCollision(self):
        player = self.player.sprite
        for npc in self.npcs.sprites():
            npc.applyGravity()
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(npc.rect):
                    npc.rect.bottom = tile.rect.top
                    npc.direction.y = 0
            if npc.rect.colliderect(player.rect):
                self.player.sprite.die()

    def gravitileVerticalMovementCollision(self):
        for gravitile in self.gravitiles.sprites():
            gravitile.applyGravity()
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(gravitile.rect) and not tile.antiGravity:
                    gravitile.rect.bottom = tile.rect.top
                    gravitile.direction.y = 0
                    gravitile.onGround = True

    def antiGravite(self):
        for gravitile in self.gravitiles.sprites():
            if gravitile.onGround:
                gravitile.direction.y = gravitile.jumpSpeed
                gravitile.onGround = False
                # Son de la capacité
                check = pygame.mixer.Sound("Audio/capacity.wav")
                pygame.mixer.Channel(1).play(check)

    def cameraBehavior(self):
        player = self.player.sprite
        pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        direction = player.direction
        maxDY = screenHeight / 4
        dy = screenHeight / 2 - pos.y

        # x axis behavior
        if pos.x < screenWidth / 4 and direction.x < 0:
            self.worldShift.x = playerSpeed
            player.speed = 0
        elif pos.x > 3 * screenWidth / 4 and direction.x > 0:
            self.worldShift.x = -playerSpeed
            player.speed = 0
        else:
            self.worldShift.x = 0
            player.speed = playerSpeed

        # y axis behavior
        if abs(dy) > maxDY:
            self.worldShift.y = dy - maxDY if dy > 0 else dy + maxDY
        else:
            self.worldShift.y = 0

    def resetCamera(self):
        player = self.player.sprite
        player_center = pygame.math.Vector2(player.rect.centerx, player.rect.centery)

        # Calculate the delta between the player's position and the center of the screen
        delta = pygame.math.Vector2(screenWidth / 2 - player_center.x, screenHeight / 2 - player_center.y)

        # Update the player's x position based on delta
        player.rect.centerx += delta.x

        # Update the positions of other cameraObjects
        for group in self.cameraObjects:
            for sprite in group.sprites():
                sprite.rect.centerx += delta.x  # Update x position
                # sprite.rect.top += delta.y  # Update y position


    def run(self):
        if self.finish:
            self.endsprite.sprite.up()
            if self.endsprite.sprite.rect.y <= -80:
                self.setupLevel()
                self.loose = True
                self.finish = False

        # updates
        self.player.update(self.worldShift)
        self.tiles.update(self.worldShift)
        self.gravitiles.update(self.worldShift)
        self.spikes.update(self.worldShift)
        self.checkpoints.update(self.worldShift)
        self.powerups.update(self.worldShift)
        self.ladders.update(self.worldShift)
        self.endsprite.update(self.worldShift)
        self.npcs.update(self.worldShift)

        # draw
        self.tiles.draw(self.displaySurface)
        self.gravitiles.draw(self.displaySurface)
        self.spikes.draw(self.displaySurface)
        self.checkpoints.draw(self.displaySurface)
        self.powerups.draw(self.displaySurface)
        self.ladders.draw(self.displaySurface)
        self.endsprite.draw(self.displaySurface)
        if not self.finish:
            self.player.draw(self.displaySurface)
        self.npcs.draw(self.displaySurface)

        # gravitiles
        self.gravitileVerticalMovementCollision()

        # player
        self.movementCollision()

        # npcs
        self.npcHorizontalMovementCollision()
        self.npcVerticalMovementCollision()

        # camera
        self.cameraBehavior()