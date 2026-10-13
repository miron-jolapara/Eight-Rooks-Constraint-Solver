# Algorithm Notes

## State representation

`positions[row] = column` means a rook is assigned to that row and column. `-1` indicates an unassigned row.

## Pseudocode

```text
SEARCH(row):
    if row == 8:
        report solution
        return success

    for col from 0 to 7:
        record candidate attempt

        if any earlier row has a rook in col:
            record conflict
            continue

        positions[row] = col
        record placement

        if SEARCH(row + 1) succeeds:
            return success

        positions[row] = -1
        record backtrack

    return failure
```

## Invariant

At the start of each recursive call for row `r`, all assigned rows before `r` have exactly one rook, and their selected columns are distinct.

## Why the conflict check is enough

Each recursion level assigns one new row, so row collisions cannot occur. A rook attacks another rook only if they share a row or column. Therefore, checking that the new column is not already used is sufficient.

## Backtracking note

With this exact constraint model, every partial assignment using distinct columns can be extended until all rows are assigned. Therefore, a first-solution search with immediate conflict rejection will typically never enter the rollback branch. Conflicting candidate attempts are still visible. To teach rollback explicitly, one can use a deliberately poor candidate ordering, add extra constraints, or generalize the task to N-Queens.
