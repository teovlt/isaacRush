import pygame as pg
from GamePanel import GamePanel
from Player import Player

class Game():
  def __init__(self, screen):
    running = True
    self.screen = screen

    # Player
    playerPos = pg.Vector2(screen.get_width() / 2, screen.get_height() - GamePanel.UNIT_SIZE)
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
        GamePanel.DT = GamePanel.CLOCK.tick(60) / 1000

    pg.quit()