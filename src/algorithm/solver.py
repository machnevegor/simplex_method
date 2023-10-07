import numpy as np
from ast_parser.parser import Problem, Constraint, ProblemKind
from ast_parser.token import TokenKind

def advanced_simplex(A, b, C):
    n, m = A.shape

    B = np.zeros((n, m - n))
    C_B = np.zeros((1, n))

    print(n, m, "\n")

    print("I got here")

    for i in range(n):
        for j in range(m - n):
            B[i, j] = A[i, j]

    for i in range(n):
        C_B[0, i] = C[0, i]

    B_inverse = np.linalg.inv(B)
    X_B = np.matmul(B_inverse, b)
    P_table = np.round(np.matmul(B_inverse, A), 3)

    objective_values = np.matmul(C_B, P_table) - C

    solution = np.round(np.matmul(C_B, X_B), 2)


    print(B, "\n")
    print(C_B, '\n')
    print(B_inverse, '\n')
    print(X_B, "\n")
    print(P_table, '\n')
    print(objective_values, '\n')
    print(solution)


def convert_to_numpy_matrices(problem):
    num_constraints = len(problem.constraints)
    num_variables = len(problem.function)

    A = np.zeros((num_constraints, num_variables))
    C = np.zeros((1, num_variables))

    B = np.zeros((num_constraints, 1))

    
    for i, constraint in enumerate(problem.constraints):
        for variable_name, coefficient in constraint.variables.items():
            j = list(problem.function.keys()).index(variable_name)
            A[i, j] = coefficient

        for variable_name, coefficient in problem.function.items():
            j = list(problem.function.keys()).index(variable_name)
            C[0, j] = coefficient

        B[i, 0] = constraint.solution

    return A, B, C

def Solver():
    problem_kind = ProblemKind.MAX
    objective_function = {"x_1": 1, "x_2": 4, "x_3": 7, "x_4":5}
    constraints = [
        Constraint(kind=TokenKind.EQ, variables={"x_1": 2, "x_2": 1, "x_3": 2, "x_4": 4}, solution=10),
        Constraint(kind=TokenKind.EQ, variables={"x_1": 3, "x_2": -1, "x_3": -2, "x_4": 6}, solution=5),
    ]

    problem = Problem(problem_kind, objective_function, constraints)

    A, b, C = convert_to_numpy_matrices(problem)

    print(A)
    print("This is b:", b)
    print("This is C:", C)

    advanced_simplex(A, b, C)