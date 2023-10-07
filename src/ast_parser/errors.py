from ast_parser.token import Location


class PositionedException(Exception):
    """Base class for exceptions with Location.

    Args:
        source (str): The source string being tokenized.
        location (Location): The Location of the exception.
        description (str, optional): An optional description of the
            error.
    """

    source: str
    """The source string being tokenized."""
    location: Location
    """The Location of the error in the source."""

    def __init__(
        self, source: str, location: Location, description: str | None = None
    ) -> None:
        super().__init__(description)

        self.source = source
        self.location = location


class LexerException(PositionedException):
    """A LexerException is raised when the Lexer encounters an invalid
    character or token.

    Args:
        source (str): The source string being tokenized.
        location (Location): The Location of the exception.
        description (str, optional): An optional description of the
            error.
    """


class LinterException(PositionedException):
    """A LinterException is raised when the Linter encounters an invalid
    token chain.

    Args:
        source (str): The source string being tokenized.
        location (Location): The Location of the exception.
        description (str, optional): An optional description of the
            error.
    """


class ParserException(PositionedException):
    """A ParserException is raised when the Parser encounters an
    unexpected token or token chain.

    Args:
        source (str): The source string being tokenized.
        location (Location): The Location of the exception.
        description (str, optional): An optional description of the
            error.
    """


__all__ = (
    "PositionedException",
    "LexerException",
    "LinterException",
    "ParserException",
)
