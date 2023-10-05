from ast_parser.errors import LinterException
from ast_parser.token import (
    Token,
    TokenKind,
    is_binary_operator,
    is_relational_operator,
)


def lint(token: Token, source: str) -> None:
    """Lint the obtained tokens step by step.

    Since the tokens must form a chain, hence the Lexer must fully
    tokenize the source before linting.

    Args:
        token (Token): The starting token.
        source (str): The source string being tokenized. Used for
            exception messages.

    Raises:
        LinterException: Unexpected binary operator, term missed.
        LinterException: Equation must contain only one relational
            operator.
        LinterException: Term must contain no more than one variable.
        LinterException: Unexpected comma at the beginning of the
            equation.
        LinterException: Unexpected comma, equation missed.
        LinterException: Unexpected comma at the end of the equation.
        LinterException: Equation must contain a relational operator.

    Returns:
        None: Nothing.
    """
    cursor: Token | None = token

    # Linting states.
    variable_provided = False
    relation_provided = False

    while cursor is not None:
        if is_binary_operator(cursor):
            if token.prev_token and is_binary_operator(token.prev_token):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected binary operator, term missed",
                )

            variable_provided = False

        if is_relational_operator(cursor):
            # <nothing> <relational operator> <nothing> ???

            if relation_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Equation must contain only one relational operator",
                )

            relation_provided = True

        # <term> <binary operator> <relational operator> ???

        if cursor.kind == TokenKind.VARIABLE:
            if variable_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Term must contain no more than one variable",
                )

            variable_provided = True

        if cursor.kind == TokenKind.COMMA:
            if token.prev_token is None:
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected comma at the beginning of the equation",
                )
            if token.prev_token.kind == TokenKind.COMMA:
                raise LinterException(
                    source, cursor.location, "Unexpected comma, equation missed"
                )

            if not relation_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Equation must contain a relational operator",
                )

            relation_provided = False

        cursor = cursor.next_token

    if not relation_provided:
        raise LinterException(
            source,
            token.location,
            "Equation must contain a relational operator",
        )
    # comma at the end of the equation ???


__all__ = ("lint",)
