# powerup.py

import tile


class Powerup(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('purple')
        self.powerup = True