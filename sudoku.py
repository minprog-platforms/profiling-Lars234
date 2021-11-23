"""
sudoku.py

Minor Programmeren
Lars Disberg

- Changed the given code, so that a sudoku can be solved faster.
"""

from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: dict[int, dict[int, int]] = {}
        col_num = 0
        row_num = 0

        for puzzle_row in puzzle:
            new_row = {}
            col_num = 0
            for value in puzzle_row:
                new_row[col_num] = int(value)
                col_num += 1
            self._grid[row_num] = new_row
            row_num += 1

        # a columnwise variant to speed up column_values
        self._grid_colwise: dict[int, dict[int, int]] = {}
        for row in range(9):
            new_row = {}
            for col in range(9):
                new_row[col] = int(self._grid[col][row])
            self._grid_colwise[row] = new_row

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value
        self._grid_colwise[x][y] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self.place(0, x, y)

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return int(self._grid[y][x])

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Remove all values from the row
        row_val = set(self.row_values(y))
        options = options - row_val

        # Remove all values from the column
        col_val = set(self.column_values(x))
        options = options - col_val

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        block_val = set(self.block_values(block_index))
        options = options - block_val

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            # if no 0 in row, skip
            if 0 in set(self.row_values(y)):
                for x in range(9):
                    if self.value_at(x, y) == 0:
                        return x, y

        return -1, -1

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return list(self._grid[i].values())

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return list(self._grid_colwise[i].values())

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for i in range(9):
            if values != set(self.column_values(i)) or values != set(self.row_values(i)) or values != set(self.block_values(i)):
                return False
        return True

    def __str__(self) -> str:
        representation = ""

        for key in self._grid:
            row = self._grid[key]
            row_ints = list(row.values())
            row_strs = [str(i) for i in row_ints]
            representation += "".join(row_strs + ["\n"])

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
