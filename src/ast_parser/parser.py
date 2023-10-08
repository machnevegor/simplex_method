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

    _equations: list[Equation]
    """List of Equation objects found in the source."""
    _accumulator: EquationAccumulator
    """Equation accumulator."""

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)
        self._linter = Linter(source)

        self._equations = []
        self._accumulator = EquationAccumulator()

    def parse(self) -> list[Equation]:
        """Parse the source. Return a list of Equation objects.

        Returns:
            list[Equation]: A list of Equation objects.
        """
        while True:
            token = next(self._lexer)

            self._linter.lint(token)

            match token.kind:
                case TokenKind.SOF | TokenKind.MUL:
                    continue
                case TokenKind.EOF:
                    self._parse_eof()

                    return self._equations
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
                    self._parse_comma()

                    continue

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

    def _extend_equations(self) -> None:
        """Extend the equations with the current Equation."""
        self._extend_variables()

        self._equations.append(
            Equation(
                self._accumulator.kind,
                self._accumulator.variables,
                self._accumulator.bound,
            )
        )

    def _parse_eof(self) -> None:
        """Parse the EOF Token."""
        self._extend_equations()

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
        """Parse the relational operator Token."""
        self._extend_variables()

        self._accumulator.kind = EquationKind(token.kind.value)
        self._accumulator.variable = None
        self._accumulator.coefficient = None

    def _parse_coefficient(self, token: Token) -> None:
        """Parse the coefficient Token."""
        if not self._accumulator.coefficient:
            self._accumulator.coefficient = 1.0

        self._accumulator.coefficient *= float(token.value)

    def _parse_variable(self, token: Token) -> None:
        """Parse the variable Token."""
        if not self._accumulator.coefficient:
            self._accumulator.coefficient = 1.0

        self._accumulator.variable = token.value

    def _parse_comma(self) -> None:
        """Parse the comma Token."""
        self._extend_equations()

        self._accumulator = EquationAccumulator()


__all__ = ("EquationKind", "Equation", "Parser")
