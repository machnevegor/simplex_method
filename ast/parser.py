from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .chars import (
    is_coefficient_start,
    is_digit,
    is_printable,
    is_variable_start,
    print_char_code,
)
from .token import Location, Token, TokenKind


class ParseError(Exception):
    source: str
    location: Location

    def __init__(
        self, source: str, location: Location, description: str | None = None
    ) -> None:
        super().__init__(description)

        self.source = source
        self.location = location

    def __repr__(self) -> str:
        res = f"ParseError(source={self.source!r}, location={self.location!r}"

        if self.args:
            res += f", description={self.args[0]!r}"

        return res + ")"


class Lexer:
    source: str

    _token: Token

    _line: int
    _line_start: int

    def __init__(self, source: str) -> None:
        self.source = source

        self._token = Token(TokenKind.SOF, 0, 0, Location(0, 0), "")

        self._line = 1
        self._line_start = 0

    def __repr__(self) -> str:
        return f"Lexer(source={self.source!r})"

    def _create_token(self, kind: TokenKind, start: int, end: int, value: str) -> Token:
        return Token(
            kind,
            start,
            end,
            self._line,
            1 + start - self._line_start,
            value,
            self._token,
        )

    def _read_code(self, position: int) -> int | None:
        return ord(self.source[position]) if position < len(self.source) else None

    def _read_digits(self, start: int, first_code: int | None) -> int:
        if not is_digit(first_code):  # not <DIGIT>
            raise ParseError(
                self.source,
                Location(self._line, 1 + start - self._line_start),
                f"Unexpected character, expected digit but got: {print_char_code(first_code)}",
            )

        position = start + 1

        while position < len(self.source) and is_digit(
            self._read_code(position)
        ):  # <DIGIT>
            position += 1

        return position

    def _read_coefficient(self, start: int, first_code: int) -> Token:
        position, code = start, first_code

        # Leftmost digits:
        if code == 0x0030:  # `0`
            position += 1
            code = self._read_code(position)

            if is_digit(code):  # <DIGIT>
                raise ParseError(
                    self.source,
                    Location(self._line, 1 + position - self._line_start),
                    f"Invalid coefficient, unexpected digit after 0: {print_char_code(code)}",
                )
        elif code != 0x002E:  # not `.`
            position = self._read_digits(position, code)
            code = self._read_code(position)

        # Rightmost digits:
        if code == 0x002E:  # `.`
            position += 1
            code = self._read_code(position)

            position += self._read_digits(position, code)
            code = self._read_code(position)

        # Exponent:
        if code in (0x0045, 0x0065):  # `E` | `e`
            position += 1
            code = self._read_code(position)

            if code in (0x002B, 0x002D):  # `+` | `-`
                position += 1
                code = self._read_code(position)

            position = self._read_digits(position, code)
            code = self._read_code(position)

        if code == 0x002E or is_variable_start(code):  # `.` | <LETTER> | `_`
            raise ParseError(
                self.source,
                Location(self._line, 1 + position - self._line_start),
                f"Invalid coefficient, expected digit but got: {print_char_code(code)}",
            )

        return self._create_token(
            TokenKind.COEFFICIENT, start, position, self.source[start:position]
        )

    def _next_token(self) -> Token:
        position = self._token.end

        while position < len(self.source):
            char = self.source[position]
            code = ord(char)

            match code:
                # Ignored:
                # - UnicodeBOM
                # - WhiteSpace
                # - LineTerminator
                case 0xFEFF | 0x0009 | 0x0020:  # <BOM> | `\t` | <space>
                    position += 1

                    continue
                case 0x000A:  # `\n`
                    position += 1

                    self._line += 1
                    self._line_start = position

                    continue
                case 0x000D:  # `\r`
                    position += 2 if ord(self.source[position + 1]) == 0x000A else 1

                    self._line += 1
                    self._line_start = position

                    continue
                # Single-char tokens:
                # - ADD
                # - MUL
                # - SUB
                # - DIV
                # - PAREN_L
                # - PAREN_R
                # - EQUALS
                case 0x002B | 0x002D | 0x002A | 0x0028 | 0x002F | 0x0029 | 0x003D:  # `+` | `-` | `*` | `(` | `)` | `=`
                    return self._create_token(
                        TokenKind(char), position, position + 1, char
                    )

            # Multi-char tokens:
            # - COEFFICIENT
            # - VARIABLE
            if is_coefficient_start(code):  # <DIGIT> | `.`
                return self._read_coefficient(position, code)
            if is_variable_start(code):  # <LETTER> | `_`
                return ...

            raise ParseError(
                self.source,
                Location(self._line, 1 + position - self._line_start),
                f"Invalid character: {print_char_code(code)}",
            )

        return self._create_token(TokenKind.EOF, position, position, "")


class Parser:
    _lexer: Lexer

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)
