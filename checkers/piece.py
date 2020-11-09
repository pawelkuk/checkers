from functools import partial
from typing import Iterable, Tuple


class Field:
    char = "?"

    def __str__(self):
        return self.char

    def __eq__(self, other):
        return self.char == other.char


class InaccessibleField(Field):
    char = "-"


class AccessibleField(Field):
    char = " "


class Color:
    char = "?"

    def __str__(self):
        return self.char


class White(Color):
    char = "x"


class Black(Color):
    char = "o"


class Piece:
    def __init__(self, color: Color):
        self.color = color

    def __str__(self):
        return str(self.color)


class Man(Piece):
    def get_diagonal_moves(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        if isinstance(self.color, White):
            return [(x - 1, y - 1), (x - 1, y + 1)]
        elif isinstance(self.color, Black):
            return [(x + 1, y - 1), (x + 1, y + 1)]


class FlyingKing(Piece):
    def __str__(self):
        return str(self.color).capitalize()


char_to_piece = {
    "o": partial(Man, color=Black()),
    "x": partial(Man, color=White()),
    "O": partial(FlyingKing, color=Black()),
    "X": partial(FlyingKing, color=Black()),
    " ": partial(AccessibleField),
    "-": partial(InaccessibleField),
}
