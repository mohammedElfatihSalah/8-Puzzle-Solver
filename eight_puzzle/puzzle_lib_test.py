import unittest
from eight_puzzle import puzzle_lib


class PuzzleTest(unittest.TestCase):

    def test_init_tiles(self):
        puzzle = puzzle_lib.Puzzle()
        tiles = puzzle.get_tiles()
        self.assertEqual(tiles, [[1, 2, 0], [3, 4, 5], [6, 7, 8]])

    def test_move_up(self):
        puzzle = puzzle_lib.Puzzle()
        puzzle.set_tiles([[1, 2, 3], [0, 4, 5], [6, 7, 8]])
        number, (x, y), (x_new, y_new) = puzzle.move(2, 0)
        self.assertEqual(number, 6)
        self.assertEqual(x_new, 1)
        self.assertEqual(y_new, 0)

    def test_move_up_left_down(self):
        puzzle = puzzle_lib.Puzzle()
        puzzle.set_tiles([[1, 2, 3], [0, 4, 5], [6, 7, 8]])
        _ = puzzle.move(2, 0)
        _ = puzzle.move(2, 1)
        number, (x, y), (x_new, y_new) = puzzle.move(1, 1)
        self.assertEqual(number, 4)
        self.assertEqual(x_new, 2)
        self.assertEqual(y_new, 1)
        self.assertEqual(puzzle.get_tiles(), [[1, 2, 3], [6, 0, 5], [7, 4, 8]])

    def test_move_right(self):
        puzzle = puzzle_lib.Puzzle()
        puzzle.set_tiles([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
        number, (x, y), (x_new, y_new) = puzzle.move(1, 0)
        self.assertEqual((x_new, y_new), (1, 1))
        self.assertEqual(puzzle.get_tiles(), [[1, 2, 3], [0, 4, 5], [6, 7, 8]])

    def test_move_none_movable_tiles(self):
        puzzle = puzzle_lib.Puzzle()
        puzzle.set_tiles([[1, 2, 3], [0, 4, 5], [6, 7, 8]])

        number, (x, y), (x_new, y_new) = puzzle.move(0, 1)
        self.assertEqual((x, y), (x_new, y_new))

        number, (x, y), (x_new, y_new) = puzzle.move(0, 2)
        self.assertEqual((x, y), (x_new, y_new))

        number, (x, y), (x_new, y_new) = puzzle.move(2, 2)
        self.assertEqual((x, y), (x_new, y_new))

    def test_is_empty(self):
        puzzle = puzzle_lib.Puzzle()
        puzzle.set_tiles([[1, 2, 3], [0, 4, 5], [6, 7, 8]])
        _ = puzzle.move(2, 0)
        _ = puzzle.move(2, 1)
        self.assertTrue(puzzle.is_empty(2, 1))


if __name__ == "__main__":
    unittest.main()
