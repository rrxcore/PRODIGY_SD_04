"""
Sudoku Solver Engine (Standard Python)
Implements standard backtracking algorithm for solving 9x9 Sudoku puzzles.
"""

import time
import copy


def is_valid(grid, row, col, number):
    """
    Check if placing 'number' at grid[row][col] is valid according to Sudoku rules:
    1. The number must not already exist in the same row.
    2. The number must not already exist in the same column.
    3. The number must not already exist in the 3x3 subgrid.
    """
    # 1. Check Row
    for c in range(9):
        if c != col and grid[row][c] == number:
            return False

    # 2. Check Column
    for r in range(9):
        if r != row and grid[r][col] == number:
            return False

    # 3. Check 3x3 Subgrid (Box)
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != row or c != col) and grid[r][c] == number:
                return False

    return True


def find_empty(grid):
    """
    Find the next empty cell (value 0) on the board.
    Returns (row, col) tuple, or None if the board is completely filled.
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return (r, c)
    return None


def solve_sudoku(grid):
    """
    Solves a 9x9 Sudoku grid using the standard recursive backtracking algorithm.
    Modifies the grid in-place and returns True if solved, False if unsolvable.
    """
    empty_cell = find_empty(grid)
    
    # Base Case: No empty cells left, puzzle is solved!
    if empty_cell is None:
        return True

    row, col = empty_cell

    # Try digits from 1 to 9
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            # Place the number
            grid[row][col] = num

            # Recursively try to solve the rest of the board
            if solve_sudoku(grid):
                return True

            # If it leads to no solution, backtrack (reset cell to 0)
            grid[row][col] = 0

    return False


def validate_board(grid):
    """
    Validates that the input grid is a 9x9 matrix and has no conflicting initial clues.
    Returns (is_valid: bool, message: str).
    """
    if len(grid) != 9:
        return False, "Grid must have exactly 9 rows."

    for r in range(9):
        if len(grid[r]) != 9:
            return False, f"Row {r + 1} must have exactly 9 columns."
        for c in range(9):
            val = grid[r][c]
            if not isinstance(val, int) or val < 0 or val > 9:
                return False, f"Invalid value '{val}' at row {r + 1}, column {c + 1}. Must be 0-9."
            if val != 0:
                if not is_valid(grid, r, c, val):
                    return False, f"Conflict: Duplicate number {val} at row {r + 1}, column {c + 1}."

    return True, "Board is valid."


def format_grid(grid):
    """
    Formats the 9x9 grid into a clean, readable ASCII string with borders.
    """
    lines = []
    border = "+-------+-------+-------+"
    for r in range(9):
        if r % 3 == 0:
            lines.append(border)
        row_str = "| "
        for c in range(9):
            val = str(grid[r][c]) if grid[r][c] != 0 else "."
            row_str += val + " "
            if (c + 1) % 3 == 0:
                row_str += "| "
        lines.append(row_str)
    lines.append(border)
    return "\n".join(lines)


def parse_grid_string(text):
    """
    Converts an 81-character string into a 9x9 integer grid.
    Accepts numbers 1-9, and '0' or '.' for empty cells.
    """
    clean_chars = [c for c in text if c.isdigit() or c in ". "]
    digits = []
    for c in clean_chars:
        if c in ". ":
            digits.append(0)
        elif c.isdigit():
            digits.append(int(c))

    if len(digits) != 81:
        raise ValueError(f"Expected 81 digits, but received {len(digits)}.")

    grid = []
    for i in range(9):
        grid.append(digits[i * 9 : (i + 1) * 9])
    return grid


# Sample Preset Puzzles
PRESET_PUZZLES = {
    "Easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "Medium": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ],
    "Hard": [
        [0, 0, 0, 0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 3, 5, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 7, 0],
        [7, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 4, 0, 0, 8, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 4, 0],
        [0, 5, 0, 0, 0, 0, 6, 0, 0]
    ],
    "Expert": [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ],
    "World's Hardest": [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
}
