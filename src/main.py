from ast_parser import Lexer, LinterException, lint

lexer = Lexer(
    """                            5 x_1

+ 3x_2 - 4 * _y3  2          - 8 XXXX_7

      ≤ 19 * .5"""
)

tokens = lexer.tokenize()

for token in tokens:
    print(token, "\n")

try:
    lint(tokens[0], lexer.source)
except LinterException as e:
    print("ERROR", e.location, e.args[0])
