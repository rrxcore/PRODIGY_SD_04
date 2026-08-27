"""
PRODIGY_SD_04: Sudoku Solver Application (Main Entry Point)
Supports launching the Desktop GUI and running in interactive CLI mode.
"""

import sys
import copy
import time
from solver import solve_sudoku, validate_board, format_grid, parse_grid_string, PRESET_PUZZLES


def run_cli():
    print("=" * 45)
    print("            SUDOKU SOLVER (CLI)              ")
    print("=" * 45)
    print("1. Solve Preset Puzzle")
    print("2. Enter Custom Puzzle String (81 digits)")
    print("3. Launch Desktop GUI")
    print("4. Exit")
    print("-" * 45)

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        print("\nAvailable Presets:")
        preset_names = list(PRESET_PUZZLES.keys())
        for i, name in enumerate(preset_names, 1):
            print(f"  {i}. {name}")
        
        sel = input("Select preset number (1-5): ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(preset_names):
            name = preset_names[int(sel) - 1]
            grid = copy.deepcopy(PRESET_PUZZLES[name])
            print(f"\n--- Original Puzzle ({name}) ---")
            print(format_grid(grid))

            start = time.time()
            success = solve_sudoku(grid)
            elapsed = (time.time() - start) * 1000

            if success:
                print(f"\n--- Solved Grid ({elapsed:.2f} ms) ---")
                print(format_grid(grid))
            else:
                print("\n[!] Puzzle is unsolvable.")
        else:
            print("Invalid selection.")

    elif choice == "2":
        print("\nEnter 81 numbers (use 1-9 for numbers, and 0 or '.' for empty cells):")
        puzzle_str = input("> ").strip()
        try:
            grid = parse_grid_string(puzzle_str)
            print("\n--- Input Puzzle ---")
            print(format_grid(grid))

            is_ok, msg = validate_board(grid)
            if not is_ok:
                print(f"\n[!] Invalid Board: {msg}")
                return

            start = time.time()
            success = solve_sudoku(grid)
            elapsed = (time.time() - start) * 1000

            if success:
                print(f"\n--- Solved Grid ({elapsed:.2f} ms) ---")
                print(format_grid(grid))
            else:
                print("\n[!] No solution exists.")
        except Exception as err:
            print(f"Error: {err}")

    elif choice == "3":
        from app_gui import launch_gui
        launch_gui()

    elif choice == "4":
        print("Exiting. Have a great day!")
        sys.exit(0)

    else:
        print("Invalid choice.")


def main():
    # If launched with --cli argument, open CLI mode
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--cli", "-c"]:
        run_cli()
    else:
        # Default: Launch Desktop GUI
        try:
            from app_gui import launch_gui
            launch_gui()
        except Exception as e:
            print(f"GUI not available ({e}). Running in CLI mode instead...")
            run_cli()


if __name__ == "__main__":
    main()
