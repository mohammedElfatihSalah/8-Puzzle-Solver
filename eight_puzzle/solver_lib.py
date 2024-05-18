import dataclasses
from typing import Optional, Any
import queue


NUM_ROWS = 3
NUM_COLS = 3


@dataclasses.dataclass
class Node:
    state: tuple
    parent: Any = None
    action: str = ""
    depth: int = 0
    id: int = 0
    _zero_index: Optional[int] = None

    def __eq__(self, __value) -> bool:
        if __value:
            return __value.state == self.state
        else:
            return False

    def __lt__(self, __value) -> bool:
        return self.id < __value.id

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

    def __post_init__(self):
        self._index_by_val = {}
        for index, val in enumerate(self._goal_state):
            self._index_by_val[val] = (index // NUM_COLS, index % NUM_COLS)

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

    def _manhattan_distance(self, state: tuple[int]) -> int:
        distance = 0
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                index = i * NUM_COLS + j
                val = state[index]
                i1, j1 = self._index_by_val[val]
                distance += abs(i - i1) + abs(j - j1)
        return distance

    def _a_star_search_manhattan(self, init_state: tuple[int]):

        number_of_nodes = 0
        root_node = Node(state=init_state, id=number_of_nodes)
        frontier = queue.PriorityQueue()
        init_distance = self._manhattan_distance(init_state)
        frontier.put((init_distance, root_node))

        while not frontier.empty():
            dist, current_node = frontier.get()
            if self._is_solved(current_node):
                return current_node
            for action in self._actions:
                neighbor_node = current_node.apply_action(action)
                if neighbor_node:
                    number_of_nodes += 1
                    neighbor_node.id = number_of_nodes
                    distance_to_goal = (
                        self._manhattan_distance(neighbor_node.state)
                        + current_node.depth
                    )
                    frontier.put((distance_to_goal, neighbor_node))

    def solve(self, init_state: list[int], approach) -> list[str]:
        if approach == "dfs":
            node = self._depth_first_search(init_state, 30, 10_000_00)
        elif approach == "a*":
            node = self._a_star_search_manhattan(init_state)

        result = []
        if node:
            while node.parent:
                result.append(node.action)
                node = node.parent
        return result[::-1]
