import dataclasses
from typing import Optional, List, Any


NUM_ROWS = 3
NUM_COLS = 3


@dataclasses.dataclass
class Node:
    state: tuple
    parent: Any = None
    action: str = ""
    depth: int = 0
    _zero_index: Optional[int] = None

    def __eq__(self, __value) -> bool:
        if __value:
            return __value.state == self.state
        else:
            return False

    def _get_zero_index(self):
        if self._zero_index:
            return self._zero_index
        else:
            for i, val in enumerate(self.state):
                if val == 0:
                    self._zero_index = i
                    return self._zero_index

    def _convert_index_to_xy(self, index: int) -> tuple:
        return index // NUM_COLS, index % NUM_ROWS

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

    def _move_zero(self, x_new, y_new, x, y):
        index_new = x_new * NUM_COLS + y_new
        index = x * NUM_COLS + y

        new_state = []
        for i in range(len(self.state)):
            if i == index_new:
                new_state.append(0)
            elif i == index:
                new_state.append(self.state[index_new])
            else:
                new_state.append(self.state[i])
        return (*new_state,)

    def apply_action(self, action: str):
        index = self._get_zero_index()
        x, y = self._convert_index_to_xy(index)
        x_delta, y_delta = self._convert_action_to_delta(action)

        x_new, y_new = x + x_delta, y + y_delta
        if (0 <= x_new < NUM_ROWS) and (0 <= y_new < NUM_COLS):
            new_state = self._move_zero(x_new, y_new, x, y)
            return Node(
                state=new_state, parent=self, action=action, depth=self.depth + 1
            )
        else:
            return None


@dataclasses.dataclass
class Solver:
    _goal_state: tuple[int] = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    _actions: tuple[str] = ("up", "down", "right", "left")

    def _is_solved(self, node):
        return node.state == self._goal_state

    def _depth_first_search(
        self, init_state: tuple[int], max_depth: int, max_iterations: int
    ) -> list[str]:
        root_node = Node(state=init_state)
        frontier = [root_node]

        iter_no = 0
        while len(frontier) > 0:
            iter_no += 1
            if iter_no > max_iterations:
                return None
            current_node = frontier.pop(-1)

            if self._is_solved(current_node):
                return current_node
            for action in self._actions:
                neighbor_node = current_node.apply_action(action)
                if (
                    neighbor_node
                    and neighbor_node != current_node.parent
                    and neighbor_node.depth < max_depth
                ):
                    frontier.append(neighbor_node)

    def solve(self, init_state: list[int]) -> list[str]:
        node = self._depth_first_search(init_state, 30, 10_000_00)

        result = []
        if node:
            while node.parent:
                result.append(node.action)
                node = node.parent
        return result[::-1]
