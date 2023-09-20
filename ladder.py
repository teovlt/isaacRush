# ladder.py
import tile

class Ladder(tile.Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('brown')
        self.image.set_alpha(100)
        self.ladder = True