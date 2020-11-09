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


board_moved_to_4D = """
-o-o-o-o
o-o-o-o-
-o-o-o-o
 - - - -
- -x- - 
x- -x-x-
-x-x-x-x
x-x-x-x-
"""
board_moved_to_5A = """
-o-o-o-o
o-o-o-o-
- -o-o-o
o- - - -
- - - - 
x-x-x-x-
-x-x-x-x
x-x-x-x-
"""
board_after_multiple_moves = """
-o-o-o-o
o- -o-o-
-o-o-o-o
o- - - -
- -x- - 
x-x-x-x-
-x- -x-x
x-x-x-x-
"""
testdata = [
    (init_state, [Move(start=(3, "C"), end=(4, "D"))], board_moved_to_4D),
    (init_state, [Move(start=(6, "B"), end=(5, "A"))], board_moved_to_5A),
    (
        init_state,
        [
            Move(start=(3, "C"), end=(4, "D")),
            Move(start=(6, "B"), end=(5, "A")),
            Move(start=(7, "C"), end=(6, "B")),
            Move(start=(2, "D"), end=(3, "C")),
        ],
        board_after_multiple_moves,
    ),
]


@pytest.mark.parametrize("initial_board,moves,expected_board", testdata)
def test_man_can_move_diagonal(initial_board, moves, expected_board):
    initial_board = CheckersBoard.from_ascii(initial_board)
    expected_board = CheckersBoard.from_ascii(expected_board)
    for move in moves:
        initial_board.move(move)
    assert str(initial_board) == str(expected_board)


jumpdata = [
    (
        """
-o- 
 -o-
-x- 
x- -
""",
        Move(start=(2, "B"), end=(4, "D")),
        """
-o-x
 - -
- - 
x- -
""",
        4,
    ),
    (
        """
-o- -
o- - 
-o-o-
x- - 
- - -
""",
        Move(start=(2, "A"), end=(2, "E")),
        """
-o- -
o- - 
- - -
 - -x
- - -
""",
        5,
    ),
    (
        """
- - - -
 -o- - 
- - - -
 -o- - 
- - - -
 -o-o- 
-x- - -
""",
        Move(start=(1, "B"), end=(7, "D")),
        """
- -x- -
 - - - 
- - - -
 - - - 
- - - -
 - -o- 
- - - -
""",
        7,
    ),
    (
        """
- - - -
 - - - 
- - - -
 -o- - 
- - - -
 -o-o- 
-x- - -
""",
        Move(start=(1, "B"), end=(1, "F")),
        """
- - - -
 - - - 
- - - -
 -o- - 
- - - -
 - - - 
- - -x-
""",
        7,
    ),
    (
        """
- - - -
 - - - 
- - - -
 -o- - 
- - - -
 -o-o- 
-x- - -
""",
        Move(start=(1, "B"), end=(5, "B")),
        """
- - - -
 - - - 
-x- - -
 - - - 
- - - -
 - -o- 
- - - -
""",
        7,
    ),
]


@pytest.mark.parametrize("board_before_jump,move,board_after_jump,dim", jumpdata)
def test_man_can_jump_over_opponents(board_before_jump, move, board_after_jump, dim):
    board_before_jump = CheckersBoard.from_ascii(board_before_jump, dim=dim)
    board_after_jump = CheckersBoard.from_ascii(board_after_jump, dim=dim)
    board_before_jump.move(move)
    assert str(board_before_jump) == str(board_after_jump)
