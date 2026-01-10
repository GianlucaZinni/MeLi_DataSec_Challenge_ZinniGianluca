# Tests for solution_minesweeper.py using Python 3.12.10
import unittest

from solution_minesweeper import count_neighbouring_mines


class TestCountNeighbouringMines(unittest.TestCase):
    def test_challenge_board(self):
        challenge_board = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 1, 0, 0],
        ]
        challenge_expected = [
            [1, 9, 2, 1],
            [2, 3, 9, 2],
            [3, 9, 4, 9],
            [9, 9, 3, 1],
        ]
        self.assertEqual(count_neighbouring_mines(challenge_board), challenge_expected)

    def test_single_mine(self):
        self.assertEqual(count_neighbouring_mines([[1]]), [[9]])

    def test_empty_board(self):
        self.assertEqual(count_neighbouring_mines([]), [])

    def test_irregular_board(self):
        irregular_board = [
            [1, 0],
            [0, 0, 1],
            [0],
        ]
        irregular_expected = [
            [9, 2],
            [1, 2, 9],
            [0],
        ]
        self.assertEqual(count_neighbouring_mines(irregular_board), irregular_expected)


if __name__ == "__main__":
    unittest.main()
