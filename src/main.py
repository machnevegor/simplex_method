from ast_parser.parser import Parser

parser = Parser(
    """                            5 x_1

+ 3x_2 - 4 * _y3  2          - 8 XXXX_7  - 4 * _y3  2

      ≤ 19 * 5, 5 <= - 3 * x"""
)

for equation in parser.parse():
    print(equation, "\n")
