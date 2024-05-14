import unittest
import game_lib


class PuzzleTest(unittest.TestCase):

    def test_init_tiles(self):
        puzzle = game_lib.Puzzle()
        tiles = puzzle.get_tiles()
        self.assertEqual(tiles, [])


if __name__ == "__main__":
    unittest.main()
