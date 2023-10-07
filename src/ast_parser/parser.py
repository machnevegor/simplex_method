from dataclasses import dataclass
from enum import Enum

from ast_parser.errors import ParserException
from ast_parser.lexer import Lexer
from ast_parser.linter import Linter
from ast_parser.token import Token, TokenKind


@dataclass
class Constraint:
    """Constraint of the LP problem."""

    #kind: TokenKind.EQ | TokenKind.LEQ | TokenKind.GEQ
    kind : TokenKind.EQ
    """Kind of the constraint."""
    variables: dict[str, float]
    """Basic variables of the constraint. Name -> coefficient."""
    solution: float
    """Solution of the constraint. Must be non-negative."""


class ProblemKind(str, Enum):
    """Kind of the LP problem."""

    MAX = "max"
    """Maximization problem."""
    MIN = "min"
    """Minimization problem."""


@dataclass
class Problem:
    """Description of the LP problem."""

    kind: ProblemKind
    """Kind of the problem."""
    function: dict[str, float]
    """Right side of the objective function. Name -> coefficient."""
    constraints: list[Constraint]
    """Constraints of the problem."""


class Parser:
    _lexer: Lexer
    _linter: Linter

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)
        self._linter = Linter(source)

    def _expect_token(self, kind: TokenKind) -> Token:
        """Expect a Token of the specific TokenKind.

        Args:
            kind (TokenKind): The expected TokenKind of the Token.

        Raises:
            ParserException: Expected <TokenKind>, found <TokenKind>.

        Returns:
            Token: The expected Token.
        """
        token = self._lexer.token

        if token.kind != kind:
            raise ParserException(
                self._lexer.source,
                token.location,
                f"Expected {kind.name}, found {token.kind.name}",
            )

        return token

    def _parse_coefficient(self) -> float:
        """Parse a coefficient token.

        Returns:
            float: The coefficient value.
        """
        token = self._expect_token(TokenKind.COEFFICIENT)

        return float(token.value)


__all__ = ("Constraint", "ProblemKind", "Problem")
