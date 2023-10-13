# simplex_method
🔬 Implementation of simplex method.

Welcome to the Simplex Method Solver project! This program is designed to help you solve linear programming problems using the simplex method, with a focus on maximization objectives. You can access and use this solver through our website without the need for complex installations.

## Table of Contents
- [Introduction](#introduction)
- [Team](#team)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Run_Locally](#run_locally)

## Introduction

The program primarily handles maximization problems. 

## Team

- Adewuyi Israel Oluwajuwon
- Egor Machnev
- Khush Patel
- Yehia Sobeh
- Hadi Salloum
- Mike Tezin

## Features

- **Maximization Solver:** Focuses on solving maximization linear programming problems.
- **Web-based Interface:** Use the solver through your web browser without the need for installation.
- **Intuitive User Interface:** Our user-friendly interface makes it easy to input your linear programming problem and obtain the optimal solution.

## Getting Started

To get started with the Maximization Simplex Method Solver, simply follow these steps:

1. Visit our website at [MAX_SIMPLEX_SOLVER](https://huggingface.co/spaces/khushpatel2002/Optimization).
2. Input your linear programming problem in the specified format. The solver will guide you through the process.
3. Click the "Submit" button to find the optimal solution.
4. Review the solution.

## Usage

Using the Maximization Simplex Method Solver is straightforward:

1. **Input Your Problem:** Enter your linear programming problem. All equations should already be in standard form, meaning, aside the
   the objective function, the inequality present should be "<=". Each equation should also be separated by a comma.
   ```
    variables  --> x_1, x_2, ...
    inequality --> <=
    objective function --> Z
   ```

3. **Solve:** Click the "Submit" button to initiate the solver.

4. **Review Solution:** Examine the solution to understand the optimal values of your decision variables and the optimal objective function value.


## Dependencies

The only package required to run this program is [NumPy](https://numpy.org). You can easily install it using pip:

```bash
pip install numpy
```
### Run_Locally

To run locally:
1. Clone the repository
```bash
git clone https://github.com/machnevegor/simplex_method
```
2. Install the dependency
```bash
pip install numpy
```
3. cd into the folder and run the main.py
```bash
main.py
```


Enjoy!
