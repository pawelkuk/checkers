from .piece import (
    char_to_piece,
    Piece,
    AccessibleField,
    Man,
    FlyingKing,
    Color,
    White,
    color_to_char,
)
from typing import Tuple, Iterable, List, Optional, Dict

init_board = """
-o-o-o-o
o-o-o-o-
-o-o-o-o
 - - - -
- - - - 
x-x-x-x-
-x-x-x-x
x-x-x-x-
"""


class Move:
    def __init__(
        self,
        start: Tuple[int, str],
        end: Tuple[int, str],
        captured: Optional[List[Tuple]] = None,
    ):
        self.start = start
        self.end = end
        self.captured = captured or []

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class Capture:
    def __init__(self, opponent_position, end_position):
        self.opponent_position = opponent_position
        self.end_position = end_position


class Board:
    def _cord2idx(self, row: int, col: str) -> Tuple[int, int]:
        x = self.dim - row
        y = ord(col) - ord("A")
        return x, y

    def _ind2cord(self, move: Tuple[int, int]) -> Tuple[int, str]:
        x, y = move
        row = self.dim - x
        col = chr(y + ord("A"))
        return row, col

    @classmethod
    def from_ascii(cls, ascii_board: Optional[str] = None, dim: int = 8):
        ascii_board = ascii_board or init_board
        rows = ascii_board.strip().split("\n")
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

    def __iter__(self):
        only_pieces = []
        for row in self._board:
            for field_or_piece in row:
                if isinstance(field_or_piece, Piece):
                    only_pieces.append(field_or_piece)
        return iter(only_pieces)

    def any_pieces_left(self, color: Color) -> bool:
        return any(piece.color == color for piece in self)


