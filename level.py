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
        self.setupLevel()
        self.worldShift = pygame.math.Vector2(0, 0)
        self.currentX = 0
        self.finish = False
        self.loose = False

    def setupLevel(self):
        self.tiles = pygame.sprite.Group()
        self.gravitiles = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.endsprite = pygame.sprite.GroupSingle()
        self.npcs = pygame.sprite.Group()
        self.collidTiles = [self.tiles, self.spikes]
        self.player.lastCheckpoint = None

        file = open(self.csv, "r")
        rows = file.read().split("\n")
        rows.pop()  # Supprimer la dernière ligne vide

        for rowIndex, row in enumerate(rows):
            row = row.split(",")
            for colIndex, cell in enumerate(row):
                cell = int(cell)
                x = colIndex
                y = rowIndex
                if cell == 1:  # tile -> bloc de mur/sol
                    if int(rows[rowIndex - 1].split(",")[colIndex]) == 1:
                        tile = Tile((x * tileSize, y * tileSize), tileSize, True)
                    else:
                        tile = Tile((x * tileSize, y * tileSize), tileSize, False)
                    self.tiles.add(tile)
                elif cell == 2:     # Joueur
                    player_sprite = Player((x * tileSize, y * tileSize), self)
                    self.player.add(player_sprite)
                elif cell == 3:     # spike -> pic
                    spike = Spike((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(spike)
                    self.spikes.add(spike)
                elif cell == 4:     # npc -> ennemi
                    npc = Npc((x * tileSize, y * tileSize + tileSize / 2))
                    self.npcs.add(npc)
                elif cell == 5:     # fin
                    end = End((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(end)
                    self.endsprite.add(end)
                elif cell == 6:     # powerup
                    powerup = Powerup((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(powerup)
                    self.powerups.add(powerup)
                elif cell == 7:     # checkpoint
                    checkpoint = Checkpoint((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(checkpoint)
                    self.checkpoints.add(checkpoint)
                elif cell == 8:     # échelle
                    ladder = Ladder((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(ladder)
                    self.ladders.add(ladder)
                elif cell == 9:     # bloc anti gravité
                    gravitile = Gravitile((x * tileSize, y * tileSize), tileSize)
                    self.gravitiles.add(gravitile)
                    self.tiles.add(gravitile)
        self.collidTiles[0] = self.tiles
        self.collidTiles[1] = self.spikes


    def blocCollision(self):
        inLadder = False
        player = self.player.sprite

        if player.rect.colliderect(self.endsprite.sprite.rect):
            self.setupLevel()
            self.finish = True

        for sprite in self.powerups.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.powerup:
                print("powerup")

        for sprite in self.checkpoints.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.checkpoint:
                self.player.sprite.lastCheckpoint = sprite

        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.player.sprite.die()

        for sprite in self.ladders.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.ladder:
                player.collideOnLadder = sprite.rect.colliderect(player.rect) and sprite.ladder
                inLadder = True

        if not inLadder:
            player.collideOnLadder = False

    def horizontalMovementCollision(self):
        # gestion des collisions horizontales
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for groupTile in self.collidTiles:
            for sprite in groupTile.sprites():
                if sprite.rect.colliderect(player.rect) and not (sprite.ladder or sprite.checkpoint or sprite.powerup or sprite.end or sprite.deadly):
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
        # print(f"Left: {player.collideOnLeft} - Right: {player.collideOnRight}")
        if player.rect.centerx != self.currentX:
            player.collideOnLeft = False
            player.collideOnRight = False

    def verticalMovementCollision(self):
        # gestion des collisions verticales
        player = self.player.sprite
        player.applyGravity()
        for sprite in self.tiles.sprites():
            # collisions tiles
            if sprite.rect.colliderect(player.rect) and not (sprite.ladder or sprite.checkpoint or sprite.powerup or sprite.end or sprite.deadly):
                # sol
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.canJump = True
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
            for npc2 in self.npcs.sprites():
                if npc2.rect.colliderect(npc.rect) and npc.direction.x < 0 and npc != npc2:
                    npc.rect.left = tile.rect.right
                    npc.direction.x = 1
                elif npc2.rect.colliderect(npc.rect) and npc.direction.x > 0 and npc != npc2:
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


    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 4 and directionX < 0:
            self.worldShift.x = playerSpeed
            player.speed = 0
        elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
            self.worldShift.x = -playerSpeed
            player.speed = 0
        else:
            self.worldShift.x = 0
            player.speed = playerSpeed

    def cameraFollowPlayer(self):
        player = self.player.sprite
        playerY = player.rect.centery
        screenCenter = screenHeight / 2
        playerDelta = screenCenter - playerY

        if abs(playerDelta) - 100 > 0:
            if playerDelta > 0:
                self.worldShift.y = playerDelta - 100
            if playerDelta < 0:
                self.worldShift.y = playerDelta + 100
        else:
            self.worldShift.y = 0

    def run(self):
        # updates
        self.tiles.update(self.worldShift)
        self.npcs.update(self.worldShift)
        self.player.update(self.worldShift)


        self.tiles.draw(self.displaySurface)
        self.player.draw(self.displaySurface)
        self.npcs.draw(self.displaySurface)

        # gravitiles
        self.gravitileVerticalMovementCollision()

        # player
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.blocCollision()
                                                                                
        # npcs
        self.npcHorizontalMovementCollision()
        self.npcVerticalMovementCollision()

        # camera
        self.scrollX()
        self.cameraFollowPlayer()