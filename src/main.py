from ast_parser import Parser, EquationKind
from algorithm import solver

print("Enter constraints in the format '6x_1 + 4x_2 <= 24,' (end with a comma) followed by \n")
print("the objective function in the format 'Z = 5x_1 + 4x_2' (no comma).")
input_equation = input()

parser = Parser(input_equation)


equations = tuple(parser)

for equation in equations:
    if equation.kind == EquationKind.GEQ and equation.bound < 0.0:
        for variable, coefficient in equation.variables.items():
            equation.variables[variable] *= -1.0

        equation.bound *= -1.0
        equation.kind = EquationKind.LEQ

        continue

    if equation.kind == EquationKind.GEQ:
        raise ValueError("Equation kind must be either EQ or LEQ")
    if equation.bound < 0.0:
        raise ValueError("Equation bound must be non-negative")

demand: dict[str, list[int]] = {}
for i, equation in enumerate(equations):
    for variable, coefficient in equation.variables.items():
        if coefficient == 0.0:
            continue

        if variable not in demand:
            demand[variable] = []

        demand[variable].append(i)

objective_variables = tuple(
    filter(lambda variable: len(demand[variable]) == 1, demand.keys())
)

objective_functions = tuple(
    filter(
        lambda function: function.kind == EquationKind.EQ,
        map(lambda variable: equations[demand[variable][0]], objective_variables),
    )
)

if len(objective_variables) != len(objective_functions):
    raise ValueError("Objective functions must be equalities")

constraints = tuple(
    filter(
        lambda function: function not in objective_functions,
        equations,
    )
)

solver.Solver(objective_functions, constraints)