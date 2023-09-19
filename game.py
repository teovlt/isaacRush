import pygame as pg

class Game():
  def __init__(self):
    self.curr_menu = None
    self.running = None
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    running = True
    dt = 0

    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() - 60)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        pg.draw.rect(screen, "white", pg.Rect(player_pos.x, player_pos.y, 25, 25))

        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
          if (player_pos.x > 0):
            player_pos.x -= 250 * dt
        if keys[pg.K_d]:
          if (player_pos.x + 25 < 1280):
            player_pos.x += 250 * dt
        if keys[pg.K_z]:
          if (player_pos.y > 0):
            player_pos.y -= 250 * dt
        if keys[pg.K_s]:
          if (player_pos.y + 25 < 720):
            player_pos.y += 250 * dt

        # flip() the display to put your work on screen
        pg.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pg.quit()
