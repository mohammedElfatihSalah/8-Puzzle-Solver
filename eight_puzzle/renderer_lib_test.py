import unittest
from eight_puzzle import renderer_lib


class RendererTest(unittest.TestCase):

    def setUp(self) -> None:
        info = renderer_lib.DisplayInfo(
            window_height=680,
            window_width=480,
            margin=(50, 60),
            tile_size=20,
            gap_size=7,
            tile_color=(0, 0, 0),
            bg_color=(0, 0, 0),
        )
        self.renderer = renderer_lib.Renderer(info)
        return super().setUp()

    def test_is_outside_naive(self):
        self.assertTrue(self.renderer.is_outside(0, 0))

    def test_is_outside_on_margin(self):
        self.assertFalse(self.renderer.is_outside(50, 60))

    def test_is_outside_on_right_gap_edge(self):
        self.assertFalse(self.renderer.is_outside(131, 60))

    def test_is_outside_on_right_gap_middle(self):
        self.assertFalse(self.renderer.is_outside(126, 60))

    def test_is_outside_on_right_gap_one_pixel_off(self):
        self.assertTrue(self.renderer.is_outside(132, 60))

    def test_is_outside_on_right_middle(self):
        self.assertTrue(self.renderer.is_outside(300, 60))

    def test_is_outside_on_bottom_gap_edge(self):
        self.assertTrue(self.renderer.is_outside(300, 141))

    def test_is_outside_on_the_board(self):
        self.assertFalse(self.renderer.is_outside(70, 80))

    def test_is_outside_on_bottom_gap_edge_one_pixel_off(self):
        self.assertTrue(self.renderer.is_outside(50, 142))

    def test_is_outside_on_bottom_middle(self):
        self.assertTrue(self.renderer.is_outside(50, 142))

    # End: is_outside

    def test_is_on_gap_right_edge(self):
        self.assertTrue(self.renderer.is_on_gap(131, 60))

    def test_is_on_gap_right_edge_one_pixel_off(self):
        self.assertFalse(self.renderer.is_on_gap(132, 60))

    def test_is_on_gap_inside_right_edge(self):
        self.assertTrue(self.renderer.is_on_gap(130, 60))

    def test_is_on_gap_inside_board_vertical_gap(self):
        self.assertTrue(self.renderer.is_on_gap(75, 65))

    def test_is_on_gap_bottom_edge(self):
        self.assertTrue(self.renderer.is_on_gap(50, 141))

    def test_is_on_gap_bottom_edge_one_pixel_off(self):
        self.assertFalse(self.renderer.is_on_gap(50, 142))

    def test_is_on_gap_inside_board_horizontal_gap(self):
        self.assertTrue(self.renderer.is_on_gap(50, 85))

    # End: is_on_gap

    def test_convert_to_game_coordinate(self):

        # On margin point.
        x, y = self.renderer.convert_to_game_coordinate(50, 60)
        self.assertEqual((x, y), (0, 0))

        # Inside the first tile.
        x, y = self.renderer.convert_to_game_coordinate(60, 70)
        self.assertEqual((x, y), (0, 0))

        # On the edge of the first tile.
        x, y = self.renderer.convert_to_game_coordinate(77, 87)
        self.assertEqual((x, y), (0, 0))

        # Inside the second tile on the first row.
        x, y = self.renderer.convert_to_game_coordinate(85, 80)
        self.assertEqual((x, y), (0, 1))

        # On the edge of the second tile on the first row.
        x, y = self.renderer.convert_to_game_coordinate(114, 120)
        self.assertEqual((x, y), (2, 2))

        # Inside the last tile


if __name__ == "__main__":
    unittest.main()
