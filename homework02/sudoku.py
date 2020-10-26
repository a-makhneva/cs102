import random

from typing import Tuple, List, Set, Optional
import typing as tp

T = tp.TypeVar("T")


def create_grid(puzzle: str) -> List[List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    # def group(values: List[int], n: int) -> List[List[int]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    final = []
    for i in range((len(values) + n - 1) // n):
        r1 = values[(i * n): ((i + 1) * n)]
        final.append(r1)
    return final


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    num = pos[0]
    row = grid[num]
    return row


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    num = pos[1]
    b = []
    for i in range(len(grid[0])):
        myrow = grid[i]
        b.append(myrow[num])
    return b


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    bigrow = pos[0] // 3
    bigcol = pos[1] // 3
    final = []
    for i in range(bigrow * 3, bigrow * 3 + 3):
        myrow = grid[i]
        for j in range(bigcol * 3, bigcol * 3 + 3):
            final.append(myrow[j])
    return final


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    x = (-1, -1)  # not found
    for i in range(len(grid)):
        myrow = grid[i]

        for j in range(len(myrow)):
            if myrow[j] == '.':
                x = (i, j)
                return x

    return x


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    p = set('123456789')
    result = set()
    for i in p:
        if (get_block(grid, pos).count(i) == 0) and (get_row(grid, pos).count(i) == 0) and (
                get_col(grid, pos).count(i) == 0):
            result.add(i)
    return result


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """Как решать Судоку? 
    1. Найти свободную позицию 
    2. Найти все возможные значения, которые могут находиться на 
    этой позиции 
    3. Для каждого возможного значения: 
        3.1. Поместить это значение на эту позицию 
        3.2. Продолжить решать оставшуюся часть пазла 
        >>> grid = read_sudoku('puzzle1.txt') 
        >>> solve(grid) 
        [['5', '3', '4', '6', '7', '8', '9', '1', '2'], 
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'], 
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'], 
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'], 
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'], 
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'], 
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'], 
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'], 
        ['3', '4', '5', '2', '8', '6', '1', '7', '9']] """

    solve_sudoku(grid)

    if find_empty_positions(grid) != (-1, -1):
        return None  # if the puzzle is unsolvable

    return grid


def solve_sudoku(grid, i=0, j=0) -> bool:
    i, j = find_empty_positions(grid)
    if i == -1:
        return True  # all pos are filled
    for e in find_possible_values(grid, (i, j)):
        grid[i][j] = e
        if solve_sudoku(grid, i, j):
            return True
        grid[i][j] = '.'  # go back

    return False


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles

    for i in range(0, 9):
        for j in range(0, 9):
            for k in set('123456789'):
                pos = (i, j)
                if (get_block(solution, pos).count(k) != 1) or (get_row(solution, pos).count(k) != 1) or (
                        get_col(solution, pos).count(k) != 1):
                    return False
    return True


def find_random_place(grid: List[List[str]]) -> Tuple[int, int]:
    x = random.randrange(0, 9)
    y = random.randrange(0, 9)
    return x, y


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = []
    for i in range(9):
        grid.append(["."] * 9)

    grid = solve(grid)
    numplaces = 81-N  # number of places to be assigned a new value
    i=0
    while i < numplaces:
        z = tuple(find_random_place(grid))
        if grid[z[0]][z[1]] != '.':
            newval = "."
            grid[z[0]][z[1]] = newval
            i += 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid_ = read_sudoku(fname)
        display(grid_)
        solution = solve(grid_)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)