import numpy as np
from ast_parser.parser import Problem, Constraint, ProblemKind
from ast_parser.token import TokenKind

def advanced_simplex(A, b, C):
    n, m = A.shape

    B = np.zeros((n, n))
    C_B = np.zeros((1, n))

    for i in range(n):
        for j in range(n):
            B[i, j] = A[i, j]

    for i in range(n):
        C_B[0, i] = C[0, i]

    while True:
        B_inverse = np.linalg.inv(B)
        X_B = np.matmul(B_inverse, b)
        P_table = np.round(np.matmul(B_inverse, A), 3)
        objective_values = np.matmul(C_B, P_table) - C
        solution = np.round(np.matmul(C_B, X_B), 2)

        if np.all(objective_values >= 0):
            return X_B, solution

        entering_var_idx = np.argmin(objective_values)

        ratios = []
        for i in range(n):
            if P_table[i, entering_var_idx] > 0:
                ratios.append(X_B[i, 0] / P_table[i, entering_var_idx])
            else:
                ratios.append(np.inf)  

        exiting_var_idx = np.argmin(ratios)

        B[:, exiting_var_idx] = A[:, entering_var_idx]


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
    objective_function = {"x_1": 5, "x_2": 4}
    constraints = [
        Constraint(kind=TokenKind.LEQ, variables={"x_1": 6, "x_2": 4}, solution=24),
        Constraint(kind=TokenKind.LEQ, variables={"x_1": 1, "x_2": 2}, solution=6),
        Constraint(kind=TokenKind.LEQ, variables={"x_1": -1, "x_2": 1}, solution=1),
        Constraint(kind=TokenKind.LEQ, variables={"x_1": 0, "x_2": 1}, solution=2)
    ]

    for i, constraint in enumerate(constraints):
        if constraint.kind == TokenKind.LEQ:
            constraint.variables["s_" + str(i)] = 1.0
            objective_function["s_" + str(i)] = 0

    constraints = list(constraints)

    problem = Problem(problem_kind, objective_function, constraints)

    A, b, C = convert_to_numpy_matrices(problem)


    # print(A)
    # print("This is b:", b)
    # print("This is C:", C)

    objective_values, solution = advanced_simplex(A, b, C)

    print("The vector of decision variables is : " , objective_values, '\n')
    print("The optimal solution is ", solution , '\n')