import pytest

from checkers.board import CheckersBoard, Move
from checkers.piece import Man, AccessibleField, InaccessibleField

init_state = """
-o-o-o-o
o-o-o-o-
-o-o-o-o
 - - - -
- - - - 
x-x-x-x-
-x-x-x-x
x-x-x-x-
"""


def test_board_parses_ascii_representation():
    board = CheckersBoard.from_ascii(init_state)
    assert str(board) == init_state


def test_can_get_board_element():
    board = CheckersBoard.from_ascii(init_state)
    assert type(board[8, "B"]) == Man
    assert type(board[8, "A"]) == InaccessibleField
    assert type(board[5, "A"]) == AccessibleField


testdata = [("", "", "")]


@pytest.mark.parametrize("initial_board,move,expected_board", testdata)
def test_man_can_move_diagonal(initial_board, move, expected_board):
    expected_end_state = """
-o-o-o-o
o-o-o-o-
-o-o-o-o
 - - - -
- -x- - 
x- -x-x-
-x-x-x-x
x-x-x-x-
"""
    init_board = CheckersBoard.from_ascii(init_state)
    expected_board = CheckersBoard.from_ascii(expected_end_state)
    move = Move(start=(3, "C"), end=(4, "D"))
    init_board.move(move)
    assert str(init_board) == str(expected_board)
