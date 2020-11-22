import pathlib
import random
import typing as tp
import copy
import argparse
import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

T = tp.TypeVar("T")


class GameOfLife:
    """ " game of life business logic separated;
    cli arguments can be used to alter game parameters"""

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ):

        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations  # int(args.max_generations)
        # Текущее число поколений
        self.generations = 1

    def parsing(self):
        """parses the cli arguments and stores them
        to alter game parameters according to user's needs"""

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--rows",
            dest="self.rows",
            action="store",
            type=int,
            help="number of rows in grid",
        )
        parser.add_argument(
            "--cols",
            dest="self.cols",
            action="store",
            type=int,
            help="number of columns in grid",
        )
        parser.add_argument(
            "--max-generations",
            type=int,
            dest="self.max_generations",
            action="store",
            help="maximum number of generations in the game",
        )
        parser.add_argument(
            "--height",
            default=480,
            type=float,
            dest="self.height",
            action="store",
            help="height of game field in pixels",
        )
        parser.add_argument(
            "--width",
            default=640,
            type=float,
            dest="self.width",
            action="store",
            help="width of game field in pixels",
        )
        parser.add_argument(
            "--cell-size",
            default=10,
            type=int,
            dest="self.cell_size",
            action="store",
            help="cell-size in pixels",
        )

        args = parser.parse_args()
        return args
        # if args.rows:
        #     self.rows = int(args.rows)
        # if args.cols:
        #     self.cols = int(args.cols)
        # if args.max_generations:
        #     self.max_generations = args.max_generations

    def create_grid(self, randomize: bool = False) -> Grid:
        """creates a random grid of '1's and '0's to set up
        a random game field"""

        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:  # if true
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    grid[i][j] = random.randrange(0, 2)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """counts the number of neighbours each cell has
        in order to figure out if life should appear or disappear"""

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
        """creates a new life generation (a logical grid)
        based on the number of neighbours a cell has"""

        def group(values: tp.List[T], c_width: int) -> tp.List[tp.List[T]]:
            return [
                values[(i * c_width) : ((i + 1) * c_width)]
                for i in range((len(values) + c_width - 1) // c_width)
            ]

        def alive(mycell: Cell) -> int:
            cur_cell = self.curr_generation[mycell[0]][mycell[1]]
            num_neigh = sum(self.get_neighbours(mycell))
            if (num_neigh == 3) or ((cur_cell == 1) and (num_neigh == 2)):
                return 1
            return 0

        newgrid = [alive((i, j)) for i in range(self.rows) for j in range(self.cols)]
        return group(newgrid, self.cols)

    def step(self) -> None:
        """ makes one game step """

        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        return None

    @property
    def is_max_generations_exceeded(self) -> bool:
        """ checks if the max-generations parameter is exceeded """

        return self.generations >= self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        """checks if the game field is changing or not;
        according to game rules, if there are no changes, the game ends"""
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        new_game = GameOfLife((640, 480), True, 5)

        file = open(filename, "r")
        grid_from_file = file.read()
        file.close()
        new_game.curr_generation = grid_from_file  # type: ignore
        new_game.prev_generation = copy.deepcopy(grid_from_file)  # type: ignore
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        f = open(filename, "w")
        f.write("".join([str(elem) for elem in self.curr_generation]))
        f.close()
