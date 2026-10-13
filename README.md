# Eight Rooks Constraint Solver (CSP + Backtracking)

An interactive Python/Tkinter educational application that visualizes the **Eight Rooks problem** on an 8×8 board. It demonstrates constraint checking, candidate rejection, search progress, and a backtracking-style search trace.

## Features

- 8×8 chessboard with rook symbols and row/column labels
- Step-by-step search trace (`Next step` and `Previous`)
- Automatic animated playback with adjustable speed
- Highlights the current candidate and detected column conflicts
- Optional highlighting of squares attacked by placed rooks
- Manual rook placement for experimentation
- Reset and progress/status indicators
- No third-party Python packages required (Tkinter is included with many Python distributions)

## Requirements

- Python 3.9 or later recommended
- Tkinter support in the Python installation
- macOS, Windows, or Linux desktop environment

> Tkinter is part of Python's standard library, but some Linux distributions package it separately. On Debian/Ubuntu, install it with `sudo apt install python3-tk` if needed.

## Run

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Eight-Rooks-CSP.git
cd Eight-Rooks-CSP
python3 eight_rooks_solver.py
```

On Windows, try:

```powershell
py eight_rooks_solver.py
```

## How the CSP is modeled

Each row is a variable:

- **Variables:** `R1, R2, ..., R8`
- **Domain:** each variable can choose a column from `{1, 2, ..., 8}`
- **Constraints:** `Ri != Rj` for all different rows `i != j`
- **Goal:** assign one column to every row without repeating any column

The implementation stores the selected column for each row in an array. A value of `-1` means that row has no rook.

## How the search works

1. Select the next row.
2. Try a column.
3. Check whether an earlier rook already occupies that column.
4. Reject conflicting candidates; otherwise place the rook and continue to the next row.
5. Finish when all eight rows have valid placements.

### Important algorithm note

For this particular problem, checking the column constraint before placing each rook means the first valid branch reaches a solution without needing to undo a previously valid placement. The trace still shows rejected candidate choices and includes a backtracking event handler, but an actual rollback event may not occur in the standard first-solution search. This is a property of the simple Eight Rooks CSP, not a failure of the constraint check. If a course rubric requires visibly demonstrated rollback, use a deliberately non-chronological candidate strategy or a generalized N-Rooks/N-Queens example with additional constraints.

## Complexity

With row-by-row search and a linear scan of earlier rows to check a column, the worst-case search is bounded by exploring permutations of columns. There are `8! = 40,320` possible complete column arrangements. The first-solution implementation generally stops much earlier. Space usage is `O(N)` for the placement array and recursion depth, excluding the GUI's precomputed event trace.

## Repository structure

```text
Eight-Rooks-CSP/
├── eight_rooks_solver.py
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── ALGORITHM.md
│   └── flowchart.mmd
└── tests/
    └── test_constraints.py
```

## Screenshots for your repository

Run the app, capture screenshots of:
1. The initial empty board
2. A candidate conflict highlighted
3. A completed solution

Save them under `docs/screenshots/` and embed them here if desired. Do not commit screenshots unless they are your own captures.

## Suggested GitHub description

> Interactive Eight Rooks Constraint Satisfaction Problem solver in Python Tkinter, demonstrating row/column constraints, step-by-step search, conflict highlighting, and search visualization.

## License

MIT. See [`LICENSE`](LICENSE).
