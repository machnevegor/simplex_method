from ast_parser.errors import LinterException
from ast_parser.token import (
    Token,
    TokenKind,
    is_binary_operator,
    is_relational_operator,
)


def is_chain_intact(token: Token) -> bool:
    """Check if the token chain is safe in the specific region.

    Args:
        token (Token): The token to check.

    Returns:
        bool: True if the token chain is safe, False otherwise.
    """
    if token.kind != TokenKind.SOF and (
        token.prev_token is None or token.prev_token.next_token is not token
    ):
        return False
    if token.kind != TokenKind.EOF and (
        token.next_token is None or token.next_token.prev_token is not token
    ):
        return False

    return True


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
    """
    cursor: Token | None = token

    # Linting states.
    variable_provided = False
    relation_provided = False

    while cursor is not None:
        if not is_chain_intact(cursor):
            raise LinterException(
                source,
                cursor.location,
                "Crude modification of the token chain is detected",
            )

        if cursor.kind == TokenKind.EOF:
            if cursor.prev_token.kind != TokenKind.SOF and not relation_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Equation must contain a relational operator",
                )
            if is_binary_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.prev_token.location,
                    "Unexpected binary operator at the end of the equation",
                )
            if is_relational_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected EOF, right side of the equation is missed",
                )
            if cursor.prev_token.kind == TokenKind.COMMA:
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected comma at the end of the equation",
                )

        if is_binary_operator(cursor):
            if is_binary_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected binary operator, term missed",
                )

            variable_provided = False

        if cursor.kind == TokenKind.MUL and cursor.prev_token.kind == TokenKind.MUL:
            raise LinterException(
                source,
                cursor.location,
                "Unexpected multiplication operator, term missed",
            )

        if is_relational_operator(cursor):
            if relation_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Equation must contain only one relational operator",
                )
            if is_binary_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected binary operator, term missed",
                )
            if cursor.prev_token.kind in (TokenKind.SOF, TokenKind.COMMA):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected relational operator, left side of the equation is missed",
                )

            variable_provided = False
            relation_provided = True

        if cursor.kind == TokenKind.VARIABLE:
            if variable_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Term must contain no more than one variable",
                )

            variable_provided = True

        if cursor.kind == TokenKind.COMMA:
            if cursor.prev_token.kind == TokenKind.SOF:
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected comma at the beginning of the equation",
                )
            if not relation_provided:
                raise LinterException(
                    source,
                    cursor.location,
                    "Equation must contain a relational operator",
                )
            if is_binary_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.prev_token,
                    "Unexpected binary operator at the end of the equation",
                )
            if is_relational_operator(cursor.prev_token):
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected comma, right side of the equation is missed",
                )
            if cursor.prev_token.kind == TokenKind.COMMA:
                raise LinterException(
                    source,
                    cursor.location,
                    "Unexpected comma, equation missed",
                )

        cursor = cursor.next_token


__all__ = ("lint",)
