import pygame as pg

class Menu():
    def __init__(self):
        pg.init()
        screen = pg.display.set_mode((1280, 720))
        clock = pg.time.Clock()
        pg.display.set_caption('Menu')
        running = True
        dt = 0
        mainMenu = False
        font = pg.font.Font('freesansbold.ttf', 24)
        menu_command = 0

        class Button:
            def __init__(self, txt, pos):
                self.text = txt
                self.pos = pos
                self.button = pg.rect.Rect((self.pos[0], self.pos[1]),(268,40))

            def checkClicker(self):

            def draw(self):
                pg.draw.rect(screen, 'light gray', self.button, 0, 5)
                pg.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
                text2 = font.render(self.text, True, 'black')
                screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))


        def drawGame():
            menu_btn = Button('Main Menu', (230, 450))
            menu_btn.draw()
            menu = menu_btn.checkClicked()
            return menu

        def drawMenu():
            command = -1
            pg.draw.rect(screen, 'black', [100, 100, 300, 300])
            pg.draw.rect(screen, 'green', [100, 100, 300, 300], 5)
            pg.draw.rect(screen, 'white', [120, 120, 260, 40], 0, 5)
            pg.draw.rect(screen, 'gray', [120, 120, 260, 40], 5, 5)
            txt = font.render('Menus Tutorial!', True, 'black')
            screen.blit(txt, (135, 127))
            # menu exit button
            menu = Button('Exit Menu', (120, 350))
            menu.draw()
            button1 = Button('Button 1', (120, 180))
            button1.draw()
            button2 = Button('Button 2', (120, 240))
            button2.draw()
            button3 = Button('Button 3', (120, 300))
            button3.draw()
            if menu.checkClicked():
                command = 0
            if button1.checkClicked():
                command = 1
            if button2.checkClicked():
                command = 2
            if button3.checkClicked():
                command = 3
            return command


        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")

            if mainMenu:
                menu_command = drawMenu()
                if menu_command != -1:
                    main_menu = False
            else:
                mainMenu = drawGame()
                if menu_command > 0:
                    text = font.render(f'Button {menu_command} pressed!', True, 'black')
                    screen.blit(text, (150, 100))

            # flip() the display to put your work on screen
            pg.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000

        pg.quit()
