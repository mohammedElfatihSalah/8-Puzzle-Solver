import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN


class Controller:
    def __init__(self, puzzle, renderer, solver):
        self.puzzle = puzzle
        self.renderer = renderer
        self.solver = solver

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            env_x, env_y = event.pos
            if self.renderer.is_solve_button_clicked(event.pos):
                tiles = self.puzzle.get_tiles()
                state = []
                for row in tiles:
                    for val in row:
                        state.append(val)

                state = tuple(state)
                result = self.solver.solve(state, "a*")
                for action in result:
                    number, (x, y), (new_x, new_y) = self.puzzle.move_by_direction(
                        action
                    )
                    self.renderer.move_animation(number, (x, y), (new_x, new_y))
                    pygame.display.update()
            elif self.renderer.is_outside(env_x, env_y):
                return
            elif self.renderer.is_on_gap(env_x, env_y):
                return
            else:
                x, y = self.renderer.convert_to_game_coordinate(env_x, env_y)

                if self.puzzle.is_empty(x, y):
                    return

                number, (x, y), (new_x, new_y) = self.puzzle.move(x, y)
                self.renderer.move_animation(number, (x, y), (new_x, new_y))
