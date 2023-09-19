# spike.py

import tile


class Spike(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('orange')
        self.deadly = True
