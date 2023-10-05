from src.ast_parser import Lexer

lexer = Lexer("""                            5 x_1

+ 3x_2 - 4 * _y3  2          - 8 XXXX_7

      ≤ 19 * .5""")

print(*lexer, sep="\n\n")
