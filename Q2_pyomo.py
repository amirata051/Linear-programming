from pyomo.environ import *

model = ConcreteModel()

# Set
model.F = Set(initialize=[0, 1, 2])
model.C = Set(initialize=[0, 1, 2])

# Parameters
model.capacity = Param(model.F, initialize={0: 100, 1: 200, 2: 150})
model.fixed_cost = Param(model.F, initialize={0: 10, 1: 20, 2: 15})
model.operating_cost = Param(model.F, initialize={0: 1, 1: 2, 2: 1.5})
model.demand = Param(model.C, initialize={0: 50, 1: 80, 2: 120})

# Variables
model.x = Var(model.C, model.F, within=Binary)

# Objective
model.obj = Objective(expr=sum(
    model.fixed_cost[f] * model.x[c, f] + model.operating_cost[f] * model.demand[c] * model.x[c, f]
    for c in model.C for f in model.F
))

# Constraints
model.capacity_constraint = ConstraintList()
for f in model.F:
    model.capacity_constraint.add(
        sum(model.demand[c] * model.x[c, f] for c in model.C) <= model.capacity[f]
    )

# Solve
solver = SolverFactory('glpk')
results = solver.solve(model)

# Print Results
print("Best Solution:")
for c in model.C:
    for f in model.F:
        if model.x[c, f].value > 0.5:
            print(f"Customer {c} -> Facility {f}")

print("Best Cost:", model.obj())
