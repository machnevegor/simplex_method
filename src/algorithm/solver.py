import numpy as np
from ast_parser.parser import Problem

def convert_to_numpy_matrix(problem):
    num_constraints = len(problem.constraints)
    num_variables = len(problem.function)

    matrix = np.zeros((num_constraints, num_variables + 1))
    for i, constraint in enumerate(problem.constraints):
        for variable_name, coefficient in constraint.variables.items():
            j = list(problem.function.keys()).index(variable_name)
            matrix[i, j] = coefficient

        matrix[i, -1] = constraint.solution

    return matrix

if __name__ == "__main__":
    # Parse the LP problem using the parser.py module and create a Problem object
    problem = Problem()
    # Convert the Problem object to a numpy matrix
    # Solve the linear programming problem using the advanced simplex method
    
