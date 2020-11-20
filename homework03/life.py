import pathlib
import random
import typing as tp
import copy
import argparse

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

T = tp.TypeVar("T")


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:

        # Размер клеточного поля
        self.rows, self.cols = size  # (int(self.args.rows), int(self.args.cols))
        parser = argparse.ArgumentParser()
        parser.add_argument("--rows", type=int, help="number of rows in grid")
        parser.add_argument("--cols", type=int, help="number of columns in grid")
        parser.add_argument(
            "--max_generations", type=int, help="maximum number of generations in the game"
        )
        parser.add_argument("--height", default=480, help="height of game field in pixels")
        parser.add_argument("--width", default=640, help="width of game field in pixels")
        parser.add_argument("--cell_size", default=10, help="cell-size in pixels")
        self.args = parser.parse_args()
        if self.args.rows:
            self.rows = self.args.rows
        if self.args.cols:
            self.cols = self.args.cols

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations  # int(args.max_generations)
        if self.args.max_generations:
            self.max_generations = self.args.max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for i in range(self.rows)]
        if not randomize:  # if false
            return grid
        if randomize:  # if true
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    grid[i][j] = random.randrange(0, 2)
            return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        mycells = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                neighbour_row = cell[0] + i
                neighbour_col = cell[1] + j
                if ((0 <= neighbour_col < self.cols) and (0 <= neighbour_row < self.rows)) and not (
                      i == 0 and j == 0
                ):
                    mycells.append(self.curr_generation[neighbour_row][neighbour_col])
        return mycells

    def get_next_generation(self) -> Grid:
        def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
            return [values[(i * n) : ((i + 1) * n)] for i in range((len(values) + n - 1) // n)]

        def alive(mycell: Cell) -> int:
            cur_cell = self.curr_generation[mycell[0]][mycell[1]]
            num_neigh = sum(self.get_neighbours(mycell))
            if (num_neigh == 3) or ((cur_cell == 1) and (num_neigh == 2)):
                return 1
            else:
                return 0

        newgrid = [alive((i, j)) for i in range(self.rows) for j in range(self.cols)]
        return group(newgrid, self.cols)

    def step(self) -> None:
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        return None

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        new_game = GameOfLife((640, 480), True, 5)

        f = open(filename, "r")
        grid_from_file = f.read()
        f.close()
        new_game.curr_generation = grid_from_file
        new_game.prev_generation = copy.deepcopy(grid_from_file)
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        f = open(filename, "w")
        f.write("".join([str(elem) for elem in self.curr_generation]))
        f.close()
