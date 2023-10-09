import numpy as np
from ast_parser.parser import EquationKind

import numpy as np

class Solver:
    def __init__(self, objective_functions, constraints):
        self.objective_functions = objective_functions[0].variables
        self.objective_functions.pop('Z')

        self.constraints = []

        for i, _ in enumerate(constraints):
            self.constraints.append(constraints[i])

        for key in self.objective_functions:
            self.objective_functions[key] *= -1

        for temp_dict in constraints:
            for key in self.objective_functions.keys():
                if key not in temp_dict.variables:
                    temp_dict.variables[key] = 0
                
        slack = len(self.constraints)
        i = 0
        
        for _, constraint in enumerate(self.constraints):
            if constraint.kind == EquationKind.LEQ:
                constraint.variables["s_" + str(i)] = 1.0
                self.objective_functions["s_" + str(i)] = 0
                i += 1

        while i < slack:
            constraint.variables["s_" + str(i)] = 1.0
            self.objective_functions["s_" + str(i)] = 0
            i += 1

        A, B, C = self.convert_to_matrices()

        objective_values, solution = self.advanced_simplex(A, B, C)

        print("The vector of decision variables is : " , objective_values, '\n')
        print("The optimal solution is ", solution , '\n')

    
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

    def advanced_simplex(self, A, b, C):
        n, m = A.shape

        B = np.eye(n)
        C_B = np.zeros((1, n))

        count = 0

        prev_solution = float('inf')
        while True:
            count += 1
            B_inverse = np.around(np.linalg.inv(B), decimals=2)
            for row in B_inverse:
                for value in row:
                    if value == -0:
                        value = 0

            X_B = np.matmul(B_inverse, b)
            P_table = np.round(np.matmul(B_inverse, A), 4)
            objective_values = np.matmul(C_B, P_table) - C
            solution = np.round(np.matmul(C_B, X_B), 4)
            
            if abs(prev_solution - solution) < 0.0001:
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
            C_B[:, exiting_var_idx] = C[:, entering_var_idx]
            prev_solution = solution