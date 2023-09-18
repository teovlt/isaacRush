import pygame as pg
from Player import Player

class Game():
  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 720
  UNIT_SIZE = 25
  GAME_UNITS = (SCREEN_WIDTH * SCREEN_HEIGHT) / UNIT_SIZE
  Clock = pg.time.Clock()

  def __init__(self):
    pg.init()
    screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    running = True
    # dt = 0

    # Player
    # player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() - Game.UNIT_SIZE)
    # Player(screen, player_pos)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = Game.Clock.tick(60) / 1000

    pg.quit()