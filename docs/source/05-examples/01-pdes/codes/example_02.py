
import petsc4py
import sys
import numpy as np
import matplotlib.pyplot as plt

petsc4py.init(sys.argv)

from petsc4py import PETSc

DX = 0.02
DT = 0.01
T0 = 1.0
N_POINTS = int(1/DX)+1
N_TIME_STEPS = int(T0/DT)+1

AA = 1.0
ALPHA = 0.01
CC = AA*DT/DX
SS = ALPHA*DT/DX**2

def exact_solution(x, t: float):
    c1 = 0.025/np.sqrt(0.000625+0.02*t)
    c2 = 0.00125 + 0.04*t
    uu = (x+0.5-t)**2
    uu = c1*np.exp(-uu/c2)
    return uu

def initial_condition(mesh: np.ndarray):
    #return np.exp(-(mesh+0.5)**2/0.00125)
    return np.zeros_like(mesh)

def boundary_condition_0(t: float):
    c1 = 0.025/np.sqrt(0.000625+0.02*t)
    c2 = 0.00125 + 0.04*t
    return c1*np.exp(-(0.5-t)**2/c2)

def boundary_condition_1(t: float):
    c1 = 0.025/np.sqrt(0.000625+0.02*t)
    c2 = 0.00125 + 0.04*t
    return c1*np.exp(-(1.5-t)**2/c2)

# ==================================================
# Sphinx doc `include` start

def lax_wendroff(mesh: np.array):
    
    print('Lax-Wendroff')
    
    def step(un: np.array, t: float):
        
        c1 = 0.5*(2*SS+CC+CC**2)
        c2 = 1-2*SS-CC**2
        c3 = 0.5*(2*SS-CC+CC**2)
        uu = np.zeros_like(un)
        
        uu[0] = boundary_condition_0(t)
        uu[-1]= boundary_condition_1(t)
        
        for i in range(1, N_POINTS-1):
            uu[i] = c1*un[i-1] + c2*un[i] +c3*un[i+1]

        return uu
    
    current_solution = initial_condition(mesh)
    
    for iter in range(N_TIME_STEPS):
        
        t = (iter+1)*DT
        current_solution = step(current_solution, t)
    
    return current_solution

def crank_nicolson(mesh: np.ndarray):

    def ndarray_b(un: np.ndarray):
        
        bb = np.zeros_like(un)

        _c1 = CC+2*SS
        _c2 = 4-4*SS
        _c3 = -(CC-2*SS)
    
        bb[0] = un[0]
        bb[-1]= un[-1]
    
        for i in range(1, N_POINTS-1):
            bb[i] = _c1*un[i-1] + _c2*un[i] + _c3*un[i+1]
        
        return bb

    c1 = -(CC+2*SS)
    c2 = 4+4*SS
    c3 = CC-2*SS

    # Create a new sparse PETSc matrix, fill it and then assemble it
    A = PETSc.Mat().createAIJ([N_POINTS, N_POINTS])
    A.setUp()
    
    A.setValue(0, 0, 1.0)
    A.setValue(N_POINTS-1, N_POINTS-1, 1.0)
    
    for i in range(1, N_POINTS-1):
        A.setValue(i, i-1, c1)
        A.setValue(i, i,   c2)
        A.setValue(i, i+1, c3)
    A.assemble()

    # Assemble the initial rhs to the linear system
    b = PETSc.Vec().createSeq(N_POINTS)
    b.setArray(ndarray_b(initial_condition(mesh)))

    # Allocate a PETSc vector storing the solution to the linear system
    x = PETSc.Vec().createSeq(N_POINTS)

    # Instantiate a linear solver: Krylow subspace linear iterative solver
    ksp = PETSc.KSP().create()
    ksp.setOperators(A)
    ksp.setFromOptions()
    
    chosen_solver = ksp.getType()
    print('Crank-Nicolson [solver: %s]'%(chosen_solver))
    
    for iter in range(N_TIME_STEPS):
        
        t = (iter+1)*DT
        ksp.solve(b, x)

        # Re-assemble the rhs to move forward in time
        current_solution = x.getArray()
        current_solution[0] = boundary_condition_0(t)
        current_solution[-1]= boundary_condition_1(t)

        b.setArray(ndarray_b(current_solution))
    
    return current_solution

# Sphinx doc `include` end  
# ==================================================

if __name__ == "__main__":
    
    mesh = np.linspace(0.0, 1.0, N_POINTS)

    sol1 = lax_wendroff(mesh)
    sol2 = crank_nicolson(mesh)

    plt.figure()
    plt.plot(mesh, exact_solution(mesh, T0), 'r')
    plt.plot(mesh, sol1, 'b--')
    plt.plot(mesh, sol2, 'g.')
    plt.legend(['exact', 'lax', 'crank'])
    plt.savefig('../figures/example_02.jpg', dpi=300)
    
    