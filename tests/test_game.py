from checkers.game import Game
from checkers.player import Player


def test_can_create_game_with_init_state():
    player_1 = Player("Alice")
    player_2 = Player("Bob")
    Game(player_1, player_2)
