import tkinter as tk
from tkinter import ttk, messagebox

N = 8
CELL = 64
MARGIN = 28
BOARD = N * CELL

# Colors are deliberately distinct for solution, current move, and conflict.
LIGHT = "#f0eadc"
DARK = "#9eac9c"
ROOK_COLOR = "#20252b"
CURRENT = "#f5d76e"
CONFLICT = "#e86b6b"
SUCCESS = "#91d5a3"
EMPTY = "#ffffff"


class EightRooksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eight Rooks — CSP / Backtracking Visualizer")
        self.root.resizable(False, False)

        self.positions = [-1] * N  # positions[row] = column, or -1
        self.steps = []
        self.step_index = -1
        self.solving = False
        self.after_id = None
        self.speed = tk.IntVar(value=450)
        self.show_attacks = tk.BooleanVar(value=True)

        outer = ttk.Frame(root, padding=14)
        outer.grid(row=0, column=0)

        title = ttk.Label(
            outer, text="EIGHT ROOKS CONSTRAINT SOLVER",
            font=("Helvetica", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 3))
        subtitle = ttk.Label(
            outer,
            text="CSP: one rook per row and column  •  Backtracking search",
            font=("Helvetica", 10)
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.canvas = tk.Canvas(
            outer, width=BOARD + 2 * MARGIN, height=BOARD + 2 * MARGIN,
            bg="#f8f8f8", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0, rowspan=7, padx=(0, 16))
        self.canvas.bind("<Button-1>", self.on_board_click)

        panel = ttk.Frame(outer, width=270)
        panel.grid(row=2, column=1, sticky="n")
        panel.grid_propagate(False)

        ttk.Label(panel, text="Solver controls", font=("Helvetica", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        self.step_btn = ttk.Button(panel, text="Next step  ▶", command=self.next_step)
        self.step_btn.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=3)
        self.prev_btn = ttk.Button(panel, text="◀ Previous", command=self.previous_step)
        self.prev_btn.grid(row=1, column=1, sticky="ew", pady=3)

        self.play_btn = ttk.Button(panel, text="▶ Auto-solve", command=self.toggle_play)
        self.play_btn.grid(row=2, column=0, sticky="ew", padx=(0, 5), pady=3)
        self.reset_btn = ttk.Button(panel, text="Reset", command=self.reset)
        self.reset_btn.grid(row=2, column=1, sticky="ew", pady=3)

        ttk.Label(panel, text="Animation speed").grid(row=3, column=0, sticky="w", pady=(12, 0))
        self.speed_scale = ttk.Scale(
            panel, from_=100, to=1200, orient="horizontal",
            command=self.update_speed
        )
        self.speed_scale.set(450)
        self.speed_scale.grid(row=4, column=0, columnspan=2, sticky="ew")
        ttk.Checkbutton(
            panel, text="Highlight attacked squares",
            variable=self.show_attacks, command=self.draw_board
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 12))

        ttk.Separator(panel).grid(row=6, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Label(panel, text="Search status", font=("Helvetica", 12, "bold")).grid(
            row=7, column=0, columnspan=2, sticky="w", pady=(4, 5)
        )

        self.status_var = tk.StringVar(value="Ready. Press Next step or Auto-solve.")
        self.status_label = ttk.Label(
            panel, textvariable=self.status_var, wraplength=255, justify="left"
        )
        self.status_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.progress_var = tk.StringVar(value="Step: 0 / 0")
        ttk.Label(panel, textvariable=self.progress_var).grid(
            row=9, column=0, columnspan=2, sticky="w"
        )
        self.rook_var = tk.StringVar(value="Rooks placed: 0 / 8")
        ttk.Label(panel, textvariable=self.rook_var).grid(
            row=10, column=0, columnspan=2, sticky="w", pady=(3, 10)
        )

        ttk.Label(panel, text="Legend", font=("Helvetica", 11, "bold")).grid(
            row=11, column=0, columnspan=2, sticky="w"
        )
        self.legend(panel, 12, CURRENT, "Current search position")
        self.legend(panel, 13, CONFLICT, "Conflict / rejected choice")
        self.legend(panel, 14, SUCCESS, "Completed solution")

        ttk.Label(
            panel,
            text="Tip: Click an empty square to try a manual rook placement. "
                 "A placement that shares a row or column is rejected and highlighted.",
            wraplength=255, justify="left"
        ).grid(row=15, column=0, columnspan=2, sticky="w", pady=(14, 0))

        self.generate_steps()
        self.draw_board()

    def legend(self, parent, row, color, text):
        swatch = tk.Canvas(parent, width=18, height=18, highlightthickness=0)
        swatch.create_rectangle(1, 1, 17, 17, fill=color, outline="#555555")
        swatch.grid(row=row, column=0, sticky="w", pady=2)
        ttk.Label(parent, text=text).grid(row=row, column=1, sticky="w", padx=(5, 0))

    def generate_steps(self):
        """Precompute the DFS trace. Each event is one candidate, rejection, or backtrack."""
        events = []
        placed = [-1] * N

        def search(row):
            if row == N:
                events.append({
                    "kind": "solution", "row": None, "col": None,
                    "positions": placed.copy(),
                    "message": "Solution found: eight rooks, no shared rows or columns."
                })
                return True

            for col in range(N):
                events.append({
                    "kind": "try", "row": row, "col": col,
                    "positions": placed.copy(),
                    "message": f"Try row {row + 1}, column {col + 1}."
                })

                # One rook is placed in each earlier row, so only column conflicts remain.
                conflict_row = next(
                    (r for r in range(row) if placed[r] == col), None
                )
                if conflict_row is not None:
                    events.append({
                        "kind": "conflict", "row": row, "col": col,
                        "conflict_row": conflict_row,
                        "positions": placed.copy(),
                        "message": (
                            f"Conflict: column {col + 1} already has a rook "
                            f"in row {conflict_row + 1}. Reject this choice."
                        )
                    })
                    continue

                placed[row] = col
                events.append({
                    "kind": "place", "row": row, "col": col,
                    "positions": placed.copy(),
                    "message": f"Safe placement at row {row + 1}, column {col + 1}."
                })

                if search(row + 1):
                    return True

                # This branch did not work: remove the rook and backtrack.
                placed[row] = -1
                events.append({
                    "kind": "backtrack", "row": row, "col": col,
                    "positions": placed.copy(),
                    "message": f"Backtrack: remove the rook from row {row + 1}, column {col + 1}."
                })
            return False

        search(0)
        self.steps = events
        self.step_index = -1

    def current_event(self):
        if 0 <= self.step_index < len(self.steps):
            return self.steps[self.step_index]
        return None

    def next_step(self):
        if self.solving:
            return
        if self.step_index + 1 >= len(self.steps):
            self.status_var.set("Search trace finished. Reset to replay.")
            return
        self.step_index += 1
        self.apply_event()

    def previous_step(self):
        self.pause()
        if self.step_index < 0:
            return
        self.step_index -= 1
        self.apply_event()

    def apply_event(self):
        event = self.current_event()
        if event is None:
            self.positions = [-1] * N
            self.status_var.set("Ready. Press Next step or Auto-solve.")
            self.progress_var.set(f"Step: 0 / {len(self.steps)}")
        else:
            self.positions = event["positions"].copy()
            self.status_var.set(event["message"])
            if event["kind"] == "solution":
                self.positions = event["positions"].copy()
        self.progress_var.set(f"Step: {self.step_index + 1} / {len(self.steps)}")
        self.rook_var.set(f"Rooks placed: {sum(c >= 0 for c in self.positions)} / 8")
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        # File labels and rank labels.
        for col in range(N):
            x = MARGIN + col * CELL + CELL / 2
            self.canvas.create_text(x, 15, text=chr(ord("A") + col), font=("Helvetica", 10, "bold"))
            self.canvas.create_text(x, MARGIN + BOARD + 13, text=chr(ord("A") + col), font=("Helvetica", 10, "bold"))
        for row in range(N):
            y = MARGIN + row * CELL + CELL / 2
            self.canvas.create_text(13, y, text=str(8 - row), font=("Helvetica", 10, "bold"))
            self.canvas.create_text(MARGIN + BOARD + 13, y, text=str(8 - row), font=("Helvetica", 10, "bold"))

        event = self.current_event()
        current = None
        conflict_cells = set()
        if event and event["kind"] in ("try", "place", "conflict", "backtrack"):
            current = (event["row"], event["col"])
        if event and event["kind"] == "conflict":
            conflict_cells.add((event["row"], event["col"]))
            conflict_cells.add((event["conflict_row"], event["col"]))

        # Optional attack highlighting: mark squares sharing a row/column with any rook.
        attacked = set()
        if self.show_attacks.get():
            for r, c in enumerate(self.positions):
                if c >= 0:
                    for cc in range(N):
                        if cc != c:
                            attacked.add((r, cc))
                    for rr in range(N):
                        if rr != r:
                            attacked.add((rr, c))

        for row in range(N):
            for col in range(N):
                x1 = MARGIN + col * CELL
                y1 = MARGIN + row * CELL
                x2, y2 = x1 + CELL, y1 + CELL
                fill = LIGHT if (row + col) % 2 == 0 else DARK
                if (row, col) in attacked:
                    fill = "#f1b8a9"
                if current == (row, col):
                    fill = CURRENT
                if (row, col) in conflict_cells:
                    fill = CONFLICT
                if event and event["kind"] == "solution" and self.positions[row] == col:
                    fill = SUCCESS

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill, outline="#ffffff", width=1
                )
                if self.positions[row] == col:
                    # Draw a simple rook glyph using Unicode chess symbol.
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="♜", font=("DejaVu Sans", 38), fill=ROOK_COLOR
                    )
                if current == (row, col) and event and event["kind"] == "try":
                    self.canvas.create_text(
                        (x1 + x2) / 2, y2 - 9, text="?", font=("Helvetica", 12, "bold")
                    )

        # Board border.
        self.canvas.create_rectangle(
            MARGIN, MARGIN, MARGIN + BOARD, MARGIN + BOARD,
            outline="#333333", width=2
        )

    def toggle_play(self):
        if self.solving:
            self.pause()
        else:
            if self.step_index >= len(self.steps) - 1:
                self.step_index = -1
                self.apply_event()
            self.solving = True
            self.play_btn.configure(text="⏸ Pause")
            self.auto_tick()

    def auto_tick(self):
        if not self.solving:
            return
        if self.step_index + 1 >= len(self.steps):
            self.pause()
            return
        self.step_index += 1
        self.apply_event()
        self.after_id = self.root.after(self.speed.get(), self.auto_tick)

    def pause(self):
        self.solving = False
        self.play_btn.configure(text="▶ Auto-solve")
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None

    def update_speed(self, value):
        self.speed.set(int(float(value)))

    def reset(self):
        self.pause()
        self.step_index = -1
        self.positions = [-1] * N
        self.status_var.set("Reset complete. Press Next step or Auto-solve.")
        self.progress_var.set(f"Step: 0 / {len(self.steps)}")
        self.rook_var.set("Rooks placed: 0 / 8")
        self.draw_board()

    def on_board_click(self, event):
        # Manual placement is a small teaching aid; solver playback remains separate.
        self.pause()
        col = int((event.x - MARGIN) // CELL)
        row = int((event.y - MARGIN) // CELL)
        if not (0 <= row < N and 0 <= col < N):
            return

        conflict = None
        for r, c in enumerate(self.positions):
            if c >= 0 and r != row and c == col:
                conflict = f"Column {col + 1} already contains a rook in row {r + 1}."
                break
        if conflict:
            self.status_var.set("Manual placement rejected: " + conflict)
            self.draw_board()
            x1, y1 = MARGIN + col * CELL, MARGIN + row * CELL
            self.canvas.create_rectangle(
                x1 + 3, y1 + 3, x1 + CELL - 3, y1 + CELL - 3,
                outline=CONFLICT, width=5
            )
            return

        # Keep one rook per row: clicking a different square moves that row's rook.
        self.positions[row] = col
        self.status_var.set(
            f"Manual placement: rook at row {row + 1}, column {col + 1}. "
            "Click another square in that row to move it."
        )
        count = sum(c >= 0 for c in self.positions)
        self.rook_var.set(f"Rooks placed: {count} / 8")
        self.progress_var.set("Manual placement mode")
        self.draw_board()


def main():
    root = tk.Tk()
    app = EightRooksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
