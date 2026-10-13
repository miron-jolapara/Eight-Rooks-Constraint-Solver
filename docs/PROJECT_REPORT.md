# Eight Rooks Constraint Solver — Project Report

## 1. Abstract

The Eight Rooks Constraint Solver is a desktop application that demonstrates how a Constraint Satisfaction Problem (CSP) can be represented and solved using search. The objective is to place eight rooks on an 8×8 chessboard so that no two rooks attack each other. Since a rook attacks along its row and column, a valid board must contain at most one rook in every row and every column. The application uses Python and Tkinter to display the board and explain search decisions through an interactive visual interface.

## 2. Problem Statement

Design a program that places eight non-attacking rooks on an 8×8 chessboard. The program must enforce the row and column constraints and provide a graphical explanation of the search process, including candidate checks and conflict highlighting.

## 3. Objectives

- Model the Eight Rooks puzzle as a CSP.
- Implement a row-by-row search strategy.
- Reject column assignments that violate constraints.
- Display rook placements on a graphical chessboard.
- Provide step controls and animated execution.
- Help users understand how constraints reduce the search space.

## 4. Constraint Satisfaction Problem Formulation

A CSP consists of variables, domains, and constraints.

### Variables

Let `Ri` represent the column selected for the rook in row `i`, where `i` ranges from 1 to 8.

### Domains

Each variable has the domain:

`Di = {1, 2, 3, 4, 5, 6, 7, 8}`

### Constraints

For every pair of distinct rows `i` and `j`:

`Ri != Rj`

Because the model assigns exactly one rook to each row, the row constraint is guaranteed by construction. The inequality constraint ensures that two rooks never occupy the same column.

### Goal test

A solution is found when every row has an assigned column and all eight selected columns are distinct.

## 5. Algorithm

1. Start with all row assignments set to `-1` (empty).
2. Select the next row.
3. Iterate through its possible columns.
4. Search previously assigned rows for a rook in the candidate column.
5. If the column is occupied, record a conflict and try another candidate.
6. Otherwise, place the rook and recursively solve the next row.
7. Stop when all eight rows are assigned.

The implementation records search events so the GUI can display them one at a time or animate them.

## 6. GUI Design

The application window contains:

- **Chessboard:** an 8×8 grid with row and column labels.
- **Next step / Previous:** moves forward and backward through the stored trace.
- **Auto-solve / Pause:** animates the trace.
- **Animation speed:** controls the delay between events.
- **Attack highlighting:** shades squares sharing a row or column with placed rooks.
- **Status panel:** explains the current candidate, conflict, or placement.
- **Reset:** returns the board to the initial state.
- **Manual placement:** allows a user to click a square to place or move a rook in a row, while rejecting occupied columns.

## 7. Technology Stack

- **Language:** Python
- **GUI library:** Tkinter
- **Algorithmic technique:** depth-first search / recursive backtracking pattern
- **Data representation:** one-dimensional list indexed by row
- **External dependencies:** none

## 8. Correctness

The program only accepts a candidate column if no earlier row uses that column. Each accepted assignment therefore preserves the invariant that all placed rooks occupy different columns. Since each recursive level corresponds to a different row, no two rooks can share a row. When all eight rows are assigned, both constraints hold, so the result is a valid Eight Rooks arrangement.

## 9. Complexity Analysis

For `N` rows and columns, there are up to `N!` complete arrangements with unique columns. A simple recursive search may examine permutations until it finds a solution. The implementation's column check scans earlier rows, taking up to `O(N)` per candidate. The recursion and placement array require `O(N)` auxiliary space, while the graphical event trace adds storage proportional to the number of recorded search events. For `N = 8`, there are `8! = 40,320` possible complete permutations.

## 10. Testing

Recommended checks:

1. The GUI starts without errors.
2. The board contains 64 squares.
3. The final solution contains eight rooks.
4. Every row contains exactly one rook.
5. Every column contains exactly one rook.
6. A candidate in an occupied column is rejected and highlighted.
7. Next and Previous update the displayed event.
8. Auto-solve can be paused and resumed.
9. Reset clears all placements and returns to the start.
10. Manual placement rejects a rook in an already occupied column.

A small automated test script is provided in `tests/test_constraints.py`.

## 11. Limitations and Future Improvements

The current implementation solves the fixed 8×8 problem and uses a simple row-by-row strategy. Because it rejects occupied columns before committing a placement, the first-solution search can reach a solution without needing to undo a valid placement. The interface includes a backtrack event type, but the standard search trace may not show an actual rollback. Possible extensions include supporting arbitrary board sizes, adding a step counter for constraint checks, exporting a search log, implementing alternative variable/value ordering, and adding a mode that intentionally demonstrates rollback.

## 12. Conclusion

The project combines a classic CSP with a graphical teaching tool. It makes the relationship between variables, domains, constraints, candidate rejection, and search visible. The interface can be used for demonstrations, practical assignments, and introductory study of constraint-based search.

## 13. References

- Python documentation: https://docs.python.org/3/
- Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- Constraint satisfaction problems: https://en.wikipedia.org/wiki/Constraint_satisfaction_problem
