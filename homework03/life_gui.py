import pygame
from life import GameOfLife
from life_console import UI


class GUI(UI):
    """ the gui version for the game of life business logic model """

    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 5) -> None:
        super().__init__(life)

        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        # Устанавливаем размер окна
        self.screen_size = self.width, self.height  # type: ignore
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        # self.life.cols = self.width // self.cell_size
        # self.life.rows = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.life.curr_generation = self.life.create_grid(True)
        self.cell_size = cell_size

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for col in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (col, 0), (col, self.height))
        for row in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, row), (self.width, row))

    def draw_grid(self) -> None:
        """ draws the coloured cells in an opened up window """

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
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    pause = True
                while pause:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos = pygame.mouse.get_pos()
                        cell_row = mouse_pos[1] // self.cell_size
                        cell_col = mouse_pos[0] // self.cell_size
                        self.life.curr_generation[cell_row][cell_col] = 1
                        self.draw_grid()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
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
