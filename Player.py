import pygame as pg
from GamePanel import GamePanel

class Player():
    _instance = None
  
    def __new__(cls, *args, **kargs):
        if Player._instance is None:
            cls._instance = super(Player, cls).__new__(cls)
            return cls._instance
        else:
            raise Exception("Une instance de Player existe déjà. Utilisez Player.get_instance() pour l'obtenir.")
  
    def __init__(self, screen, playerPos):
        self.screen = screen
        self.playerPos = playerPos

        self.verticalVelocity = 0
        self.gravity = 10
        self.onGround = False

    def draw(self):
        pg.draw.rect(self.screen, "white", pg.Rect(self.playerPos.x, self.playerPos.y, GamePanel.UNIT_SIZE, GamePanel.UNIT_SIZE))
  
    def move(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_q] or keys[pg.K_LEFT]:
          if (self.playerPos.x > 0):
            self.playerPos.x -= 250 * GamePanel.DT
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
          if (self.playerPos.x + 25 < 1280):
            self.playerPos.x += 250 * GamePanel.DT

        # Appliquer la gravité
        if not self.onGround:
           self.verticalVelocity += self.gravity # Ajouter la gravité à la vitesse verticale
           self.playerPos.y += self.verticalVelocity * GamePanel.DT # Mettre à jour la position

        # Limiter la descente du joueur pour qu'il ne passe pas à travers le sol
        if self.playerPos.y + GamePanel.UNIT_SIZE >= GamePanel.SCREEN_HEIGHT:
            self.playerPos.y = GamePanel.SCREEN_HEIGHT - GamePanel.UNIT_SIZE
            self.verticalVelocity = 0 # Arrêter la descente du joueur
            self.onGround = True # Indiquer que le joueur est au sol

        # Gérer le saut
        if keys[pg.K_SPACE] and self.onGround:
           self.verticalVelocity = -200 # Donner une impulsion au joueur
           self.onGround = False # Le joueur n'est plus au sol
           
    @staticmethod
    def getInstance(screen, playerPos):
        if Player._instance is None:    
            Player._instance = Player(screen, playerPos)
        return Player._instance