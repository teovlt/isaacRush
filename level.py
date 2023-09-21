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
        self.cameraObjects.append(self.tiles)
        # Anti bravity blocks
        self.gravitiles = pygame.sprite.Group()
        self.cameraObjects.append(self.gravitiles)
        # Spikes
        self.spikes = pygame.sprite.Group()
        self.cameraObjects.append(self.spikes)
        # Power Ups
        self.powerups = pygame.sprite.Group()
        self.cameraObjects.append(self.powerups)
        # Checkpoints
        self.checkpoints = pygame.sprite.Group()
        self.cameraObjects.append(self.checkpoints)
        # Ladders
        self.ladders = pygame.sprite.Group()
        self.cameraObjects.append(self.ladders)
        # Npcs
        self.npcs = pygame.sprite.Group()
        self.cameraObjects.append(self.npcs)
        # End
        self.endsprite = pygame.sprite.GroupSingle()
        self.cameraObjects.append(self.endsprite)
        # Player
        self.player = pygame.sprite.GroupSingle()
        
        self.collidTiles = [self.tiles]
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
        self.collidTiles.clear()
        self.collidTiles.append(self.tiles)
        self.collidTiles.append(self.spikes)
        self.resetCamera()


    def blocCollision(self):
        inLadder = False
        player = self.player.sprite

        if self.endsprite.sprite.rect.colliderect(player.rect) and self.endsprite.sprite.end:
            self.setupLevel()
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
        # collision horizontale
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.centerx
                    player.collideOnLeft = True
                    break
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.centerx
                    player.collideOnRight = True
                    break
        # collision verticale
        player.applyGravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.canJump = True
                    player.lastJumpX = None
                    break
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    break
        # si le joueur bouge sur l'axe x , on considère qu'il n'est plus en collision avec le mur
        if player.rect.centerx < self.currentX or player.rect.centerx > self.currentX:
            player.collideOnLeft = False
            player.collideOnRight = False

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False

        for npc in self.npcs.sprites():
            if npc.rect.colliderect(player.rect) and player.direction.y > 0:
                player.rect.bottom = npc.rect.top
                player.direction.y = player.jumpSpeed / 2
                npc.kill()


    def horizontalMovementCollision(self):
        # gestion des collisions horizontales
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for groupTile in self.collidTiles:
            for sprite in groupTile.sprites():
                if sprite.rect.colliderect(player.rect) and not (
                        sprite.ladder or sprite.checkpoint or sprite.powerup or sprite.end or sprite.deadly):
                    # collisions gauche
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        self.currentX = player.rect.centerx
                        player.collideOnLeft = True
                    # collisions droite
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                        self.currentX = player.rect.centerx
                        player.collideOnRight = True
        # si le joueur bouge sur l'axe x , on considère qu'il n'est plus en collision avec le mur
        if player.rect.centerx != self.currentX:
            player.collideOnLeft = False
            player.collideOnRight = False

    def verticalMovementCollision(self):
        # gestion des collisions verticales
        player = self.player.sprite
        player.applyGravity()
        for sprite in self.tiles.sprites():
            # collisions tiles
            if sprite.rect.colliderect(player.rect) and not (
                    sprite.ladder or sprite.checkpoint or sprite.powerup or sprite.end or sprite.deadly):
                # sol
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.canJump = True
                    player.lastJumpX = None
                # plafond
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        for npc in self.npcs.sprites():
            if npc.rect.colliderect(player.rect) and player.direction.y > 0:
                player.rect.bottom = npc.rect.top
                player.direction.y = player.jumpSpeed / 2
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

        # Print debug information (optional)
        print(f"Player x: {player_center.x}, y: {player_center.y}")
        print(f"Delta x: {delta.x}, y: {delta.y}")


    def run(self):
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
        self.player.draw(self.displaySurface)
        self.npcs.draw(self.displaySurface)

        # gravitiles
        self.gravitileVerticalMovementCollision()

        # player
        self.movementCollision()
        self.blocCollision()

        # npcs
        self.npcHorizontalMovementCollision()
        self.npcVerticalMovementCollision()

        # camera
        self.cameraBehavior()