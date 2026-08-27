"""
PRODIGY_SD_04: Sudoku Solver - Desktop Graphical Interface
Modern, responsive Obsidian Dark UI built purely with standard Python tkinter.
Features 9x9 interactive grid, number pad, difficulty presets, live stats, and keyboard navigation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy
from solver import is_valid, solve_sudoku, validate_board, PRESET_PUZZLES


class ModernSudokuApp:
    # --- Modern Slate & Emerald Color Palette ---
    COLOR_BG_DARK = "#0F172A"       # Slate 900
    COLOR_BG_CARD = "#1E293B"       # Slate 800
    COLOR_BG_CARD_LIGHT = "#283548" # Slate 750
    COLOR_BORDER = "#334155"        # Slate 700
    COLOR_BORDER_THICK = "#64748B"  # Slate 500 (3x3 grid dividers)
    
    COLOR_CELL_1 = "#1E293B"        # Alternating box 1
    COLOR_CELL_2 = "#172033"        # Alternating box 2
    COLOR_CELL_HOVER = "#2D3D54"    # Cell hover
    COLOR_CELL_SELECTED = "#3B82F6" # Selection border
    COLOR_CELL_RELATED = "#233044"  # Highlight row/col/box
    
    COLOR_TEXT_WHITE = "#F8FAFC"
    COLOR_TEXT_MUTED = "#94A3B8"
    COLOR_TEXT_DIM = "#64748B"
    
    COLOR_CLUE = "#38BDF8"          # Sky Blue (Original given numbers)
    COLOR_SOLVED = "#34D399"        # Emerald Green (Solved numbers)
    COLOR_CONFLICT = "#F87171"      # Coral Red (Conflicts)
    COLOR_HIGHLIGHT = "#FBBF24"     # Amber / Gold
    
    COLOR_BTN_SOLVE = "#10B981"     # Emerald 500
    COLOR_BTN_SOLVE_HOVER = "#059669"
    COLOR_BTN_SEC = "#334155"
    COLOR_BTN_SEC_HOVER = "#475569"
    COLOR_BTN_DANGER = "#EF4444"
    COLOR_BTN_DANGER_HOVER = "#DC2626"

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("840x680")
        self.root.minsize(780, 620)
        self.root.configure(bg=self.COLOR_BG_DARK)

        # State Variables
        self.cell_entries = [[None for _ in range(9)] for _ in range(9)]
        self.cell_vars = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.initial_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_pos = None  # (row, col)

        self._setup_ttk_styles()
        self._build_header()
        self._build_main_body()
        self._build_footer_status()
        
        # Load default puzzle
        self.load_preset("Easy")

    def _setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Custom Combobox Style
        style.configure(
            "Custom.TCombobox",
            fieldbackground=self.COLOR_BG_CARD_LIGHT,
            background=self.COLOR_BORDER,
            foreground=self.COLOR_TEXT_WHITE,
            arrowcolor=self.COLOR_CLUE,
            darkcolor=self.COLOR_BG_CARD,
            lightcolor=self.COLOR_BG_CARD
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", self.COLOR_BG_CARD_LIGHT)],
            foreground=[("readonly", self.COLOR_TEXT_WHITE)]
        )

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=self.COLOR_BG_DARK, pady=12, padx=25)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="Sudoku Solver",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLOR_BG_DARK,
            fg=self.COLOR_TEXT_WHITE
        )
        title_lbl.pack(anchor="w")

    def _build_main_body(self):
        container = tk.Frame(self.root, bg=self.COLOR_BG_DARK, padx=25, pady=5)
        container.pack(fill=tk.BOTH, expand=True)

        # Left Column: 9x9 Sudoku Board Container
        left_col = tk.Frame(container, bg=self.COLOR_BG_DARK)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))

        self._build_grid_board(left_col)

        # Right Column: Side Control Card (Presets, Quick Numpad, Action Buttons, Stats)
        right_col = tk.Frame(container, bg=self.COLOR_BG_CARD, bd=1, relief=tk.SOLID)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_sidebar_controls(right_col)

    def _build_grid_board(self, parent):
        # Outer thick border frame
        board_outer = tk.Frame(parent, bg=self.COLOR_BORDER_THICK, bd=3, relief=tk.SOLID)
        board_outer.pack(pady=5)

        for r in range(9):
            for c in range(9):
                # 3x3 Block Thicker Boundaries
                pad_top = 3 if (r % 3 == 0 and r != 0) else 1
                pad_left = 3 if (c % 3 == 0 and c != 0) else 1

                # Alternating 3x3 block background colors for visual clarity
                box_r, box_c = r // 3, c // 3
                cell_bg = self.COLOR_CELL_1 if (box_r + box_c) % 2 == 0 else self.COLOR_CELL_2

                cell_frame = tk.Frame(board_outer, bg=self.COLOR_BORDER)
                cell_frame.grid(row=r, column=c, padx=(pad_left, 1), pady=(pad_top, 1))

                entry = tk.Entry(
                    cell_frame,
                    textvariable=self.cell_vars[r][c],
                    font=("Segoe UI", 16, "bold"),
                    justify="center",
                    width=2,
                    bg=cell_bg,
                    fg=self.COLOR_CLUE,
                    insertbackground=self.COLOR_CLUE,
                    relief=tk.FLAT,
                    bd=0,
                    highlightthickness=0
                )
                entry.pack(padx=2, pady=2, ipady=5)

                # Key & Mouse bindings
                entry.bind("<KeyRelease>", lambda e, row=r, col=c: self._on_cell_type(e, row, col))
                entry.bind("<FocusIn>", lambda e, row=r, col=c: self._on_cell_focus(row, col))
                entry.bind("<Up>", lambda e, row=r, col=c: self._navigate_focus(row - 1, col))
                entry.bind("<Down>", lambda e, row=r, col=c: self._navigate_focus(row + 1, col))
                entry.bind("<Left>", lambda e, row=r, col=c: self._navigate_focus(row, col - 1))
                entry.bind("<Right>", lambda e, row=r, col=c: self._navigate_focus(row, col + 1))

                self.cell_entries[r][c] = entry

    def _build_sidebar_controls(self, parent):
        inner = tk.Frame(parent, bg=self.COLOR_BG_CARD, padx=18, pady=16)
        inner.pack(fill=tk.BOTH, expand=True)

        # 1. Preset Puzzles Section
        self._make_section_label(inner, "DIFFICULTY PRESETS")
        
        preset_row = tk.Frame(inner, bg=self.COLOR_BG_CARD)
        preset_row.pack(fill=tk.X, pady=(0, 14))

        self.preset_combo = ttk.Combobox(
            preset_row,
            values=list(PRESET_PUZZLES.keys()),
            state="readonly",
            font=("Segoe UI", 10),
            style="Custom.TCombobox"
        )
        self.preset_combo.set("Easy")
        self.preset_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.preset_combo.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_combo.get()))

        load_btn = self._create_button(
            preset_row,
            text="Load",
            bg=self.COLOR_BTN_SEC,
            hover_bg=self.COLOR_BTN_SEC_HOVER,
            command=lambda: self.load_preset(self.preset_combo.get()),
            font_size=9,
            pady=3,
            padx=12
        )
        load_btn.pack(side=tk.RIGHT)

        # Divider
        tk.Frame(inner, bg=self.COLOR_BORDER, height=1).pack(fill=tk.X, pady=(0, 14))

        # 2. Main Actions Section
        self._make_section_label(inner, "SOLVE & VALIDATE")

        self.solve_btn = self._create_button(
            inner,
            text="⚡ Solve Puzzle",
            bg=self.COLOR_BTN_SOLVE,
            hover_bg=self.COLOR_BTN_SOLVE_HOVER,
            command=self.solve_grid,
            font_size=11,
            bold=True,
            pady=8
        )
        self.solve_btn.pack(fill=tk.X, pady=(0, 8))

        val_reset_row = tk.Frame(inner, bg=self.COLOR_BG_CARD)
        val_reset_row.pack(fill=tk.X, pady=(0, 14))

        val_btn = self._create_button(
            val_reset_row,
            text="✓ Validate Board",
            bg=self.COLOR_BTN_SEC,
            hover_bg=self.COLOR_BTN_SEC_HOVER,
            command=self.validate_grid,
            font_size=9,
            pady=5
        )
        val_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        reset_btn = self._create_button(
            val_reset_row,
            text="↺ Reset Clues",
            bg=self.COLOR_BTN_SEC,
            hover_bg=self.COLOR_BTN_SEC_HOVER,
            command=self.reset_to_clues,
            font_size=9,
            pady=5
        )
        reset_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # Divider
        tk.Frame(inner, bg=self.COLOR_BORDER, height=1).pack(fill=tk.X, pady=(0, 12))

        # 3. Interactive On-Screen Keypad
        self._make_section_label(inner, "QUICK KEYPAD")

        numpad_frame = tk.Frame(inner, bg=self.COLOR_BG_CARD)
        numpad_frame.pack(fill=tk.X, pady=(0, 14))

        # 3x3 Digits
        for i in range(9):
            num = str(i + 1)
            btn = self._create_button(
                numpad_frame,
                text=num,
                bg=self.COLOR_BG_CARD_LIGHT,
                hover_bg=self.COLOR_BTN_SEC_HOVER,
                command=lambda n=num: self._input_digit_to_selected(n),
                font_size=11,
                bold=True,
                pady=4
            )
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2, sticky="nsew")
            numpad_frame.columnconfigure(i % 3, weight=1)

        # Clear Digit & Clear Board Row
        keypad_bot = tk.Frame(inner, bg=self.COLOR_BG_CARD)
        keypad_bot.pack(fill=tk.X, pady=(0, 14))

        erase_btn = self._create_button(
            keypad_bot,
            text="⌫ Erase Cell",
            bg=self.COLOR_BTN_SEC,
            hover_bg=self.COLOR_BTN_SEC_HOVER,
            command=lambda: self._input_digit_to_selected(""),
            font_size=9,
            pady=4
        )
        erase_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        clear_all_btn = self._create_button(
            keypad_bot,
            text="🗑 Clear Board",
            bg=self.COLOR_BTN_SEC,
            hover_bg=self.COLOR_BTN_DANGER,
            command=self.clear_all,
            font_size=9,
            pady=4
        )
        clear_all_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # 4. Live Puzzle Statistics Card
        stats_card = tk.Frame(inner, bg=self.COLOR_BG_DARK, bd=1, relief=tk.SOLID, padx=10, pady=8)
        stats_card.pack(fill=tk.X, side=tk.BOTTOM)

        self.stat_clues_lbl = tk.Label(
            stats_card,
            text="Clues: 0 / 81",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG_DARK,
            fg=self.COLOR_TEXT_MUTED
        )
        self.stat_clues_lbl.pack(side=tk.LEFT)

        self.stat_time_lbl = tk.Label(
            stats_card,
            text="Solve Time: --",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG_DARK,
            fg=self.COLOR_SOLVED
        )
        self.stat_time_lbl.pack(side=tk.RIGHT)

    def _make_section_label(self, parent, text):
        lbl = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_BG_CARD,
            fg=self.COLOR_CLUE
        )
        lbl.pack(anchor="w", pady=(0, 6))

    def _create_button(self, parent, text, bg, hover_bg, command, font_size=10, bold=False, pady=6, padx=8):
        weight = "bold" if bold else "normal"
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", font_size, weight),
            bg=bg,
            fg=self.COLOR_TEXT_WHITE,
            activebackground=hover_bg,
            activeforeground=self.COLOR_TEXT_WHITE,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            pady=pady,
            padx=padx,
            command=command
        )
        # Hover animations
        btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.config(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, orig=bg: b.config(bg=orig))
        return btn

    def _build_footer_status(self):
        self.status_bar = tk.Label(
            self.root,
            text="Ready. Select a preset or type digits (1-9) directly onto the grid.",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG_CARD,
            fg=self.COLOR_TEXT_MUTED,
            anchor="w",
            padx=20,
            pady=7,
            bd=1,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # --- Grid Interaction & Styling ---

    def _on_cell_focus(self, row, col):
        self.selected_pos = (row, col)
        self._refresh_board_highlights()

    def _on_cell_type(self, event, row, col):
        val = self.cell_vars[row][col].get().strip()
        if len(val) > 1:
            val = val[-1]

        if val in "123456789":
            self.cell_vars[row][col].set(val)
            self.cell_entries[row][col].config(fg=self.COLOR_CLUE)
            # Auto-advance to next cell on number input
            if event.keysym in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                next_c = (col + 1) % 9
                next_r = row + 1 if next_c == 0 else row
                if next_r < 9:
                    self._navigate_focus(next_r, next_c)
        else:
            self.cell_vars[row][col].set("")

        self._update_stats()
        self._refresh_board_highlights()

    def _input_digit_to_selected(self, digit):
        if self.selected_pos:
            r, c = self.selected_pos
            self.cell_vars[r][c].set(digit)
            self.cell_entries[r][c].config(fg=self.COLOR_CLUE)
            self._update_stats()
            self._refresh_board_highlights()
            # Advance to next cell if number was added
            if digit != "":
                next_c = (c + 1) % 9
                next_r = r + 1 if next_c == 0 else r
                if next_r < 9:
                    self._navigate_focus(next_r, next_c)

    def _navigate_focus(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            self.cell_entries[row][col].focus_set()
            self._on_cell_focus(row, col)

    def _refresh_board_highlights(self):
        curr_val = ""
        if self.selected_pos:
            sr, sc = self.selected_pos
            curr_val = self.cell_vars[sr][sc].get().strip()

        for r in range(9):
            for c in range(9):
                box_r, box_c = r // 3, c // 3
                default_bg = self.COLOR_CELL_1 if (box_r + box_c) % 2 == 0 else self.COLOR_CELL_2
                
                # Check relation to selected cell
                if self.selected_pos and (r, c) == self.selected_pos:
                    self.cell_entries[r][c].config(bg=self.COLOR_CELL_HOVER)
                elif self.selected_pos and (r == self.selected_pos[0] or c == self.selected_pos[1] or (box_r == self.selected_pos[0] // 3 and box_c == self.selected_pos[1] // 3)):
                    self.cell_entries[r][c].config(bg=self.COLOR_CELL_RELATED)
                else:
                    self.cell_entries[r][c].config(bg=default_bg)

    def _update_stats(self):
        grid = self.get_current_grid()
        filled = sum(1 for r in range(9) for c in range(9) if grid[r][c] != 0)
        self.stat_clues_lbl.config(text=f"Cells Filled: {filled} / 81")

    # --- Core Board Operations ---

    def get_current_grid(self):
        grid = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cell_vars[r][c].get().strip()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid

    def set_grid_display(self, grid, is_clue_mask=None):
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                self.cell_vars[r][c].set(str(val) if val != 0 else "")
                
                if is_clue_mask and is_clue_mask[r][c]:
                    self.cell_entries[r][c].config(fg=self.COLOR_CLUE)
                elif val != 0:
                    self.cell_entries[r][c].config(fg=self.COLOR_SOLVED)
                else:
                    self.cell_entries[r][c].config(fg=self.COLOR_TEXT_WHITE)
        self._update_stats()
        self._refresh_board_highlights()

    def load_preset(self, name):
        if name in PRESET_PUZZLES:
            grid = PRESET_PUZZLES[name]
            self.initial_grid = copy.deepcopy(grid)
            clue_mask = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]
            self.set_grid_display(grid, clue_mask)
            self.stat_time_lbl.config(text="Solve Time: --", fg=self.COLOR_SOLVED)
            self.status_bar.config(
                text=f"Loaded '{name}' puzzle preset. Click 'Solve Puzzle' to execute backtracking.",
                fg=self.COLOR_CLUE
            )

    def validate_grid(self):
        grid = self.get_current_grid()
        is_ok, message = validate_board(grid)
        if is_ok:
            self.status_bar.config(text="✓ " + message + " Ready to solve.", fg=self.COLOR_SOLVED)
            messagebox.showinfo("Board Valid", "The board layout satisfies all Sudoku constraints.")
        else:
            self.status_bar.config(text="⚠ " + message, fg=self.COLOR_CONFLICT)
            messagebox.showwarning("Rule Conflict", message)

    def solve_grid(self):
        grid = self.get_current_grid()
        is_ok, message = validate_board(grid)
        if not is_ok:
            messagebox.showerror("Cannot Solve", message)
            return

        clue_mask = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]
        solve_copy = copy.deepcopy(grid)

        start_time = time.perf_counter()
        solved = solve_sudoku(solve_copy)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if solved:
            self.set_grid_display(solve_copy, clue_mask)
            self.stat_time_lbl.config(text=f"Solve Time: {elapsed_ms:.2f}ms", fg=self.COLOR_SOLVED)
            self.status_bar.config(
                text=f"✓ Solved successfully in {elapsed_ms:.2f} ms using recursive backtracking!",
                fg=self.COLOR_SOLVED
            )
        else:
            self.stat_time_lbl.config(text="Unsolvable", fg=self.COLOR_CONFLICT)
            self.status_bar.config(
                text="❌ No solution exists for this Sudoku puzzle.",
                fg=self.COLOR_CONFLICT
            )
            messagebox.showinfo("Unsolvable", "No valid configuration satisfies all Sudoku rules for this board.")

    def reset_to_clues(self):
        clue_mask = [[self.initial_grid[r][c] != 0 for c in range(9)] for r in range(9)]
        self.set_grid_display(self.initial_grid, clue_mask)
        self.stat_time_lbl.config(text="Solve Time: --", fg=self.COLOR_SOLVED)
        self.status_bar.config(text="Board reset to original puzzle clues.", fg=self.COLOR_TEXT_MUTED)

    def clear_all(self):
        empty_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_grid = copy.deepcopy(empty_grid)
        self.set_grid_display(empty_grid)
        self.stat_time_lbl.config(text="Solve Time: --", fg=self.COLOR_SOLVED)
        self.status_bar.config(text="Grid cleared completely. Type your custom numbers.", fg=self.COLOR_TEXT_MUTED)


def launch_gui():
    root = tk.Tk()
    app = ModernSudokuApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
