from ast_parser.errors import LinterException
from ast_parser.token import (
    Token,
    TokenKind,
    is_binary_operator,
    is_relational_operator,
)


class Linter:
    """Linter enables real-time validation of the token chain.

    Args:
        source (str): The source string being tokenized.
    """

    _source: str

    _variable_provided: bool
    _relation_provided: bool

    def __init__(self, source: str) -> None:
        self._source = source

        self._variable_provided = False
        self._relation_provided = False

    def lint(self, token: Token) -> None:
        """The lint method checks the token for integrity, validity and
        relevance. It raises a LinterException if the token is invalid
        or unexpected.

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
        if token.kind != TokenKind.SOF and (
            token.prev_token is None or token.prev_token.next_token is not token
        ):
            raise LinterException(
                self._source,
                token.location,
                "Crude modification of the token chain is detected",
            )

        if token.kind == TokenKind.EOF:
            self._lint_eof(token)

        if is_binary_operator(token):
            self._lint_binary_operator(token)

            self._variable_provided = False

        if token.kind == TokenKind.MUL:
            self._lint_multiplication_operator(token)

        if is_relational_operator(token):
            self._lint_relational_operator(token)

            self._variable_provided = False
            self._relation_provided = True

        if token.kind == TokenKind.VARIABLE:
            self._lint_variable(token)

            self._variable_provided = True

        if token.kind == TokenKind.COMMA:
            self._lint_comma(token)

            self._variable_provided = False

    def _lint_eof(self, token: Token) -> None:
        """Lint the EOF Token.

        Args:
            token (Token): The EOF Token.

        Raises:
            LinterException: Equation must contain a relational
                operator.
            LinterException: Unexpected binary operator at the end of
                the equation.
            LinterException: Unexpected EOF, right side of the equation
                is missed.
            LinterException: Unexpected comma at the end of the
                equation.
        """
        if token.prev_token.kind != TokenKind.SOF and not self._relation_provided:
            raise LinterException(
                self._source,
                token.location,
                "Equation must contain a relational operator",
            )
        if is_binary_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.prev_token.location,
                "Unexpected binary operator at the end of the equation",
            )
        if is_relational_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.location,
                "Unexpected EOF, right side of the equation is missed",
            )
        if token.prev_token.kind == TokenKind.COMMA:
            raise LinterException(
                self._source,
                token.location,
                "Unexpected comma at the end of the equation",
            )

    def _lint_binary_operator(self, token: Token) -> None:
        """Lint the binary operator Token.

        Args:
            token (Token): The binary operator Token.

        Raises:
            LinterException: Unexpected binary operator, term missed.
        """
        if is_binary_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.location,
                "Unexpected binary operator, term missed",
            )

    def _lint_multiplication_operator(self, token: Token) -> None:
        """Lint the multiplication operator Token.

        Args:
            token (Token): The multiplication operator Token.

        Raises:
            LinterException: Unexpected multiplication operator, term
                missed.
        """
        if token.prev_token.kind == TokenKind.MUL:
            raise LinterException(
                self._source,
                token.location,
                "Unexpected multiplication operator, term missed",
            )

    def _lint_relational_operator(self, token: Token) -> None:
        """Lint the relational operator Token.

        Args:
            token (Token): The relational operator Token.

        Raises:
            LinterException: Equation must contain only one relational
                operator.
            LinterException: Unexpected binary operator, term missed.
            LinterException: Unexpected relational operator, left side
                of the equation is missed.
        """
        if self._relation_provided:
            raise LinterException(
                self._source,
                token.location,
                "Equation must contain only one relational operator",
            )
        if is_binary_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.location,
                "Unexpected binary operator, term missed",
            )
        if token.prev_token.kind in (TokenKind.SOF, TokenKind.COMMA):
            raise LinterException(
                self._source,
                token.location,
                "Unexpected relational operator, left side of the equation is missed",
            )

    def _lint_variable(self, token: Token) -> None:
        """Lint the variable Token.

        Args:
            token (Token): The variable Token.

        Raises:
            LinterException: Term must contain no more than one
                variable.
        """
        if self._variable_provided:
            raise LinterException(
                self._source,
                token.location,
                "Term must contain no more than one variable",
            )

    def _lint_comma(self, token: Token) -> None:
        """Lint the comma Token.

        Args:
            token (Token): The comma Token.

        Raises:
            LinterException: Unexpected comma at the beginning of the
                equation.
            LinterException: Unexpected comma, equation missed.
            LinterException: Unexpected comma at the end of the
                equation.
        """
        if token.prev_token.kind == TokenKind.SOF:
            raise LinterException(
                self._source,
                token.location,
                "Unexpected comma at the beginning of the equation",
            )
        if not self._relation_provided:
            raise LinterException(
                self._source,
                token.location,
                "Equation must contain a relational operator",
            )
        if is_binary_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.prev_token,
                "Unexpected binary operator at the end of the equation",
            )
        if is_relational_operator(token.prev_token):
            raise LinterException(
                self._source,
                token.location,
                "Unexpected comma, right side of the equation is missed",
            )
        if token.prev_token.kind == TokenKind.COMMA:
            raise LinterException(
                self._source,
                token.location,
                "Unexpected comma, equation missed",
            )


__all__ = ("Linter",)
