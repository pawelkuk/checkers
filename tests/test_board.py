import pytest

from checkers.board import CheckersBoard, Move
from checkers.piece import Man, AccessibleField, InaccessibleField, Color, Black, White

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
-o-X
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
- -X- -
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
    (
        """
- - 
 - -
-X- 
o- -
""",
        Move(start=(1, "A"), end=(3, "C")),
        """
- - 
 -o-
- - 
 - -
""",
        4,
    ),
]


@pytest.mark.parametrize("board_before_jump,move,board_after_jump,dim", jumpdata)
def test_man_can_jump_over_opponents(board_before_jump, move, board_after_jump, dim):
    board_before_jump = CheckersBoard.from_ascii(board_before_jump, dim=dim)
    board_after_jump = CheckersBoard.from_ascii(board_after_jump, dim=dim)
    board_before_jump.move(move)
    assert str(board_before_jump) == str(board_after_jump)


man_flying_king_cases = [
    (
        """
- - 
x- -
- - 
 - -
""",
        Move(start=(3, "A"), end=(4, "B")),
        """
-X- 
 - -
- - 
 - -
""",
        4,
    ),
    (
        """
- - 
o-x-
-x- 
 - -
""",
        Move(start=(3, "A"), end=(1, "C")),
        """
- - 
 -x-
- - 
 -O-
""",
        4,
    ),
    (
        """
o- - 
- - -
o- - 
-x-x-
 - -x
""",
        Move(start=(3, "A"), end=(3, "E")),
        """
o- - 
- - -
 - -o
- - -
 - -x
""",
        5,
    ),
]


@pytest.mark.parametrize("given,move,then,dim", man_flying_king_cases)
def test_man_can_convert_to_flying_king_after_reaching_end_of_board(
    given, move: Move, then, dim
):
    given = CheckersBoard.from_ascii(given, dim=dim)
    then = CheckersBoard.from_ascii(then, dim=dim)
    given.move(move)
    assert str(given) == str(then)


flying_king_moves_all_over_the_board = [
    (
        """
- - 
 - -
- - 
X- -
""",
        Move(start=(1, "A"), end=(4, "D")),
        """
- -X
 - -
- - 
 - -
""",
        4,
    ),
    (
        """
- - 
 - -
- - 
X- -
""",
        Move(start=(1, "A"), end=(3, "C")),
        """
- - 
 -X-
- - 
 - -
""",
        4,
    ),
    (
        """
- -o
 -o-
- - 
X- -
""",
        Move(start=(1, "A"), end=(2, "B")),
        """
- -o
 -o-
-X- 
 - -
""",
        4,
    ),
    (
        """
- - 
 - -
- -X
 - -
""",
        Move(start=(2, "D"), end=(4, "B")),
        """
-X- 
 - -
- - 
 - -
""",
        4,
    ),
]


@pytest.mark.parametrize("given,move,then,dim", flying_king_moves_all_over_the_board)
def test_flying_king_can_move_all_over_the_board(given, move: Move, then, dim):
    given = CheckersBoard.from_ascii(given, dim=dim)
    then = CheckersBoard.from_ascii(then, dim=dim)
    given.move(move)
    assert str(given) == str(then)


flying_king_captures_opponents = [
    (
        """
- - 
 - -
-o- 
X- -
""",
        Move(start=(1, "A"), end=(4, "D")),
        """
- -X
 - -
- - 
 - -
""",
        4,
    ),
    (
        """
- - 
 - -
-o- 
X- -
""",
        Move(start=(1, "A"), end=(3, "C")),
        """
- - 
 -X-
- - 
 - -
""",
        4,
    ),
    (
        """
- - - - 
 - - - -
- - - - 
 - - - -
- -o- - 
 - - - -
-o- - - 
X- - - -
""",
        Move(start=(1, "A"), end=(8, "H")),
        """
- - - -X
 - - - -
- - - - 
 - - - -
- - - - 
 - - - -
- - - - 
 - - - -
""",
        8,
    ),
    (
        """
- - - - 
 - - - -
-o-o- - 
x- - - -
-o-o- - 
 - - - -
-o- - - 
X- - - -
""",
        Move(start=(5, "A"), end=(5, "A")),
        """
- - - - 
 - - - -
- - - - 
x- - - -
- - - - 
 - - - -
-o- - - 
X- - - -
""",
        8,
    ),
    (
        """
- - - - 
 - - - -
-o-o- - 
X- - - -
-o-o- - 
 - - - -
-o- - - 
X- - - -
""",
        Move(start=(5, "A"), end=(5, "A")),
        """
- - - - 
 - - - -
- - - - 
X- - - -
- - - - 
 - - - -
-o- - - 
X- - - -
""",
        8,
    ),
]


@pytest.mark.parametrize("given,move,then,dim", flying_king_captures_opponents)
def test_flying_king_jumps_over_opponents_according_to_rules(
    given, move: Move, then, dim
):
    given = CheckersBoard.from_ascii(given, dim=dim)
    then = CheckersBoard.from_ascii(then, dim=dim)
    given.move(move)
    assert str(given) == str(then)


invalid_moves = [
    (
        """
- - - - 
 - - - -
- -o- - 
 - - - -
- -o-o- 
 - - - -
-x- -o- 
X- - - -
""",
        Move(start=(1, "A"), end=(1, "E")),
        8,
    ),
    (
        """
- - - - 
 - - - -
- -o- - 
 - - - -
- -o-o- 
 - - - -
-o- -x- 
X- - - -
""",
        Move(start=(1, "A"), end=(1, "E")),
        8,
    ),
    (
        """
- - 
 - -
-x- 
 - -
""",
        Move(start=(2, "B"), end=(1, "C")),
        4,
    ),
    (
        """
- - 
 - -
-o- 
 - -
""",
        Move(start=(2, "B"), end=(3, "C")),
        4,
    ),
    (
        """
- - 
 -o-
- - 
x- -
""",
        Move(start=(1, "A"), end=(4, "D")),
        4,
    ),
]


@pytest.mark.parametrize("given,move,dim", invalid_moves)
def test_board_raises_error_when_given_invalid_move(given, move: Move, dim):
    given = CheckersBoard.from_ascii(given, dim=dim)
    with pytest.raises(ValueError):
        given.move(move)


any_left_data = [
    (
        """
- - 
 -o-
-o- 
 - -
""",
        4,
        Black(),
        True,
    ),
    (
        """
- - 
 -o-
-o- 
 - -
""",
        4,
        White(),
        False,
    ),
    (
        """
- - 
 - -
- -x
 -x-
""",
        4,
        White(),
        True,
    ),
    (
        """
- - 
 - -
- -x
 -x-
""",
        4,
        Black(),
        False,
    ),
]


@pytest.mark.parametrize("board,dim,color,expected_result", any_left_data)
def test_if_any_pieces_of_given_color_left(board, dim, color, expected_result):
    board = CheckersBoard.from_ascii(board, dim=4)
    assert board.any_pieces_left(color) is expected_result
