from .piece import char_to_piece, Piece, AccessibleField, Man, FlyingKing
from typing import Tuple, Iterable, List


class Move:
    def __init__(self, start: Tuple[int, str], end: Tuple[int, str]):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class Board:
    def _cord2idx(self, row: int, col: str) -> Tuple[int, int]:
        x = self.dim - row
        y = ord(col) - ord("A")
        return x, y

    def _ind2cord(self, move: Move) -> Tuple[int, str]:
        x, y = move
        row = self.dim - x
        col = chr(y + ord("A"))
        return row, col

    @classmethod
    def from_ascii(cls, board: str, dim: int = 8):
        rows = board.strip().split("\n")
        board = []
        for i, row in enumerate(rows):
            board_row = []
            for j, c in enumerate(row):
                field = char_to_piece[c]()
                board_row.append(field)
            if len(board_row) != dim:
                raise ValueError
            board.append(board_row)
        if len(board) != dim:
            raise ValueError
        return cls(board, dim=dim)

    def __init__(self, board: List[List], dim=8):
        self._board = board
        self.dim = dim

    def __getitem__(self, key):
        row, col = key
        if len(col) != 1 or not (0 < row <= self.dim):
            raise ValueError
        x, y = self._cord2idx(row, col)
        return self._board[x][y]

    def __setitem__(self, key, val):
        row, col = key
        if len(col) != 1 or not (0 < row <= self.dim):
            raise ValueError
        x, y = self._cord2idx(row, col)
        self._board[x][y] = val

    def __str__(self):
        rows = ["".join(str(c) for c in row) for row in self._board]
        board = "\n".join(rows)
        return "\n" + board + "\n"


class CheckersBoard(Board):
    def move(self, move: Move):
        if not isinstance(self[move.start], Piece):
            raise TypeError("One can move only pieces")
        if not isinstance(self[move.end], AccessibleField):
            raise TypeError("The field is not accessable")
        if self._is_valid(move):
            self[move.end] = self[move.start]
            self[move.start] = AccessibleField()

    def _is_valid(self, move: Move):
        return move in self._possible_moves(start=move.start)

    def _possible_moves(self, start: Tuple[int, str]) -> Iterable[Move]:
        piece = self[start]
        x, y = self._cord2idx(*start)
        if type(piece) == Man:
            possible_moves = self._explore_man_rules(x, y)
        elif type(piece) == FlyingKing:
            possible_moves = self._explore_flying_king_rules(x, y)
        else:
            raise TypeError
        possible_moves = [
            Move(start=start, end=self._ind2cord(end)) for end in possible_moves
        ]
        return possible_moves

    def _explore_man_rules(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        if self._can_capture(x, y):
            return self._get_moves_with_max_capture(x, y)
        else:
            return self._get_diagonal_moves(x, y)

    def _explore_flying_king_rules(self, x, y):
        raise NotImplementedError

    def _can_capture(self, x, y):
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in dirs:
            opponent_x, opponent_y = x + dx, y + dy
            after_jump_x, after_jump_y = x + 2 * dx, y + 2 * dy
            if not (0 <= after_jump_x < self.dim and 0 <= after_jump_y < self.dim):
                continue
            if not isinstance(self._board[opponent_x][opponent_y], Piece):
                continue
            if self._board[opponent_x][opponent_y].color == self._board[x][y].color:
                continue
            if self._board[after_jump_x][after_jump_y] == AccessibleField():
                return True
        return False

    def _get_diagonal_moves(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        piece: Man = self._board[x][y]
        potential_moves = piece.get_diagonal_moves(x, y)
        potential_moves = [
            (x, y)
            for x, y in potential_moves
            if 0 <= x < self.dim and 0 <= y < self.dim
        ]
        potential_moves = [
            (x, y) for x, y in potential_moves if self._board[x][y] == AccessibleField()
        ]
        return potential_moves

    def _get_moves_with_max_capture(x: int, y: int) -> Iterable[Move]:
        raise NotImplementedError
