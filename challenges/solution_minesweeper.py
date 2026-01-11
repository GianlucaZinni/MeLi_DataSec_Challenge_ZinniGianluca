# Python 3.12.10
"""
Counts neighbouring mines on a Minesweeper board.

Implementation notes:
    - Uses fixed neighbour offsets across eight directions and iterates every cell once
    to build a new matrix; time complexity O(r*c*8) with r rows and c columns.
    - Treats any cell equal to 1 as a mine and marks it with 9 in the output, otherwise
    counts adjacent mines.
    - Handles empty boards or empty rows by returning an empty list. Supports non-rectangular
    (irregular) boards by checking each row length before indexing.
"""
from typing import List


def count_neighbouring_mines(board: list) -> list:
    """
    Counts neighbouring mines for each cell in a Minesweeper board.

    Parameters:
        board (list): A 2D list where 0 represents empty and 1 represents a mine.

    Returns:
        list: A 2D list where each cell contains the count of neighbouring mines, or 9 if the cell contains a mine.
    """
    if not board or not isinstance(board, list):
        return []

    # Eight offsets (row, column) for all adjacent cells.
    # Using a tuple keeps the offsets constant and avoids per-cell reassignment.
    # Each pair represents a directional move relative to the current cell.
    neighbour_offsets = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    result: List[List[int]] = []
    for row_index, row in enumerate(board):

        if not isinstance(row, list):
            return []
        result_row: List[int] = []
        for col_index in range(len(row)):

            cell = row[col_index]

            if cell == 1:
                result_row.append(9)
                continue

            mine_count = 0
            for delta_row, delta_col in neighbour_offsets:

                neighbour_row_index = row_index + delta_row
                neighbour_col_index = col_index + delta_col
                if 0 <= neighbour_row_index < len(board):
                    neighbour_row = board[neighbour_row_index]
                    if isinstance(
                        neighbour_row, list
                    ) and 0 <= neighbour_col_index < len(neighbour_row):
                        if neighbour_row[neighbour_col_index] == 1:
                            mine_count += 1
            result_row.append(mine_count)
        result.append(result_row)

    return result
