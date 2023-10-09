import numpy as np
from ast_parser.parser import EquationKind, Equation
# from ast_parser.token import TokenKind

import numpy as np

class Solver:
    def __init__(self, objective_functions, constraints):
        self.objective_functions = objective_functions[0].variables
        self.objective_functions.pop('Z')

        self.constraints = []

        for i, _ in enumerate(constraints):
            self.constraints.append(constraints[i])
        
        # print(type(self.objective_functions), '\n')
        # print(type(self.constraints))

        for temp_dict in constraints:
            for key in self.objective_functions.keys():
                if key not in temp_dict.variables:
                    temp_dict.variables[key] = 0
        
        for i, constraint in enumerate(self.constraints):
            if constraint.kind == EquationKind.LEQ:
                constraint.variables["s_" + str(i)] = 1.0
                self.objective_functions["s_" + str(i)] = 0

        # print(self.constraints)
        A, B, C = self.convert_to_matrices()

        print(A, '\n')
        print(B, '\n')
        print(C, '\n')
        # objective_values, solution = self.advanced_simplex(A, B, C)

        # print("The vector of decision variables is : " , objective_values, '\n')
        # print("The optimal solution is ", solution , '\n')


    
    def convert_to_matrices(self):
        num_constraints = len(self.constraints)
        num_variables = len(self.objective_functions)

        A = np.zeros((num_constraints, num_variables))
        C = np.zeros((1, num_variables))
        B = np.zeros((num_constraints, 1))


        for i, constraint in enumerate(self.constraints):
            for variable_name, coefficient in constraint.variables.items():
                j = list(self.objective_functions.keys()).index(variable_name)
                A[i, j] = coefficient

            for variable_name, coefficient in self.objective_functions.items():
                j = list(self.objective_functions.keys()).index(variable_name)
                C[0, j] = coefficient

            B[i, 0] = constraint.bound

        return A, B, C

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