from .lexer import Lexer


class Parser:
    _lexer: Lexer

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)


__all__ = ("Parser",)
