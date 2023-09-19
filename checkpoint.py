# checkpoint.py

import tile


class Checkpoint(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('pink')
        self.checkpoint = True