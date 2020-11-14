from time import time
from typing import Optional
from .board import CheckersBoard, Move
from .player import Player, Winner
from .piece import Black, White

SECS = 60


class Game:
    def __init__(
        self, white: Player, black: Player, playing_time: float = 10, board=None
    ):
        self._board = board or CheckersBoard.from_ascii()
        white.color = White()
        black.color = Black()
        self._turn: Player = white
        self._wait: Player = black
        self._moves = []
        self._turn.remaining_time = playing_time * SECS
        self._wait.remaining_time = playing_time * SECS
        self._timestamp = time()
        self._winner: Optional[Winner] = None
        self._game_over: False

    def move(self, move: Move) -> Optional[Winner]:
        if self._winner:
            return Winner(self._winner)
        if self._time_is_over():
            self._winner = self._wait
            return Winner(self._winner)
        if not self._is_correct_turn(move):
            raise ValueError("The other player must do the move.")

        try:
            self._board.move(move)
        except Exception as e:
            raise e
        self._moves.append(move)

        if self._player_has_won():
            self._winner = self._turn
            return Winner(self._winner)

        self._update_time()
        self._turn, self._wait = self._wait, self._turn

    def _time_is_over(self) -> bool:
        time_elapsed_since_last_move = time() - self._timestamp
        new_remaining_time = self._turn.remaining_time - time_elapsed_since_last_move
        return new_remaining_time <= 0

    def _is_correct_turn(self, move: Move) -> bool:
        return self._board[move.start].color == self._turn.color

    def _update_time(self):
        time_elapsed_since_last_move = time() - self._timestamp
        self._turn.remaining_time -= time_elapsed_since_last_move
        self._timestamp = time()

    def _player_has_won(self):
        opponent_color = self._wait.color
        if self._board.any_pieces_left(opponent_color):
            return False
        else:
            return True

    def back(self):
        raise NotImplementedError
