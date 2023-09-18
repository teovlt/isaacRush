import pygame as pg

class GamePanel():
  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 720
  UNIT_SIZE = 25
  GAME_UNITS = (SCREEN_WIDTH * SCREEN_HEIGHT) / UNIT_SIZE
  CLOCK = pg.time.Clock()
  DT = 0

  def __init__(self):
    pg.init()
    self.screen = pg.display.set_mode((GamePanel.SCREEN_WIDTH, GamePanel.SCREEN_HEIGHT))