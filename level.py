# level.py
import pygame
from tile import Tile
from player import Player
from settings import tileSize, screenWidth
from npc import Npc
from spike import Spike


class Level:
    def __init__(self, surface, csv):
        self.csv = csv
        self.displaySurface = surface
        self.setupLevel(csv)
        self.worldShift = 0
        self.currentX = 0
        self.finish = False

    def setupLevel(self, csv):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.npcs = pygame.sprite.Group()

        file = open(csv, "r")
        rows = file.read().split("\n")
        rows.pop()  # Supprimer la dernière ligne vide

        for rowIndex, row in enumerate(rows):
            row = row.split(",")
            for colIndex, cell in enumerate(row):
                cell = int(cell)
                x = colIndex
                y = rowIndex
                if cell == 1:
                    tile = Tile((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(tile)
                elif cell == 2:
                    player_sprite = Player((x * tileSize, y * tileSize))
                    self.player.add(player_sprite)
                elif cell == 3:
                    spike = Spike((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(spike)
                elif cell == 4:
                    npc = Npc((x * tileSize, y * tileSize + tileSize / 2))
                    self.npcs.add(npc)

    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.setupLevel(self.csv)
                self.finish = True
            elif sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right

    def horizontalMovementCollisionNpcs(self):
        npcs = self.npcs.sprites()
        player = self.player.sprite

        for npc in npcs:
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(npc.rect) and npc.direction.x < 0:
                    npc.rect.left = sprite.rect.right
                    npc.direction.x = 1
                elif sprite.rect.colliderect(npc.rect) and npc.direction.x > 0:
                    npc.rect.right = sprite.rect.left
                    npc.direction.x = -1
                elif npc.rect.colliderect(player.rect):
                    self.setupLevel(self.csv)
                    self.finish = True

    def verticalMovementCollision(self):
        player = self.player.sprite
        player.applyGravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.setupLevel(self.csv)
                self.finish = True
            elif sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8

    def run(self):
        # tiles
        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)

        # player
        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()

        self.scrollX()
        self.player.draw(self.displaySurface)

        # npcs
        self.npcs.draw(self.displaySurface)
        self.npcs.update(self.worldShift)
        self.horizontalMovementCollisionNpcs()
