
import petsc4py
import sys
import numpy as np
import matplotlib.pyplot as plt

petsc4py.init(sys.argv)

from petsc4py import PETSc

N_POINTS = 1001
TIME_STEP_LENGTH = 0.005
N_TIME_STEPS = 10

def main():
    
    element_length = 1.0 / (N_POINTS - 1)
    mesh = np.linspace(0.0, 1.0, N_POINTS)

    # Create a new sparse PETSc matrix, fill it and then assemble it
    A = PETSc.Mat().createAIJ([N_POINTS, N_POINTS])
    A.setUp()

    diagonal_entry = 1.0 + 2.0 * TIME_STEP_LENGTH / element_length**2
    off_diagonal_entry = - 1.0 * TIME_STEP_LENGTH / element_length**2

    A.setValue(0, 0, 1.0)
    A.setValue(N_POINTS-1, N_POINTS-1, 1.0)

    for i in range(1, N_POINTS - 1):
        A.setValue(i, i, diagonal_entry)
        A.setValue(i, i-1, off_diagonal_entry)
        A.setValue(i, i+1, off_diagonal_entry)
    
    A.assemble()

    # Define the initial condition
    initial_condition = np.where(
        (mesh > 0.3) & (mesh < 0.5),
        1.0,
        0.0,
    )

    # Assemble the initial rhs to the linear system
    b = PETSc.Vec().createSeq(N_POINTS)
    b.setArray(initial_condition)
    b.setValue(0, 0.0)
    b.setValue(N_POINTS-1, 0.0)

    # Allocate a PETSc vector storing the solution to the linear system
    x = PETSc.Vec().createSeq(N_POINTS)

    # Instantiate a linear solver: Krylow subspace linear iterative solver
    ksp = PETSc.KSP().create()
    ksp.setOperators(A)
    ksp.setFromOptions()

    chosen_solver = ksp.getType()
    print(f"Solving with {chosen_solver:}")
    
    plt.plot(mesh, initial_condition)

    for iter in range(N_TIME_STEPS):
        ksp.solve(b, x)

        # Re-assemble the rhs to move forward in time
        current_solution = x.getArray()
        b.setArray(current_solution)
        b.setValue(0, 0.0)
        b.setValue(N_POINTS - 1, 0.0)

        # Visualize
        plt.plot(mesh, current_solution)        

    plt.savefig('../figures/example_01.jpg', dpi=300)


if __name__ == "__main__":
    main()
