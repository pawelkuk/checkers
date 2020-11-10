from .piece import char_to_piece, Piece, AccessibleField, Man, FlyingKing, Color, White
from typing import Tuple, Iterable, List, Optional


class Move:
    def __init__(self, start: Tuple[int, str], end: Tuple[int, str]):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class SimpleMove(Move):
    ...


class JumpMove(Move):
    def __init__(
        self,
        start: Tuple[int, str],
        end: Tuple[int, str],
        captured: List[Tuple[int, int]],
    ):
        super().__init__(start=start, end=end)
        self.captured = captured


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
        possible_moves = self._possible_moves(move.start)
        if move not in possible_moves:
            raise ValueError("Invalid move")
        for m in possible_moves:
            if m != move:
                continue
            self[m.end] = self[m.start]
            self[m.start] = AccessibleField()
            if isinstance(m, JumpMove):
                for captured in m.captured:
                    x, y = captured
                    self._board[x][y] = AccessibleField()
            self._try_convert_to_flying_king(m.end)

    def _try_convert_to_flying_king(self, end_position: Tuple[int, str]):
        if not isinstance(self[end_position], Man):
            return
        end_of_board = self.dim if self[end_position].color == White() else 1
        if end_position[0] == end_of_board:
            self[end_position] = FlyingKing(color=self[end_position].color)

    def _possible_moves(self, start: Tuple[int, str]) -> Iterable[SimpleMove]:
        piece = self[start]
        x, y = self._cord2idx(*start)
        if type(piece) == Man:
            possible_moves = self._explore_man_rules(x, y)
        elif type(piece) == FlyingKing:
            possible_moves = self._explore_flying_king_rules(x, y)
        else:
            raise TypeError

        return possible_moves

    def _explore_man_rules(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        start = self._ind2cord((x, y))

        if self._can_capture_from(x, y):
            move_with_captured_pieces = self._get_moves_with_max_capture(
                x, y, color=self._board[x][y].color, mode="man"
            )
            possible_moves = [
                JumpMove(start=start, end=self._ind2cord(end), captured=captured)
                for captured, end in move_with_captured_pieces
            ]
        else:
            possible_moves = self._get_diagonal_moves(x, y)
            possible_moves = [
                SimpleMove(start=start, end=self._ind2cord(end))
                for end in possible_moves
            ]
        return possible_moves

    def _explore_flying_king_rules(self, x, y):
        start = self._ind2cord((x, y))
        if self._can_capture_as_flying_king_from(x, y):
            move_with_captured_pieces = self._get_moves_with_max_capture(
                x, y, color=self._board[x][y].color, mode="flying_king"
            )
            possible_moves = [
                JumpMove(start=start, end=self._ind2cord(end), captured=captured)
                for captured, end in move_with_captured_pieces
            ]
        else:
            possible_moves = self._get_diagonal_moves(x, y)
            possible_moves = [
                SimpleMove(start=start, end=self._ind2cord(end))
                for end in possible_moves
            ]
        return possible_moves

    def _can_capture_as_flying_king_from(
        self, x: int, y: int, color: Optional[Color] = None
    ) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
        color = color or self._board[x][y].color
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
                            ((i * dx, i * dy), (end_x, end_y))
                        )
                break
        return capture_end_position_pairs

    def _can_capture_from(
        self, x: int, y: int, color: Optional[Color] = None
    ) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
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
                can_capture.append(((dx, dy), (x + 2 * dx, y + 2 * dy)))
        return can_capture

    def _get_diagonal_moves(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        piece: Man = self._board[x][y]
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
        self,
        x: int,
        y: int,
        color: Color,
        captured=None,
        mode: str = "man",
    ) -> List[Tuple[List[Tuple[int, int]], Tuple[int, int]]]:
        new_captures = []
        captured = captured or []
        possible_captures = (
            self._can_capture_from(x, y, color=color)
            if mode == "man"
            else self._can_capture_as_flying_king_from(x, y, color=color)
        )
        possible_captures = [
            ((dx, dy), pos)
            for (dx, dy), pos in possible_captures
            if (x + dx, y + dy) not in captured
        ]
        if not possible_captures:
            return [(captured, (x, y))]
        for (dx, dy), (new_x, new_y) in possible_captures:
            new_capture = x + dx, y + dy
            max_captured = self._get_moves_with_max_capture(
                new_x, new_y, captured=captured + [new_capture], color=color, mode=mode
            )
            new_captures.extend(max_captured)
        max_capture = max([len(c[0]) for c in new_captures])
        equivalent_max_captures = [
            cap for cap in new_captures if len(cap[0]) == max_capture
        ]
        return equivalent_max_captures
