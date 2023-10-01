from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TokenKind(str, Enum):
    EOF = "<EOF>"
    SOF = "<SOF>"

    ADD = "+"
    MUL = "*"
    SUB = "-"

    PAREN_L = "("
    PAREN_R = ")"

    EQUALS = "="

    COEFFICIENT = "Coefficient"
    VARIABLE = "Variable"


@dataclass
class Token:
    kind: TokenKind
    start: int
    end: int

    value: str

    prev_token: Token | None = field(repr=False, default=None)
    next_token: Token | None = field(repr=False, default=None)


class Lexer:
    source: str
    last_token: Token
    token: Token

    def __init__(self, source: str) -> None:
        self.source = source
        self.token = Token(TokenKind.SOF, 0, 0, "")

    def _next_token(self) -> Token:
        position = self.token.end
        
        while position < len(self.source):
            char = self.source[position]
            
            
        
        
        
        

class Parser:
    _lexer: Lexer

    def __init__(self, source: str) -> None:
        self._lexer = Lexer(source)


__all__ = ["Parser"]
