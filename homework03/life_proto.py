import random
import typing as tp
import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

T = tp.TypeVar("T")


class GameOfLife:
    """ a simple python game of life prototype (gui) """

    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for col in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (col, 0), (col, self.height))
        for row in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, row), (self.width, row))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.create_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        # return None  # type: ignore

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:  # if true
            for i in range(0, self.cell_height):
                for j in range(0, self.cell_width):
                    grid[i][j] = random.randrange(0, 2)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        pygame.init()
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if self.grid[i][j] == 0:
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

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        mycells = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                neighbour_row = cell[0] + i
                neighbour_col = cell[1] + j
                if (
                    (0 <= neighbour_col < self.cell_width)
                    and (0 <= neighbour_row < self.cell_height)
                ) and not (i == 0 and j == 0):
                    # print(neighbour_row, neighbour_col)
                    mycells.append(self.grid[neighbour_row][neighbour_col])
        return mycells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        def group(values: tp.List[T], c_width: int) -> tp.List[tp.List[T]]:
            return [
                values[(i * c_width) : ((i + 1) * c_width)]
                for i in range((len(values) + c_width - 1) // c_width)
            ]

        def alive(mycell: Cell) -> int:
            cur_cell = self.grid[mycell[0]][mycell[1]]
            num_neigh = sum(self.get_neighbours(mycell))

            if (num_neigh == 3) or ((cur_cell == 1) and (num_neigh == 2)):
                return 1
            return 0

        newgrid = [alive((i, j)) for i in range(self.cell_height) for j in range(self.cell_width)]
        return group(newgrid, self.cell_width)


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
