import unittest
import solver_lib


class NodeTest(unittest.TestCase):

    def test_get_zero_index(self):
        node = solver_lib.Node(state=(1, 0, 2, 3, 4, 5, 6, 7, 8))
        self.assertEqual(node._get_zero_index(), 1)

        node = solver_lib.Node(state=(0, 1, 2, 3, 4, 5, 6, 7, 8))
        self.assertEqual(node._get_zero_index(), 0)

        node = solver_lib.Node(state=(1, 2, 3, 4, 5, 7, 6, 0, 8))
        self.assertEqual(node._get_zero_index(), 7)

        node = solver_lib.Node(state=(1, 6, 2, 3, 4, 5, 8, 7, 0))
        self.assertEqual(node._get_zero_index(), 8)

    def test_get_zero_index_twice(self):
        node = solver_lib.Node(state=(1, 0, 2, 3, 4, 5, 6, 7, 8))
        _ = node._get_zero_index()
        self.assertEqual(node._get_zero_index(), 1)

    def test_covert_to_xy(self):
        node = solver_lib.Node(state=(1, 0, 2, 3, 4, 5, 6, 7, 8))
        x, y = node._convert_index_to_xy(0)
        self.assertEqual((x, y), (0, 0))

        x, y = node._convert_index_to_xy(1)
        self.assertEqual((x, y), (0, 1))

        x, y = node._convert_index_to_xy(2)
        self.assertEqual((x, y), (0, 2))

        x, y = node._convert_index_to_xy(3)
        self.assertEqual((x, y), (1, 0))

    def test_move_zero(self):
        node = solver_lib.Node(state=(1, 0, 2, 3, 4, 5, 6, 7, 8))

        state = node._move_zero(0, 0, 0, 1)
        self.assertEqual(state, (0, 1, 2, 3, 4, 5, 6, 7, 8))

        state = node._move_zero(0, 2, 0, 1)
        self.assertEqual(state, (1, 2, 0, 3, 4, 5, 6, 7, 8))

        state = node._move_zero(1, 1, 0, 1)
        self.assertEqual(state, (1, 4, 2, 3, 0, 5, 6, 7, 8))

    def test_apply_action(self):
        node = solver_lib.Node(state=(1, 0, 2, 3, 4, 5, 6, 7, 8))
        child_node = node.apply_action("up")

        self.assertIsNone(child_node)

        child_node = node.apply_action("down")
        self.assertEqual(child_node.state, (1, 4, 2, 3, 0, 5, 6, 7, 8))


class SolverTest(unittest.TestCase):

    def test_solve_depth_first_search(self):
        solver = solver_lib.Solver()

        state = (1, 0, 2, 3, 4, 5, 6, 7, 8)
        result = solver.solve(state, "dfs")
        self.assertEqual(result, ["left"])

        state = (1, 2, 0, 3, 4, 5, 6, 7, 8)
        result = solver.solve(state, "dfs")
        self.assertEqual(result, ["left", "left"])

    def test_manhattan_distance(self):
        solver = solver_lib.Solver()

        state = (1, 0, 2, 3, 4, 5, 6, 7, 8)
        result = solver._manhattan_distance(state)
        self.assertEqual(result, 2)

        state = (1, 4, 2, 3, 0, 5, 6, 7, 8)
        result = solver._manhattan_distance(state)
        self.assertEqual(result, 4)

        state = (1, 4, 2, 3, 0, 5, 6, 8, 7)
        result = solver._manhattan_distance(state)
        self.assertEqual(result, 6)

        state = (1, 4, 2, 3, 5, 0, 6, 8, 7)
        result = solver._manhattan_distance(state)
        self.assertEqual(result, 8)

    def test_solve_a_star(self):
        solver = solver_lib.Solver()

        state = (1, 0, 2, 3, 4, 5, 6, 7, 8)
        result = solver.solve(state, "a*")
        self.assertEqual(result, ["left"])

        state = (1, 2, 5, 3, 4, 0, 6, 7, 8)
        result = solver.solve(state, "a*")
        self.assertEqual(result, ["up", "left", "left"])


if __name__ == "__main__":
    unittest.main()
