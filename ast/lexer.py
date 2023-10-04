"""This module contains the Lexer class, which is responsible for
converting a source string into a stream of tokens.
"""
from typing import Callable

from .chars import (
    is_coefficient_start,
    is_digit,
    is_variable_continue,
    is_variable_start,
    print_code,
)
from .token import Location, Token, TokenKind


class LexerException(Exception):
    """A LexerException is raised when the Lexer encounters an invalid
    character or token.

    Args:
        source (str): The source string being tokenized.
        location (Location): The location of the invalid character or token.
        description (str | None): An optional description of the error.
    """

    source: str
    """The source string being tokenized."""
    location: Location
    """The location of the invalid character or token."""

    def __init__(
        self, source: str, location: Location, description: str | None = None
    ) -> None:
        super().__init__(description)

        self.source = source
        self.location = location


class Lexer:
    """A Lexer is a stateful stream generator in that every time it is
    advanced, it returns the next token in the Source.

    Assuming the source lexes, the final Token emitted by the Lexer
    will be of kind EOF, after which the Lexer will repeatedly return
    the same EOF token whenever called.

    Args:
        source (str): The source string being tokenized.
    """

    source: str
    """The source string being tokenized."""

    _token: Token
    """The currently active token."""

    _line: int
    """The current line number."""
    _line_start: int
    """The index of the start of the current line."""

    def __init__(self, source: str) -> None:
        self.source = source

        self._token = Token(TokenKind.SOF, 0, 0, Location(0, 0), "")

        self._line = 1
        self._line_start = 0

    def _create_token(self, kind: TokenKind, start: int, end: int, value: str) -> Token:
        """Creates a token with the given parameters.

        A token is created relative to the current state of the Lexer.

        Args:
            kind (TokenKind): The kind of token.
            start (int): The index of the first character of the token.
            end (int): The index of the first character after the token.
            value (str): The value of the token.

        Returns:
            Token:
        """
        location = Location(self._line, 1 + start - self._line_start)

        return Token(kind, start, end, location, value, self._token)

    def _read_code(self, position: int) -> int | None:
        """Reads the character code at the given position in the source.

        Args:
            position (int): The index of the character to read.

        Returns:
            int | None: The character code at the given position, or
                None if the position is out of bounds.
        """
        return ord(self.source[position]) if position < len(self.source) else None

    def _read_while(self, start: int, predicate: Callable[[int], bool]) -> int:
        """Reads a sequence of characters from the source starting at
        the given position while the predicate is satisfied.

        Args:
            start (int): The index of the first character of the token.
            predicate (Callable[[int], bool]): A function that takes a
                character code and returns whether or not it satisfies
                the predicate.

        Returns:
            int: The index of the first character after the sequence.
        """
        position = start

        while position < len(self.source) and predicate(ord(self.source[position])):
            position += 1

        return position

    def _read_digits(self, start: int, first_code: int | None) -> int:
        """Reads a sequence of digits from the source starting at the
        given position.

        Args:
            start (int): The index of the first character of the token.
            first_code (int | None): The code of the first character of
                the token.

        Raises:
            LexerException: Unexpected character, expected digit but
                got: <code>.

        Returns:
            int: The index of the first character after the digits.
        """
        if not is_digit(first_code):  # not <digit>
            raise LexerException(
                self.source,
                Location(self._line, 1 + start - self._line_start),
                f"Unexpected character, expected digit but got: {print_code(first_code)}",
            )

        return self._read_while(start + 1, is_digit)

    def _read_coefficient(self, start: int, first_code: int) -> Token:
        """Reads a coefficient token from the source starting at the
        given position.

        Args:
            start (int): The index of the first character of the token.
            first_code (int): The code of the first character of the
                token.

        Raises:
            LexerException: Invalid coefficient, expected digit but
                got: <code>.

        Returns:
            Token: The coefficient token.
        """
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

        return self._create_token(
            TokenKind.COEFFICIENT, start, position, self.source[start:position]
        )

    def _read_variable(self, start: int) -> Token:
        """Reads a variable token from the source starting at the given
        position.

        Args:
            start (int): The index of the first character of the token.

        Returns:
            Token: The variable token.
        """
        position = self._read_while(start + 1, is_variable_continue)

        return self._create_token(
            TokenKind.VARIABLE, start, position, self.source[start:position]
        )

    def _next_token(self) -> Token:
        """Gets the next token from the source starting at the given
        position.

        This skips over whitespace until it finds the next lexable
        token, then lexes punctuators immediately or calls the
        appropriate helper function for more complicated tokens.

        Raises:
            LexerException: Unexpected character, less than operator is
                not allowed.
            LexerException: Unexpected character, greater than operator
                is not allowed.
            LexerException: Invalid character: <code>.
            LexerException: Invalid coefficient, unexpected digit after
                0: <code>.
            LexerException: Invalid coefficient, expected digit but
                got: <code>.

        Returns:
            Token: The next token from the source.
        """
        position = self._token.end

        while position < len(self.source):
            char = self.source[position]
            code = ord(char)

            match code:
                # Ignored:
                # - Unicode BOM
                # - White space
                # - Line terminator
                case 0xFEFF | 0x0009 | 0x0020:  # <BOM> | `\t` | <space>
                    position += 1

                    continue
                case 0x000A:  # `\n`
                    position += 1

                    self._line += 1
                    self._line_start = position

                    continue
                case 0x000D:  # `\r`
                    position += (
                        2 if self._read_code(position + 1) == 0x000A else 1
                    )  # `\r\n` | `\r`

                    self._line += 1
                    self._line_start = position

                    continue
                # Single-char tokens:
                # - Binary plus and minus operators
                # - Multiplication operator
                # - Relational operators
                case 0x002B | 0x002D | 0x002A:  # `+` | `-` | `*`
                    return self._create_token(
                        TokenKind(char), position, position + 1, char
                    )
                case 0x003D:  # `=`
                    if self._read_code(position + 1) == 0x003D:
                        return self._create_token(
                            TokenKind.EQ, position, position + 2, "=="
                        )

                    return self._create_token(
                        TokenKind.EQ, position, position + 1, char
                    )
                case 0x003C:  # `<`
                    if self._read_code(position + 1) == 0x003D:  # `=`
                        return self._create_token(
                            TokenKind.LEQ, position, position + 2, "<="
                        )

                    raise LexerException(
                        self.source,
                        Location(self._line, 1 + position - self._line_start),
                        "Unexpected character, less than operator is not allowed",
                    )
                case 0x003E:  # `>`
                    if self._read_code(position + 1) == 0x003D:  # `=`
                        return self._create_token(
                            TokenKind.GEQ, position, position + 2, ">="
                        )

                    raise LexerException(
                        self.source,
                        Location(self._line, 1 + position - self._line_start),
                        "Unexpected character, greater than operator is not allowed",
                    )
                case 0x2264:  # `≤`
                    return self._create_token(
                        TokenKind.LEQ, position, position + 1, char
                    )
                case 0x2265:  # `≥`
                    return self._create_token(
                        TokenKind.GEQ, position, position + 1, char
                    )

            # Multi-char tokens:
            # - Coefficient
            # - Variable
            if is_coefficient_start(code):  # <digit> | `.`
                return self._read_coefficient(position, code)
            if is_variable_start(code):  # <alpha> | `_`
                return self._read_variable(position)

            raise LexerException(
                self.source,
                Location(self._line, 1 + position - self._line_start),
                f"Invalid character: {print_code(code)}",
            )

        return self._create_token(TokenKind.EOF, position, position, "")


__all__ = ("LexerException", "Lexer")
