import time
import pytest
from checkers.game import Game
from checkers.player import Player
from checkers.board import Move, CheckersBoard
from checkers.game import SECS


# 8|-o-o-o-o|
# 7|o-o-o-o-|
# 6|-o-o-o-o|
# 5| - - - -|
# 4|- - - - |
# 3|x-x-x-x-|
# 2|-x-x-x-x|
# 1|x-x-x-x-|
#   ABCDEFGH


def test_can_create_game_with_init_state():
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    Game(player_1, player_2)


def test_player_can_not_make_to_moves_in_a_row():
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    game = Game(player_1, player_2)
    game.move(Move(start=(3, "A"), end=(4, "B")))
    with pytest.raises(ValueError):
        game.move(Move(start=(4, "B"), end=(5, "C")))


def test_player_1_runs_out_of_time():
    # given:
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    g = Game(player_1, player_2, playing_time=1e-16)

    # when:
    time.sleep(2e-16 * SECS)
    winner = g.move(Move(start=(3, "A"), end=(4, "B")))

    # then:
    assert winner.player is player_2


def test_player_2_runs_out_of_time():
    # given:
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    time_in_secs = 1e-6
    g = Game(player_1, player_2, playing_time=time_in_secs)

    # when:
    g.move(Move(start=(3, "A"), end=(4, "B")))
    time.sleep(time_in_secs * SECS * 1.1)
    winner = g.move(Move(start=(6, "B"), end=(5, "A")))

    # then:
    assert winner.player is player_1


player_1_win_data = [
    (
        """
- - 
 -o-
- -x
 - -
""",
        4,
        Move(start=(2, "D"), end=(4, "B")),
    ),
    (
        """
- - -
 - - 
-o-o-
 - -x
- - -
""",
        5,
        Move(start=(2, "E"), end=(2, "A")),
    ),
]


@pytest.mark.parametrize("board,dim,move", player_1_win_data)
def test_player_1_wins_after_winning_move(board, dim, move):
    # given:
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    board = CheckersBoard.from_ascii(board, dim=dim)
    g = Game(player_1, player_2, board=board)

    # when:
    winner = g.move(move)

    # then:
    assert winner.player is player_1


player_2_win_data = [
    (
        """
-o- 
 - -
- -x
 - -
""",
        4,
        [
            Move(start=(2, "D"), end=(3, "C")),
            Move(start=(4, "B"), end=(2, "D")),
        ],
    ),
    (
        """
- - -
 - -o
-x- -
 - -x
- - -
""",
        5,
        [
            Move(start=(2, "E"), end=(3, "D")),
            Move(start=(4, "E"), end=(4, "A")),
        ],
    ),
]


@pytest.mark.parametrize("board,dim,moves", player_2_win_data)
def test_player_2_wins_after_winning_move(board, dim, moves):
    # given:
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    board = CheckersBoard.from_ascii(board, dim=dim)
    g = Game(player_1, player_2, board=board)

    # when:
    for move in moves:
        winner = g.move(move)

    # then:
    assert winner.player is player_2


back_moves_data = [
    (
        """
- -o-
 - - 
- - -
 - -x
-x- -
""",
        5,
        [
            Move(start=(2, "E"), end=(3, "D")),
            Move(start=(5, "D"), end=(4, "C")),
        ],
        """
- -o-
 - - 
- -x-
 - - 
-x- -
""",
    ),
    (
        """
- -o-
 - - 
- - -
 - -x
-x- -
""",
        5,
        [
            Move(start=(2, "E"), end=(3, "D")),
        ],
        """
- -o-
 - - 
- - -
 - -x
-x- -
""",
    ),
]


@pytest.mark.parametrize("board,dim,moves,expected", back_moves_data)
def test_player_can_undo_move(board, dim, moves, expected):
    # given
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    board = CheckersBoard.from_ascii(board, dim=dim)
    g = Game(player_1, player_2, board=board)

    # when:
    for move in moves:
        g.move(move)
    g.undo()

    # then:
    assert str(g) == expected


undo_after_game_end = [
    (
        """
- - -
 - -o
- - -
 - -x
- - -
""",
        5,
        [
            Move(start=(2, "E"), end=(3, "D")),
            Move(start=(4, "E"), end=(2, "C")),
        ],
        """
- - -
 - - 
- - -
 -o- 
- - -
""",
    ),
]


@pytest.mark.parametrize("board,dim,moves,expected", undo_after_game_end)
def test_player_can_not_undo_move_if_the_game_ended(board, dim, moves, expected):
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    board = CheckersBoard.from_ascii(board, dim=dim)
    g = Game(player_1, player_2, board=board)
    for move in moves:
        g.move(move)

    with pytest.raises(ValueError):
        g.undo()
