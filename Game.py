import pygame as pg
from Player import Player

class Game():
  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 720
  UNIT_SIZE = 25
  GAME_UNITS = (SCREEN_WIDTH * SCREEN_HEIGHT) / UNIT_SIZE
  CLOCK = pg.time.Clock()
  DT = 0

  def __init__(self):
    pg.init()
    screen = pg.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    running = True

    # Player
    playerPos = pg.Vector2(screen.get_width() / 2, screen.get_height() - Game.UNIT_SIZE)
    player = Player.getInstance(screen, playerPos)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Player
        player.draw()
        player.move()

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        Game.DT = Game.CLOCK.tick(60) / 1000

    pg.quit()