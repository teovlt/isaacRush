# end.py

import tile


class End(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('green')
        self.end = True