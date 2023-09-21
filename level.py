# level.py
import pygame
from settings import tileSize, screenWidth, screenHeight
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
        self.setupLevel(csv)
        self.worldShift = pygame.math.Vector2(0,0)
        self.currentX = 0
        self.finish = False
        self.loose = False

    def setupLevel(self, csv):
        self.tiles = pygame.sprite.Group()
        self.gravitiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.npcs = pygame.sprite.Group()
        self.player.lastCheckpoint = None

        file = open(csv, "r")
        rows = file.read().split("\n")
        rows.pop()  # Supprimer la dernière ligne vide

        for rowIndex, row in enumerate(rows):
            row = row.split(",")
            for colIndex, cell in enumerate(row):
                cell = int(cell)
                x = colIndex
                y = rowIndex
                if cell == 1:       # tile -> bloc de mur/sol
                    tile = Tile((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(tile)
                elif cell == 2:     # Joueur
                    player_sprite = Player((x * tileSize, y * tileSize), self)
                    self.player.add(player_sprite)
                elif cell == 3:     # spike -> pic
                    spike = Spike((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(spike)
                elif cell == 4:     # npc -> ennemi
                    npc = Npc((x * tileSize, y * tileSize + tileSize / 2))
                    self.npcs.add(npc)
                elif cell == 5:
                    end = End((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(end)
                elif cell == 6:
                    powerup = Powerup((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(powerup)
                elif cell == 7:
                    checkpoint = Checkpoint((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(checkpoint)
                elif cell == 8:
                    ladder = Ladder((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(ladder)
                elif cell == 9:
                    gravitile = Gravitile((x * tileSize, y * tileSize), tileSize)
                    self.gravitiles.add(gravitile)
                    self.tiles.add(gravitile)

    def blocCollision(self):
        inLadder = False
        player = self.player.sprite
        for sprite in self.tiles.sprites():
            # disable collisions end
            if sprite.rect.colliderect(player.rect) and sprite.end:
                self.setupLevel(self.csv)
                self.finish = True
            # disable collisions powerup
            elif sprite.rect.colliderect(player.rect) and sprite.powerup:
                print("powerup")
            # disable collisions checkpoint
            elif sprite.rect.colliderect(player.rect) and sprite.checkpoint:
                self.player.sprite.lastCheckpoint = sprite
            # collisions spike
            elif sprite.rect.colliderect(player.rect) and sprite.deadly:
                if self.player.sprite.lastCheckpoint is None:
                    self.setupLevel(self.csv)
                    self.loose = True
                else:
                    self.player.sprite.respawnLastCheckpoint()
                # collisions tiles
            elif sprite.rect.colliderect(player.rect) and sprite.ladder:
                player.collisionLadder = sprite.rect.colliderect(player.rect) and sprite.ladder
                inLadder = True

        if not inLadder:
            player.collisionLadder = False

    def horizontalMovementCollision(self):
        # gestion des collisions horizontales
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
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
        if player.rect.centerx < self.currentX or player.rect.centerx > self.currentX:
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

    def gravitileVerticalMovementCollision(self):
        for gravitile in self.gravitiles.sprites():
            gravitile.applyGravity()
            for tile in self.tiles.sprites():
                if gravitile.rect.colliderect(tile.rect) and not tile.antiGravity:
                    gravitile.rect.bottom = tile.rect.top
                    gravitile.direction.y = 0

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
                self.setupLevel(self.csv)
                self.loose = True

    def npcVerticalMovementCollision(self):
        player = self.player.sprite
        for npc in self.npcs.sprites():
            npc.applyGravity()
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(npc.rect):
                    npc.rect.bottom = tile.rect.top
                    npc.direction.y = 0
            if npc.rect.colliderect(player.rect):
                 self.setupLevel(self.csv)
                 self.loose = True

    def antigravite(self):
        for tile in self.gravitiles.sprites():
            tile.update(pygame.math.Vector2(0, -tileSize/3))


    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 4 and directionX < 0:
            self.worldShift.x = tileSize/8
            player.speed = 0
        elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
            self.worldShift.x = -tileSize/8
            player.speed = 0
        else:
            self.worldShift.x = 0
            player.speed = tileSize/8


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


        # player
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.blocCollision()
                                                                                
        # npcs
        self.npcHorizontalMovementCollision()
        self.npcVerticalMovementCollision()

        # gravitiles
        self.gravitileVerticalMovementCollision()

        # camera
        self.scrollX()
        self.cameraFollowPlayer()