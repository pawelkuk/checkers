import pytest
from checkers.game import Game
from checkers.player import Player
from checkers.board import Move

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
