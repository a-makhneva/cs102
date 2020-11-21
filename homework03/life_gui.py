import pygame
from life import GameOfLife
from pygame.locals import *
from life_console import UI

# import pygame_gui
import argparse


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 5) -> None:
        super().__init__(life)
        # parser = argparse.ArgumentParser()
        # parser.add_argument("--height", default=480, help="height of game field in pixels")
        # parser.add_argument("--width", default=640, help="width of game field in pixels")
        # parser.add_argument("--cell_size", default=10, help="cell-size in pixels")
        # parser.add_argument("--rows", type=int, help="number of rows in grid")
        # parser.add_argument("--cols", type=int,  help="number of columns in grid")
        # parser.add_argument("--max_generations", type=int, help="maximum number of generations in the game")
        # args = parser.parse_args()
        self.life = life
        if self.life.args.width:
            self.width = int(self.life.args.width)
        else:
            self.width = self.life.cols * cell_size

        if self.life.args.height:
            self.height = int(self.life.args.height)
        else:
            self.height = self.life.rows * cell_size

        if self.life.args.cell_size:
            self.cell_size = int(self.life.args.cell_size)
        else:
            self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = (
            self.width,
            self.height,
        )  # self.life.cols * cell_size, self.life.rows * cell_size
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.life.cols = self.width // self.cell_size
        self.life.rows = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.life.curr_generation = self.life.create_grid(True)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
        pygame.display.flip()

    def run(self) -> None:
        pause = False
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.life.create_grid()

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # type: ignore
                    running = False

                if event.type == pygame.KEYUP:  # type: ignore
                    pause = True
                while pause:
                    if event.type == pygame.MOUSEBUTTONUP:  # type: ignore
                        mouse_pos = pygame.mouse.get_pos()
                        cell_row = mouse_pos[1] // self.cell_size
                        cell_col = mouse_pos[0] // self.cell_size
                        self.life.curr_generation[cell_row][cell_col] = 1
                        self.draw_grid()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:  # type: ignore
                            pause = not pause

            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.life.step()
            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)
            
if __name__ == "__main__":
    life = GameOfLife((48, 64), True, 50)
    ui = GUI(life)
    ui.run()
