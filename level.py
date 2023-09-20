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
                if cell == 1:       # tile -> bloc de mur/sol
                    tile = Tile((x * tileSize, y * tileSize), tileSize)
                    self.tiles.add(tile)
                elif cell == 2:     # Joueur
                    player_sprite = Player((x * tileSize, y * tileSize))
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

    def blocCollision(self):
        inLadder = False
        player = self.player.sprite
<<<<<<< HEAD
        player.rect.x += player.direction.x * player.speed
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
                print("checkpoint")
            #collisions spike
            elif sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.setupLevel(self.csv)
                self.loose = True

            elif sprite.rect.colliderect(player.rect):
                # collisions gauche
                if player.direction.x < 0:
                    # blocage du joueur au niveau du bord droite du tile
                    player.rect.left = sprite.rect.right
                    # empêcher le joueur de sauter deux fois du même mur
                    if player.lastJump != "gauche":
                        player.canJump = True
                    #le dernier saut a été fait depuis le mur gauche
                    player.lastJump = "gauche"
                    #le joueur est en collision avec le mur gauche
                    player.collisionGauche = True
                # collisions droite
                elif player.direction.x > 0:
                    # blocage du joueur au niveau du bord gauche du tile
                    player.rect.right = sprite.rect.left
                    # empêcher le joueur de sauter deux fois du même mur
                    if player.lastJump != "droite":
                        player.canJump = True
                    # le dernier saut a été fait depuis le mur droit
                    player.lastJump = "droite"
                    # le joueur est en collision avec le mur droit
                    player.collisionDroite = True
        # print(player.direction.x)
        # si le joueur bouge sur l'axe x , on considère qu'il n'est plus en collision avec le mur
        if (player.collisionDroite and player.direction.x < 1) or (player.collisionGauche and player.direction.x > -1):
            player.collisionDroite = False
            player.collisionGauche = False


    def verticalMovementCollision(self):
        # gestion des collisions verticales
        player = self.player.sprite
        player.applyGravity()
=======
>>>>>>> d14ca462bcb0a6e2a29b9276277fc7574cd49b19
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
                print("checkpoint")
            # collisions spike
            elif sprite.rect.colliderect(player.rect) and sprite.deadly:
                self.setupLevel(self.csv)
<<<<<<< HEAD
                self.loose = True

=======
                # collisions tiles
                self.finish = True
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
                    player.canJump = True
                    player.collisionGauche = True
                # collisions droite
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.canJump = True
                    player.collisionDroite = True
        # si le joueur bouge sur l'axe x , on considère qu'il n'est plus en collision avec le mur
        if (player.collisionDroite and player.direction.x < 1) or (player.collisionGauche and player.direction.x > -1):
            player.collisionDroite = False
            player.collisionGauche = False


    def verticalMovementCollision(self):
        # gestion des collisions verticales
        player = self.player.sprite
        player.applyGravity()
        for sprite in self.tiles.sprites():
>>>>>>> d14ca462bcb0a6e2a29b9276277fc7574cd49b19
            # collisions tiles
            if sprite.rect.colliderect(player.rect) and not (sprite.ladder or sprite.checkpoint or sprite.powerup or sprite.end or sprite.deadly):
                # sol
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.canJump = True
                    player.lastJump = "sol"
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
                self.setupLevel(self.csv)
                self.finish = True


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

        # camera
        self.scrollX()
        self.cameraFollowPlayer()