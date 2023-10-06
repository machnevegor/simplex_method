from dataclasses import dataclass
from enum import Enum

from ast_parser.token import TokenKind


@dataclass
class Constraint:
    """Constraint of the LP problem."""

    kind: TokenKind.EQ | TokenKind.LEQ | TokenKind.GEQ
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


__all__ = ("Constraint", "ProblemKind", "Problem")
