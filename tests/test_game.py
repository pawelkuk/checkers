import time
import pytest
from checkers.game import Game
from checkers.player import Player
from checkers.board import Move
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
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    g = Game(player_1, player_2, playing_time=1e-16)
    time.sleep(2e-16 * SECS)
    winner = g.move(Move(start=(3, "A"), end=(4, "B")))
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
