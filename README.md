# Sudoku Solver

A clean, automated Sudoku Solver application built with standard Python and `tkinter`. It solves any valid 9x9 Sudoku puzzle using the standard recursive backtracking algorithm.

---

## Features

- **Standard Backtracking Algorithm:** Efficiently solves 9x9 Sudoku puzzles using simple, clean recursive constraint satisfaction.
- **Desktop Graphical Interface (GUI):** Easy-to-use dark-themed graphical interface built with standard `tkinter`.
- **Keyboard Navigation:** Use arrow keys (Up, Down, Left, Right) and number keys (1-9) to input numbers smoothly.
- **Preset Puzzles:** Includes preset puzzles for Easy, Medium, Hard, Expert, and World's Hardest.
- **Board Validation:** Automatically verifies that initial numbers follow all Sudoku rules (no duplicates in rows, columns, or 3x3 boxes).
- **Interactive CLI Mode:** Command-line mode to solve presets or custom 81-character puzzle strings in the terminal.
- **Pure Standard Python:** 100% standard library code with zero external pip dependencies.
- **Automated Unit Tests:** Tested with Python's built-in `unittest`.

---

## Installation & Requirements

### Requirements
- Python 3.8 or newer (No pip packages required)

---

## How to Run

### 1. Run Desktop GUI (Default)
```bash
python main.py
```

### 2. Run Interactive Command Line (CLI)
```bash
python main.py --cli
```

---

## Project Structure

```
PRODIGY_SD_04/
├── solver.py            # Core backtracking logic, validation, and preset puzzles
├── app_gui.py           # Desktop GUI interface (Tkinter)
├── main.py              # Main entry point (GUI & CLI support)
├── test_sudoku.py       # Automated unit tests
├── requirements.txt     # Python standard library note
├── .gitignore           # Standard git ignore file
└── README.md            # Project documentation
```

---

## Running Unit Tests

```bash
python -m unittest test_sudoku.py -v
```

---

## License
MIT License
