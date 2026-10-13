"""Lightweight correctness tests for the Eight Rooks CSP.

Run from the repository root:
    python3 -m unittest discover -s tests -v
"""

import unittest


def is_valid_solution(positions):
    """Return True if each of 8 rows has a column and all columns are unique."""
    if len(positions) != 8:
        return False
    if any(not isinstance(c, int) or c < 0 or c >= 8 for c in positions):
        return False
    return len(set(positions)) == 8


def solve_eight_rooks():
    """Independent reference solver used by the tests."""
    result = [-1] * 8

    def search(row, used_columns):
        if row == 8:
            return True
        for col in range(8):
            if col in used_columns:
                continue
            result[row] = col
            if search(row + 1, used_columns | {col}):
                return True
            result[row] = -1
        return False

    search(0, set())
    return result


class TestEightRooksConstraints(unittest.TestCase):
    def test_reference_solver_returns_eight_rooks(self):
        solution = solve_eight_rooks()
        self.assertEqual(len(solution), 8)
        self.assertTrue(is_valid_solution(solution))

    def test_permutation_is_valid(self):
        self.assertTrue(is_valid_solution([0, 1, 2, 3, 4, 5, 6, 7]))

    def test_duplicate_column_is_invalid(self):
        self.assertFalse(is_valid_solution([0, 1, 2, 3, 4, 5, 6, 6]))

    def test_unassigned_row_is_invalid(self):
        self.assertFalse(is_valid_solution([0, 1, 2, 3, 4, 5, 6, -1]))

    def test_out_of_range_column_is_invalid(self):
        self.assertFalse(is_valid_solution([0, 1, 2, 3, 4, 5, 6, 8]))

    def test_wrong_board_size_is_invalid(self):
        self.assertFalse(is_valid_solution([0, 1, 2]))


if __name__ == "__main__":
    unittest.main()
