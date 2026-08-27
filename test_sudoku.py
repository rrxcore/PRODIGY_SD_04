"""
Automated Unit Tests for Sudoku Solver
"""

import unittest
import copy
from solver import is_valid, solve_sudoku, validate_board, parse_grid_string, PRESET_PUZZLES


class TestSudoku(unittest.TestCase):

    def test_is_valid_row_and_column(self):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        grid[0][0] = 5

        # Row check (duplicate in same row)
        self.assertFalse(is_valid(grid, 0, 4, 5))

        # Column check (duplicate in same column)
        self.assertFalse(is_valid(grid, 4, 0, 5))

        # 3x3 box check (duplicate in same 3x3 box)
        self.assertFalse(is_valid(grid, 1, 1, 5))

        # Valid placement
        self.assertTrue(is_valid(grid, 3, 3, 5))

    def test_solve_easy_puzzle(self):
        grid = copy.deepcopy(PRESET_PUZZLES["Easy"])
        solved = solve_sudoku(grid)
        self.assertTrue(solved)

        # Check all cells are filled with numbers 1-9
        for row in grid:
            self.assertNotIn(0, row)
            self.assertEqual(len(set(row)), 9)

    def test_solve_expert_puzzle(self):
        grid = copy.deepcopy(PRESET_PUZZLES["Expert"])
        solved = solve_sudoku(grid)
        self.assertTrue(solved)

    def test_solve_worlds_hardest(self):
        grid = copy.deepcopy(PRESET_PUZZLES["World's Hardest"])
        solved = solve_sudoku(grid)
        self.assertTrue(solved)

    def test_invalid_initial_board(self):
        # Two identical numbers in the same row
        grid = [[0 for _ in range(9)] for _ in range(9)]
        grid[0][0] = 7
        grid[0][1] = 7
        is_ok, _ = validate_board(grid)
        self.assertFalse(is_ok)

    def test_string_parser(self):
        puzzle_str = (
            "530070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        grid = parse_grid_string(puzzle_str)
        self.assertEqual(len(grid), 9)
        self.assertEqual(grid[0][0], 5)
        self.assertEqual(grid[8][8], 9)


if __name__ == "__main__":
    unittest.main()
