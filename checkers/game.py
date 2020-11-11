from time import time
from .board import CheckersBoard, Move
from .player import Player

SECS = 60


class Game:
    def __init__(
        self, white: Player, black: Player, playing_time: float = 10, board=None
    ):
        self._board = board or CheckersBoard.from_ascii()
        self._turn: Player = white
        self._wait: Player = black
        self._moves = []
        self._turn.remaining_time = playing_time * SECS
        self._wait.remaining_time = playing_time * SECS
        self._timestamp = time()

    def move(self, move: Move):
        ...