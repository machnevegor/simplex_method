"""This module contains the Token class and its related classes."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TokenKind(str, Enum):
    """Kind of the Token."""

    SOF = "<SOF>"
    """Start of file."""
    EOF = "<EOF>"
    """End of file."""

    ADD = "+"
    """Addition operator."""
    SUB = "-"
    """Subtraction operator."""
    MUL = "*"
    """Multiplication operator."""

    EQ = "="
    """Equality operator."""
    LEQ = "<="
    """Less than or equal to operator."""
    GEQ = ">="
    """Greater than or equal to operator."""

    COEFFICIENT = "Coefficient"
    """Coefficient of a variable."""
    VARIABLE = "Variable"
    """Variable name."""


@dataclass
class Location:
    """Location of the Token in the source.

    The Location is more user-friendly than the start and end indices.
    """

    line: int
    """Line number of the token in the source. Starts at 1."""
    column: int
    """Column number of the token in the source. Starts at 1."""


@dataclass
class Token:
    """Token of the source code."""

    kind: TokenKind
    """Kind of the token."""

    start: int
    """The index of the first character of the token."""
    end: int
    """The index of the first character after the token."""
    location: Location
    """The Location of the token in the sourc."""

    value: str
    """The value of the token."""

    prev_token: Token | None = field(repr=False, default=None)
    """The previous Token in the source."""
    next_token: Token | None = field(repr=False, default=None)
    """The next Token in the source."""


__all__ = ("TokenKind", "Location", "Token")
