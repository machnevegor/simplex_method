import numpy as np
from ast_parser.parser import EquationKind  # Assuming EquationKind is imported from another module

class Solver:
    """Solver takes in the equations which have been parsed from the input,
    it converts them to matrix arrays and applies the matrix operations on 
    them.

    Args:
        objective_functions (list of Equation objects): List of objective functions.
        constraints (list of Equation objects): List of constraint equations.
    """
    def __init__(self, objective_functions, constraints):
        # Extract objective function variables and negate their coefficients
        self.objective_functions = objective_functions[0].variables
        self.objective_functions.pop('Z')

        self.constraints = []

        for i, _ in enumerate(constraints):
            self.constraints.append(constraints[i])

        # Negate coefficients of objective function for maximization
        for key in self.objective_functions:
            self.objective_functions[key] *= -1

        # Add slack variables to constraints if necessary
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

        objective_values, solution, variable_names = self.advanced_simplex(A, B, C)
        variable_names = list(variable_names.values())
        print("The vector of decision variables is : ")
        for i in range(len(objective_values)):
            print(variable_names[i], ": ", round(objective_values[i, 0], 2))
        print("The optimal solution is ", solution , '\n')

    def convert_to_matrices(self):
        """Converts objective functions and constraints to matrices.

        Returns:
            A (numpy.ndarray): Coefficients matrix for constraints.
            B (numpy.ndarray): Right-hand side matrix for constraints.
            C (numpy.ndarray): Coefficients matrix for objective function.
        """
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
        """Performs the advanced simplex algorithm to find the optimal solution.

        Args:
            A (numpy.ndarray): Coefficients matrix for constraints.
            b (numpy.ndarray): Right-hand side matrix for constraints.
            C (numpy.ndarray): Coefficients matrix for objective function.

        Returns:
            objective_values (numpy.ndarray): The values of the objective function variables.
            solution (float): The optimal solution value.
        """
        n, m = A.shape

        B = np.eye(n)
        C_B = np.zeros((1, n))

        count = 0
        
        variable_names = list(self.objective_functions.keys())[-n:]  
        variable_names = {key: value for key, value in zip(range(n), variable_names)}
       
        prev_solution = float('inf')
        while True:
            count += 1
            B_inverse = np.around(np.linalg.inv(B), decimals=2)
            for row in B_inverse:
                for value in row:
                    if value == -0:
                        value = 0

            X_B = np.matmul(B_inverse, b)
            P_table = np.round(np.matmul(B_inverse, A), 2)
            objective_values = np.matmul(C_B, P_table) - C
            solution = np.round(np.matmul(C_B, X_B), 2)
            
            if abs(prev_solution - solution) < 0.0001:
                return X_B, solution, variable_names

            entering_var_idx = np.argmin(objective_values)

            ratios = []
            for i in range(n):
                if P_table[i, entering_var_idx] > 0:
                    ratios.append(X_B[i, 0] / P_table[i, entering_var_idx])
                else:
                    ratios.append(np.inf)  

            exiting_var_idx = np.argmin(ratios)
            
            temp_list = list(self.objective_functions.keys())

            variable_names[exiting_var_idx] = temp_list[entering_var_idx]
            B[:, exiting_var_idx] = A[:, entering_var_idx]
            C_B[:, exiting_var_idx] = C[:, entering_var_idx]
            prev_solution = solution