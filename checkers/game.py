from .board import CheckersBoard
from .player import Player


class Game:
    def __init__(self, white: Player, black: Player, board=None):
        self._player_1 = white
        self._player_2 = black
        self._board = board or CheckersBoard()
        self._turn = white
