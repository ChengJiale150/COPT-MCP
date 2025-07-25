import coptpy as cp
from coptpy import COPT

def main():
    """
    The problem to solve:

    Maximize:
        1.2 x + 1.8 y + 2.1 z

    Subject to:
        1.5 x + 1.2 y + 1.8 z <= 2.6
        0.8 x + 0.6 y + 0.9 z >= 1.2

    where:
        0.1 <= x <= 0.6
        0.2 <= y <= 1.5
        0.3 <= z <= 2.8
    """

    # Create COPT environment
    env = cp.Envr()

    # Create COPT model
    model = env.createModel("lp_ex1")

    # Add variables: x, y, z
    x = model.addVar(lb=0.1, ub=0.6, name="x")
    y = model.addVar(lb=0.2, ub=1.5, name="y")
    z = model.addVar(lb=0.3, ub=2.8, name="z")

    # Add constraints
    model.addConstr(1.5*x + 1.2*y + 1.8*z <= 2.6)
    model.addConstr(0.8*x + 0.6*y + 0.9*z >= 1.2)

    # Set objective function
    model.setObjective(1.2*x + 1.8*y + 2.1*z, sense=COPT.MAXIMIZE)

    # Set parameter
    model.setParam(COPT.Param.TimeLimit, 10.0)

    # Solve the model
    model.solve()

    # Analyze solution
    if model.status == COPT.OPTIMAL:
        print("Objective value: {}".format(model.objval))
    allvars = model.getVars()

    print("Variable solution:")
    for var in allvars:
        print(" x[{0}]: {1}".format(var.index, var.x))

    print("Variable basis status:")
    for var in allvars:
        print(" x[{0}]: {1}".format(var.index, var.basis))


if __name__ == "__main__":
    main()
