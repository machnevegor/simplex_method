from .chars import is_coefficient_start, is_digit, is_variable_start, print_code
from .token import Location, Token, TokenKind


class LexerException(Exception):
    source: str
    location: Location

    def __init__(
        self, source: str, location: Location, description: str | None = None
    ) -> None:
        super().__init__(description)

        self.source = source
        self.location = location


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
        if not is_digit(first_code):  # not <digit>
            raise LexerException(
                self.source,
                Location(self._line, 1 + start - self._line_start),
                f"Unexpected character, expected digit but got: {print_code(first_code)}",
            )

        position = start + 1

        while position < len(self.source) and is_digit(
            self._read_code(position)
        ):  # <digit>
            position += 1

        return position

    def _read_coefficient(self, start: int, first_code: int) -> Token:
        position, code = start, first_code

        # Leftmost digits:
        if code == 0x0030:  # `0`
            position += 1
            code = self._read_code(position)

            if is_digit(code):  # <digit>
                raise LexerException(
                    self.source,
                    Location(self._line, 1 + position - self._line_start),
                    f"Invalid coefficient, unexpected digit after 0: {print_code(code)}",
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

        if code == 0x002E or is_variable_start(code):  # `.` | <alpha> | `_`
            raise LexerException(
                self.source,
                Location(self._line, 1 + position - self._line_start),
                f"Invalid coefficient, expected digit but got: {print_code(code)}",
            )

        return self._create_token(
            TokenKind.COEFFICIENT, start, position, self.source[start:position]
        )


__all__ = ("LexerException", "Lexer")
