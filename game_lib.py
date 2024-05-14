class Puzzle:

    def __init__(self):
        self._init_tiles()

    def _init_tiles(self):
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(i * 3 + j)
            tiles.append(row)
        self._tiles = tiles
        self._empty_tile_pos = 0, 0

    def get_tiles(self):
        return self._tiles()

    def get_empty_tile_pos(self):
        return self._empty_tile_pos

    def set_empty_tile_pos(self, x, y):
        self._empty_tile_pos = (x, y)

    def move(self, x, y):
        tile = self._tile[x][y]
        if self.is_empty(tile):
            return None
        new_x, new_y = self.get_empty_tile_pos()
        self._tiles[new_x][new_y] = tile
        self._tiles[x][y] = 0
        self._update_empty_tile_pos(self, x, y)
        return (tile, (x, y), (new_x, new_y))
