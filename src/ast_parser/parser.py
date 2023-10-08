from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ast_parser.lexer import Lexer
from ast_parser.linter import Linter
from ast_parser.token import Token, TokenKind


class EquationKind(str, Enum):
    """Kind of relationship between the left and right parts of the
    Equation."""

    EQ = "="
    """Equality operator."""
    LEQ = "<="
    """Less than or equal to operator."""
    GEQ = ">="
    """Greater than or equal to operator."""


@dataclass
class Equation:
    """Equation definition."""

    kind: EquationKind
    """Kind of relationship between the left and right parts of the
    Equation.
    """
    variables: dict[str, float]
    """Equation variables. The names are the keys, the coefficients are
    the values.
    """
    bound: float
    """Bound of the Equation. Must be non-negative."""


@dataclass
class EquationAccumulator:
    """The EquationAccumulator collects equation Tokens: variables,
    coefficients, and bounds.
    """

    kind: EquationKind | None = field(default=None)
    """Kind of relationship between the left and right parts of the
    Equation.
    """
    variables: dict[str, float] = field(default_factory=dict)
    """Equation variables. The names are the keys, the coefficients are
    the values.
    """
    bound: float = field(default=0.0)
    """Bound of the Equation. Must be non-negative."""

    coefficient: float | None = field(default=None)
    """Coefficient of the current variable."""
    variable: str | None = field(default=None)
    """Name of the current variable."""


class Parser:
    """Source Parser. It parses the source and returns a list of
    Equation objects found in the source.

    Args:
        source (str): The source to parse.
    """

    _lexer: Lexer
    """Lexer of the source."""
    _linter: Linter
    """Linter of the source."""

    _accumulator: EquationAccumulator
    """Equation accumulator."""

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)
        self._linter = Linter(source)

        self._accumulator = EquationAccumulator()

    def __iter__(self) -> Parser:
        """Gets an iterator over the Equations in the source.

        Returns:
            Parser: _description_
        """
        return self

    def __next__(self) -> Equation:
        """Gets the next Equation in the source.

        Accumulation, processing and validation of Equations in
        real-time. The source is parsed sequentially, token by token.

        Raises:
            StopIteration: The end of the source has been reached.
            LexerException: Unexpected character, less than operator is
                not allowed.
            LexerException: Unexpected character, greater than operator
                is not allowed.
            LexerException: Invalid character: <code>.
            LexerException: Invalid coefficient, unexpected digit after
                0: <code>.
            LexerException: Invalid coefficient, expected digit but
                got: <code>.
            LinterException: Unexpected binary operator, term missed.
            LinterException: Equation must contain only one relational
                operator.
            LinterException: Term must contain no more than one
                variable.
            LinterException: Unexpected comma at the beginning of the
                equation.
            LinterException: Unexpected comma, equation missed.
            LinterException: Unexpected comma at the end of the
                equation.
            LinterException: Equation must contain a relational
                operator.

        Returns:
            Equation: The next Equation from the source.
        """
        while True:
            token = next(self._lexer)

            self._linter.lint(token)

            match token.kind:
                case TokenKind.SOF | TokenKind.MUL:
                    continue
                case TokenKind.EOF:
                    if token.prev_token.kind == TokenKind.SOF:
                        raise StopIteration

                    return self._derive_equation()
                case TokenKind.ADD:
                    self._parse_addition_operator()

                    continue
                case TokenKind.SUB:
                    self._parse_subtraction_operator()

                    continue
                case TokenKind.EQ | TokenKind.LEQ | TokenKind.GEQ:
                    self._parse_relational_operator(token)

                    continue
                case TokenKind.COEFFICIENT:
                    self._parse_coefficient(token)

                    continue
                case TokenKind.VARIABLE:
                    self._parse_variable(token)

                    continue
                case TokenKind.COMMA:
                    return self._derive_equation()

    def _extend_variables(self) -> None:
        """Extend the variables with the current variable and
        coefficient.
        """
        if self._accumulator.coefficient:
            if self._accumulator.kind:
                self._accumulator.coefficient *= -1.0
            if self._accumulator.variable:
                if self._accumulator.variable in self._accumulator.variables:
                    self._accumulator.variables[
                        self._accumulator.variable
                    ] += self._accumulator.coefficient
                else:
                    self._accumulator.variables[
                        self._accumulator.variable
                    ] = self._accumulator.coefficient
            else:
                self._accumulator.bound -= self._accumulator.coefficient

    def _derive_equation(self) -> Equation:
        """Derive the Equation from the EquationAccumulator.

        Returns:
            Equation: The derived Equation.
        """
        self._extend_variables()

        equation = Equation(
            self._accumulator.kind, self._accumulator.variables, self._accumulator.bound
        )

        self._accumulator = EquationAccumulator()

        return equation

    def _parse_addition_operator(self) -> None:
        """Parse the addition operator Token."""
        self._extend_variables()

        self._accumulator.variable = None
        self._accumulator.coefficient = 1.0

    def _parse_subtraction_operator(self) -> None:
        """Parse the subtraction operator Token."""
        self._extend_variables()

        self._accumulator.variable = None
        self._accumulator.coefficient = -1.0

    def _parse_relational_operator(self, token: Token) -> None:
        """Parse the relational operator Token.

        Args:
            token (Token): The relational operator Token.
        """
        self._extend_variables()

        self._accumulator.kind = EquationKind(token.kind.value)
        self._accumulator.variable = None
        self._accumulator.coefficient = None

    def _parse_coefficient(self, token: Token) -> None:
        """Parse the coefficient Token.

        Args:
            token (Token): The coefficient Token.
        """
        if not self._accumulator.coefficient:
            self._accumulator.coefficient = 1.0

        self._accumulator.coefficient *= float(token.value)

    def _parse_variable(self, token: Token) -> None:
        """Parse the variable Token.

        Args:
            token (Token): The variable Token.
        """
        if not self._accumulator.coefficient:
            self._accumulator.coefficient = 1.0

        self._accumulator.variable = token.value


__all__ = ("EquationKind", "Equation", "Parser")
