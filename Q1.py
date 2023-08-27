from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define variables
model.x1 = Var(within=NonNegativeReals)
model.x2 = Var(within=NonNegativeReals)
model.y1 = Var(within=NonNegativeIntegers)
model.y2 = Var(within=NonNegativeIntegers)
model.y3 = Var(within=Binary)
model.y4 = Var(within=Binary)

# Define the objective function
model.obj = Objective(
    expr=2 * model.x1 + 3 * model.x2 + 4 * model.y1 + model.y2 + model.y3 + 2 * model.y4,
    sense=maximize
)

# Define the constraints
model.con1 = Constraint(expr=model.x1 + 2 * model.x2 + 3 * model.y1 + 2 * model.y2 + model.y3 + 3 * model.y4 <= 12)
model.con2 = Constraint(expr=3 * model.x1 - 2 * model.x2 - model.y1 + 2 * model.y2 - 2 * model.y3 - 3 * model.y4 >= 5)
model.con3 = Constraint(expr=2 * model.y1 + model.y3 + model.y4 >= 4)
model.con4 = Constraint(expr=model.y1 + 2 * model.y2 >= 5)

# Solve the MILP using the Branch and Bound algorithm
solver = SolverFactory('cbc')  # Choose the solver
results = solver.solve(model, tee=True, strategy='branch-and-bound')

# Print the results
print(results)

# Access the optimal solution
optimal_solution = model.obj()
print(f"Optimal Solution: {optimal_solution}")
print(f"x1: {model.x1.value}")
print(f"x2: {model.x2.value}")
print(f"y1: {model.y1.value}")
print(f"y2: {model.y2.value}")
print(f"y3: {model.y3.value}")
print(f"y4: {model.y4.value}")