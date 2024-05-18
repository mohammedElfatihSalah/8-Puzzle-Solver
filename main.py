import renderer_lib
import solver_lib
import puzzle_lib
import controller as controller_lib
import pygame
from pygame.locals import QUIT
import sys

pygame.init()


puzzle = puzzle_lib.Puzzle()
renderer = renderer_lib.Renderer(renderer_lib.DisplayInfo(margin=(100, 100)))
controller = controller_lib.Controller(puzzle, renderer, solver=solver_lib.Solver())

renderer.init_display()
renderer.draw_board(puzzle.get_tiles())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        else:
            controller.handle_event(event)
