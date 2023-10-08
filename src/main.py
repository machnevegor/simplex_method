from ast_parser.parser import Parser

# parser = Parser(
#     """                            5 x_1

# + 3x_2 - 4 * _y3  2          - 8 XXXX_7  - 4 * _y3  2

#       ≤ 19 * 5, 5 <= - 3 * x"""
# )

parser = Parser(
    #Tatar Paint Optimization Problem constraints
    """
        6x_1 + 4x_2 <= 24,

        x_1 + 2x_2 <= 6,

        x_1 + x_2 <= 1,

        x_2 <= 2,

        Z = 5x_1 + 4x_2
    """
)

for equation in parser:
    print(equation)
