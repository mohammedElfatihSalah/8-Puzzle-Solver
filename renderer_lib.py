import dataclasses
import math
import pygame

NUM_COLS = 3
NUM_ROWS = 3


@dataclasses.dataclass
class DisplayInfo:
    window_width: int = 640
    window_height: int = 480
    margin: tuple = (40, 40)
    tile_size: int = 50
    gap_size: int = 10
    bg_color: tuple = (0, 0, 0)
    tile_color: tuple = (128, 255, 255)
    button_width: int = 80
    button_height: int = 40


class Renderer:

    def __init__(self, info):
        self.info = info
        self.clock = pygame.time.Clock()

        # Create Rect for `Solve` button
        tile_size = self.info.tile_size + self.info.gap_size
        x = self.info.margin[0] + NUM_COLS * tile_size + self.info.button_width
        y = self.info.margin[1] + NUM_ROWS * tile_size - self.info.button_height

        self.solve_button_rect = pygame.Rect(
            x, y, self.info.button_width, self.info.button_height
        )

    def init_display(self):
        self.surface = pygame.display.set_mode(
            (self.info.window_width, self.info.window_height)
        )
        self.surface.fill(self.info.bg_color)

    def is_outside(self, x, y) -> bool:
        relative_x, relative_y = x - self.info.margin[0], y - self.info.margin[1]
        if relative_x < 0 or relative_y < 0:
            return True

        x_boundary = (self.info.gap_size + self.info.tile_size) * NUM_COLS
        y_boundary = (self.info.gap_size + self.info.tile_size) * NUM_ROWS

        if relative_x > x_boundary or relative_y > y_boundary:
            return True

        return False

    def is_on_gap(self, x, y) -> bool:
        if self.is_outside(x, y):
            return False

        relative_x, relative_y = x - self.info.margin[0], y - self.info.margin[1]
        size = self.info.gap_size + self.info.tile_size

        x_remainder = relative_x % size
        if x_remainder == 0 or x_remainder > self.info.tile_size:
            return True

        y_remainder = relative_y % size
        if y_remainder == 0 or y_remainder > self.info.tile_size:
            return True

        return False

    def is_solve_button_clicked(self, pos: tuple) -> bool:
        return self.solve_button_rect.collidepoint(pos)

    def convert_to_game_coordinate(self, x, y) -> tuple:

        relative_x, relative_y = x - self.info.margin[0], y - self.info.margin[1]
        step = self.info.gap_size + self.info.tile_size

        def get_index(val, size):
            if val == 0:
                return 0
            index = val // size
            if val % step == 0:
                index -= 1
            return index

        game_y = get_index(relative_x, step)
        game_x = get_index(relative_y, step)

        return (game_x, game_y)

    def draw_tile(self, x, y, number):
        if number == 0:
            return
        pygame.draw.rect(
            self.surface,
            self.info.tile_color,
            (x, y, self.info.tile_size, self.info.tile_size),
            width=3,
        )
        font = pygame.font.Font(None, 36)
        text = font.render(str(number), True, (255, 255, 255))
        rect = text.get_rect(
            center=(x + self.info.tile_size // 2, y + self.info.tile_size // 2)
        )
        self.surface.blit(text, rect)
        pygame.display.update()

    def draw_empty_tile(self, x, y):
        pygame.draw.rect(
            self.surface,
            self.info.bg_color,
            (x, y, self.info.tile_size, self.info.tile_size),
        )

    def draw_solve_button(self):
        pygame.draw.rect(
            self.surface,
            (15, 255, 80),
            self.solve_button_rect,
            width=3,
            border_radius=20,
        )
        font = pygame.font.Font(None, 28)
        text_surface = font.render("Solve", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.solve_button_rect.center)
        self.surface.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_board(self, numbers):
        step = self.info.gap_size + self.info.tile_size
        xb, yb = self.info.margin

        for i in range(len(numbers)):
            y = yb + i * step
            for j in range(len(numbers[0])):
                x = xb + j * step
                self.draw_tile(x, y, numbers[i][j])

        self.draw_solve_button()

    def convert_from_game_coordinate(self, x, y):
        step = self.info.gap_size + self.info.tile_size

        y_env = x * step + self.info.margin[1]
        x_env = y * step + self.info.margin[0]

        return x_env, y_env

    def move_animation(self, number, begin, end):
        x, y = begin
        xb, yb = self.convert_from_game_coordinate(x, y)

        x, y = end
        xe, ye = self.convert_from_game_coordinate(x, y)

        if xe == xb and yb == ye:
            return

        speed = 10
        if xe == xb:
            if yb > ye:
                while yb > ye:
                    self.draw_empty_tile(xb, yb)
                    yb -= speed
                    if yb < ye:
                        yb = ye
                    self.draw_tile(xb, yb, number)
                    self.clock.tick(30)
                    pygame.display.update()
            elif yb < ye:
                while yb < ye:
                    self.draw_empty_tile(xb, yb)
                    yb += speed
                    if yb > ye:
                        yb = ye
                    self.draw_tile(xb, yb, number)
                    self.clock.tick(30)
                    pygame.display.update()
        if ye == yb:
            if xb > xe:
                while xb > xe:
                    self.draw_empty_tile(xb, yb)
                    xb -= speed
                    if xb < xe:
                        xb = xe
                    self.draw_tile(xb, yb, number)
                    self.clock.tick(30)
                    pygame.display.update()
            elif xb < xe:
                while xb < xe:
                    self.draw_empty_tile(xb, yb)
                    xb += speed
                    if xb > xe:
                        xb = xe
                    self.draw_tile(xb, yb, number)
                    self.clock.tick(30)
                    pygame.display.update()