class CheckersBoard(Board):
    def move(self, move: Move):
        moving_piece = self[move.start]
        if not isinstance(moving_piece, Piece):
            raise TypeError("One can move only pieces")
        forced_move = self._move_with_highest_precedence(moving_piece)
        self[move.start] = AccessibleField()
        if self[move.end] != AccessibleField():
            raise TypeError("The field is not accessable")
        possible_moves = self._possible_moves(move.start, moving_piece)
        if move not in possible_moves:
            self[move.start] = moving_piece
            raise ValueError("Invalid move")
        for m in possible_moves:
            if m != move:
                continue
            if forced_move and len(m.captured) < len(forced_move.captured):
                self[move.start] = moving_piece
                raise ValueError("Other move has higher precedence")
            self[m.end] = moving_piece
            for captured in m.captured:
                x, y = captured
                self._board[x][y] = AccessibleField()
            self._try_convert_to_flying_king(m.end)

    def _move_with_highest_precedence(self, moving_piece) -> Optional[Move]:
        all_moves = []
        for x, row in enumerate(self._board):
            for y, piece in enumerate(row):
                if piece is moving_piece:
                    continue
                if not isinstance(piece, Piece):
                    continue
                if piece.color != moving_piece.color:
                    continue
                moves = self._possible_moves(self._ind2cord((x, y)), piece)
                moves = [m for m in moves if m.captured is not None]
                all_moves.extend(moves)
        return (
            max(all_moves, key=lambda move: len(move.captured)) if all_moves else None
        )

    def _try_convert_to_flying_king(self, end_position: Tuple[int, str]):
        if not isinstance(self[end_position], Man):
            return
        end_of_board = self.dim if self[end_position].color == White() else 1
        if end_position[0] == end_of_board:
            self[end_position] = FlyingKing(color=self[end_position].color)

    def _possible_moves(self, start: Tuple[int, str], piece) -> Iterable[Move]:
        x, y = self._cord2idx(*start)
        if type(piece) == Man:
            possible_moves = self._explore_man_rules(x, y, piece)
        elif type(piece) == FlyingKing:
            possible_moves = self._explore_flying_king_rules(x, y, piece)
        else:
            raise TypeError

        return possible_moves

    def _explore_man_rules(self, x: int, y: int, piece) -> Iterable:
        start = self._ind2cord((x, y))

        if self._can_capture_from(x, y, color=piece.color):
            move_with_captured_pieces = self._get_moves_with_max_capture(
                x, y, color=piece.color, mode="man"
            )
            possible_moves = [
                Move(start=start, end=self._ind2cord(end), captured=captured)
                for captured, end in move_with_captured_pieces
            ]
        else:
            moves = self._get_diagonal_moves(x, y, piece)
            possible_moves = [
                Move(start=start, end=self._ind2cord(end)) for end in moves
            ]
        return possible_moves

    def _explore_flying_king_rules(self, x, y, piece) -> Iterable:
        start = self._ind2cord((x, y))
        if self._can_capture_as_flying_king_from(x, y, color=piece.color):
            move_with_captured_pieces = self._get_moves_with_max_capture(
                x, y, color=piece.color, mode="flying_king"
            )
            possible_moves = [
                Move(start=start, end=self._ind2cord(end), captured=captured)
                for captured, end in move_with_captured_pieces
            ]
        else:
            possible_moves = self._get_diagonal_moves(x, y, piece)
            possible_moves = [
                Move(start=start, end=self._ind2cord(end)) for end in possible_moves
            ]
        return possible_moves

    def _can_capture_as_flying_king_from(
        self, x: int, y: int, color: Optional[Color] = None
    ) -> Iterable[Capture]:
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        capture_end_position_pairs = []
        for dx, dy in dirs:
            for i in range(1, self.dim):
                new_x, new_y = x + i * dx, y + i * dy
                if not (0 <= new_x < self.dim and 0 <= new_y < self.dim):
                    break
                if not isinstance(self._board[new_x][new_y], Piece):
                    continue
                if self._board[new_x][new_y].color == color:
                    break
                for j in range(i + 1, self.dim):
                    end_x, end_y = x + j * dx, y + j * dy
                    if not (0 <= end_x < self.dim and 0 <= end_y < self.dim):
                        break
                    if isinstance(self._board[end_x][end_y], Piece):
                        break
                    if self._board[end_x][end_y] == AccessibleField():
                        capture_end_position_pairs.append(
                            Capture(
                                opponent_position=(new_x, new_y),
                                end_position=(end_x, end_y),
                            )
                        )
                break
        return capture_end_position_pairs

    def _can_capture_from(
        self, x: int, y: int, color: Optional[Color] = None
    ) -> Iterable[Capture]:
        color = color or self._board[x][y].color
        can_capture = []
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in dirs:
            opponent_x, opponent_y = x + dx, y + dy
            after_jump_x, after_jump_y = x + 2 * dx, y + 2 * dy
            if not (0 <= after_jump_x < self.dim and 0 <= after_jump_y < self.dim):
                continue
            if not isinstance(self._board[opponent_x][opponent_y], Piece):
                continue
            if self._board[opponent_x][opponent_y].color == color:
                continue
            if self._board[after_jump_x][after_jump_y] == AccessibleField():
                can_capture.append(
                    Capture(
                        opponent_position=(opponent_x, opponent_y),
                        end_position=(after_jump_x, after_jump_y),
                    )
                )
        return can_capture

    def _get_diagonal_moves(self, x: int, y: int, piece) -> Iterable[Tuple[int, int]]:
        potential_moves = piece.get_diagonal_moves(x, y, self.dim)
        potential_moves = [
            (x, y)
            for x, y in potential_moves
            if 0 <= x < self.dim and 0 <= y < self.dim
        ]
        potential_moves = [
            (x, y) for x, y in potential_moves if self._board[x][y] == AccessibleField()
        ]
        return potential_moves

    def _get_moves_with_max_capture(
        self, x: int, y: int, color: Color, captured=None, mode: str = "man",
    ) -> List[Tuple[List[Tuple[int, int]], Tuple[int, int]]]:
        captured = captured or []
        possible_captures = (
            self._can_capture_from(x, y, color=color)
            if mode == "man"
            else self._can_capture_as_flying_king_from(x, y, color=color)
        )
        possible_captures = [
            capture
            for capture in possible_captures
            if capture.opponent_position not in captured
        ]

        if not possible_captures:
            return [(captured, (x, y))]

        new_captures = []
        for capture in possible_captures:
            new_capture = capture.opponent_position
            new_x, new_y = capture.end_position
            max_captured = self._get_moves_with_max_capture(
                new_x, new_y, captured=captured + [new_capture], color=color, mode=mode
            )
            new_captures.extend(max_captured)
        max_capture = max([len(c[0]) for c in new_captures])
        equivalent_max_captures = [
            cap for cap in new_captures if len(cap[0]) == max_capture
        ]
        return equivalent_max_captures

    @staticmethod
    def _checkers_notation_to_coord(i: int) -> Tuple[int, int]:
        x = (i - 1) // 4
        y = 1 - (x % 2) + 2 * ((i - 1) % 4)
        return x, y

    def to_checkers_notation(self) -> Dict[int, Optional[str]]:
        checkers_notation = {}
        for i in range(1, 33):
            x, y = self._checkers_notation_to_coord(i)
            if isinstance(self._board[x][y], Piece):
                checkers_notation[i] = self._board[x][y].color.name
            else:
                checkers_notation[i] = None
        return checkers_notation

    @classmethod
    def from_checkers_notation(
        cls, checkers_notation: Dict[int, Optional[str]]
    ) -> "CheckersBoard":
        board = cls.from_ascii()

        for idx, piece in checkers_notation.items():
            x, y = cls._checkers_notation_to_coord(idx)
            board._board[x][y] = char_to_piece[color_to_char[piece]]()
        return board
