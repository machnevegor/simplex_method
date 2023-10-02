from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TokenKind(str, Enum):
    EOF = "<EOF>"
    SOF = "<SOF>"

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

    PAREN_L = "("
    PAREN_R = ")"

    EQ = "="
    LEQ = "<="
    GEQ = ">="

    COEFFICIENT = "Coefficient"
    VARIABLE = "Variable"


@dataclass
class Location:
    line: int
    column: int


@dataclass
class Token:
    kind: TokenKind

    start: int
    end: int
    location: Location

    value: str

    prev_token: Token | None = field(repr=False, default=None)
    next_token: Token | None = field(repr=False, default=None)


__all__ = ("TokenKind", "Location", "Token")
