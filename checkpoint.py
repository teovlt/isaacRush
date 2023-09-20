# checkpoint.py

import tile
import itertools


class Checkpoint(tile.Tile):
    id_iter = itertools.count()
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('pink')
        self.checkpoint = True
        self.id = next(self.id_iter)