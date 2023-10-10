import numpy as np
import matplotlib.pyplot as plt

def plot_2d(C, A, B, initial_point):
    n_constraints = A.shape[0]  # Get the number of constraints

    plt.figure(figsize=(8, 6))
    plt.xlim(0, 5)  # Adjust based on your problem
    plt.ylim(0, 5)  # Adjust based on your problem
    plt.xlabel('X1')
    plt.ylabel('X2')

    # Plot feasible region (constraints)
    x1 = np.linspace(0, 5, 100)
    
    for i in range(n_constraints):
        x2_i = (B[i] - A[i, 0] * x1) / A[i, 1]  # Calculate x2 values for each constraint
        plt.plot(x1, x2_i, label=f'{A[i, 0]}*X1 + {A[i, 1]}*X2 <= {B[i]}')

    # Fill the feasible region
    min_x2 = np.minimum.reduce([(B[i] - A[i, 0] * x1) / A[i, 1] for i in range(n_constraints)])
    plt.fill_between(x1, min_x2, 0, where=(x1 >= 0) & (x1 <= 5), alpha=0.2)

    # Plot the initial feasible solution point
    plt.scatter(initial_point[0], initial_point[1], color='red', marker='o', label='Initial Point')

    plt.legend()
    plt.show()

# Example usage with variable-sized A and B:
C = np.array([2, 3])  # Objective function coefficients
A = np.array([[1, 1],  # Constraint matrix
              [2, 1],
              [3, 1]])  # Add more rows for additional constraints
B = np.array([4, 5, 6])  # Right-hand side, add more values for additional constraints
initial_point = np.array([1.0, 3.0])
plot_2d(C, A, B, initial_point)
