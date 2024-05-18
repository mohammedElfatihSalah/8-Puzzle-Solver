NUM_ROWS = 3
NUM_COLS = 3


class Puzzle:

    def __init__(self):
        self._init_tiles()

    def _init_tiles(self):
        self._tiles = [[1, 2, 0], [3, 4, 5], [6, 7, 8]]
        self._empty_tile_pos = 0, 2

    def get_tiles(self):
        return self._tiles

    def set_tiles(self, tiles):
        # TODO: Add check to the size of tiles.
        self._tiles = tiles
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                if tiles[i][j] == 0:
                    self._empty_tile_pos = (i, j)
                    break

    def is_solved(self):
        return self._tiles == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def is_empty(self, x, y):
        return self._tiles[x][y] == 0

    def move(self, x, y):
        tile = self._tiles[x][y]
        for delta_x, delta_y in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            x_new = x + delta_x
            y_new = y + delta_y
            if (
                (0 <= x_new < NUM_ROWS)
                and (0 <= y_new < NUM_COLS)
                and self.is_empty(x_new, y_new)
            ):
                tile = self._tiles[x][y]
                self._tiles[x_new][y_new] = tile
                self._tiles[x][y] = 0
                self._empty_tile_pos = (x, y)
                return tile, (x, y), (x_new, y_new)

        return self._tiles[x][y], (x, y), (x, y)

    def _convert_action_to_delta(self, action):
        if action == "up":
            return (-1, 0)
        elif action == "down":
            return (1, 0)
        elif action == "right":
            return (0, 1)
        elif action == "left":
            return (0, -1)
        else:
            raise ValueError()

    def move_by_direction(self, direction):
        print(direction)
        x, y = self._empty_tile_pos
        dx, dy = self._convert_action_to_delta(direction)

        x_new = x + dx
        y_new = y + dy

        number = self._tiles[x_new][y_new]
        self._tiles[x][y] = number
        self._tiles[x_new][y_new] = 0
        self._empty_tile_pos = (x_new, y_new)
        return number, (x_new, y_new), (x, y)
