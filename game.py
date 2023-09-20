import pygame as pg
import menu

def backMenu():
  menu.Menu()
  print("Je suis bien là")

class Game():
  def __init__(self):
    self.curr_menu = None
    self.running = None
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    pg.display.set_caption("En cours...")
    running = True
    dt = 0

    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() - 60)

    # Fonction pour afficher du texte sur l'écran
    def displayText(text, size, x, y, color):
        police = pg.font.SysFont('Times New Roman', size)
        textSurface = police.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        screen.blit(textSurface, textRect)

    def pause():

      paused = True

      while paused:
        for event in pg.event.get():
          if event.type == pg.QUIT:
            pg.quit()
            quit()

          if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
              paused = False
            elif event.key == pg.K_q:
              backMenu()
        screen.fill('#ffffff')
        displayText("Pause", 100, 650, 200, 'black')
        displayText("Press Echap to continue or Q to quit.", 50, 610, 300, 'black')

        pg.display.update()
        clock.tick(5)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                       
                if event.key == pg.K_ESCAPE:
                    print("JE sais que tu clique sur ECHAP depuis game.py")
                    pause()

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
