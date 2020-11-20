import abc
import curses
import time
import curses.ascii
from life import GameOfLife
import argparse


class UI(abc.ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.life = life

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        # tst = self.life.rows
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, "*")
                else:
                    screen.addch(i + 1, j + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        win = curses.newwin(self.life.rows + 2, self.life.cols + 2, 1, 1)
        self.draw_borders(win)
        self.draw_grid(win)
        win.refresh()
        time.sleep(5)
        for i in range(0, self.life.max_generations):  # type: ignore
            if self.life.is_changing:
                # self.life.curr_generation = self.life.get_next_generation()
                self.draw_grid(win)
                self.life.step()
                win.refresh()
                time.sleep(3)
            else:
                win.addstr(0, 0, "the positions aren't changing", curses.A_STANDOUT)
                win.refresh()
                time.sleep(7)
                break
        curses.endwin()
