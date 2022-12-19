
import matplotlib.pyplot as plt
import numpy as np
from euler1d import Roe, Reconstruction, initialization, pressure, GAMMA
from typing import List

N_POINTS = 201
I_PROBLEM = 0

T0 = 0.25

DS_PHI = 0.5     # Dual step coefficient: phi
RATIO_LAMBDA = 1.01

CFL = 0.8
N_PHYSICAL_STEP = 100
N_PSEUDO_STEP = 5


class Cell():
    '''
    Data of each cell
    '''
    def __init__(self) -> None:
        
        # conserved variables: [rho, rho u, rho E]
        # primitive variables: [rho, u, p]
        
        #* Physical step n-1
        self.U_nm1 = np.zeros(3)    # conserved variables (physical step n-1)
        
        #* Physical step n
        self.U_n = np.zeros(3)      # conserved variables (physical step n)

        #* pseudo step m
        self.U_m = np.zeros(3)      # conserved variables (pseudo step m)
        self.DU_m = np.zeros(3)     # difference of the conserved variables (pseudo step m)
        self.DU_star = np.zeros(3)  # temporal DU* after L sweep (pseudo step m)
        self.residual = np.zeros(3) # the right hand side of the dU/dt=Res
        
        self.abs_eigenvalues = np.zeros(3)  # absolute eigenvalues [abs(u+a), abs(u), abs(u-a)]
        self.lambda_max_m = 0.0             # maximum absolute eigenvalue of Jacobin A
        self.mA_m = np.zeros([3,3])         # Jacobin A = dF/dU
        
        self.pseudo_dt = 0.0        # pseudo time step
        self.ratio_lu = 0.0         # ratio of (RHS + [A+]DU) or [A-]DU
    
    @staticmethod
    def JacobinA(u: float, tE: float) -> np.ndarray:
        '''
        >>> mA = Cell.JacobinA(U[1]/U[0], U[2]/U[0])
        '''
        u2 = u**2
        gE = tE*GAMMA
        
        mA = np.zeros([3,3])
        mA[0,0] = 0
        mA[0,1] = 1
        mA[0,2] = 0
        mA[1,0] = 0.5*(GAMMA-3)*u2
        mA[1,1] = (3-GAMMA)*u
        mA[1,2] = GAMMA - 1
        mA[2,0] = (GAMMA-1)*u*u2 - gE*u
        mA[2,1] = -1.5*(GAMMA-1)*u2 + gE
        mA[2,2] = GAMMA*u
        
        return mA
    
    @staticmethod
    def JacobinA_plus (mA: np.ndarray, lambda_max_m: float, ratio=1.01) -> np.ndarray:
        return 0.5*(mA + np.eye(3)*lambda_max_m*ratio)
    
    @staticmethod
    def JacobinA_minus(mA: np.ndarray, lambda_max_m: float, ratio=1.01) -> np.ndarray:
        return 0.5*(mA - np.eye(3)*lambda_max_m*ratio)
    
    
def explicit_residual(Um2, Um1, U, Up1, Up2) -> np.ndarray:
    '''
    Calculate the right hand side of the (1/J) dU/dt = Res
    '''
    uUL, uUR = Reconstruction.Upwind1_TVD(Um2, Um1, U, Up1,
                limiter=Reconstruction.min_mod)

    fFaceL = Roe.flux_face(uUL, uUR)

    uUL, uUR = Reconstruction.Upwind1_TVD(Um1, U, Up1, Up2,
                limiter=Reconstruction.min_mod)
    
    fFaceR = Roe.flux_face(uUL, uUR)

    res = - (fFaceR - fFaceL)
        
    return res
    

def LU_SGS(physical_dt: float, dx: float, cfl: float, cells: List[Cell], n_pseudo_steps: int, phi: float):
    '''
    Update cell.U_n (need initial U_n & U_nm1)
    '''
    #* Initialization
    for i in range(len(cells)):
        cells[i].U_m = cells[i].U_n.copy()

    #* Pseudo time iteration: L-U sweep
    for i_pseudo in range(n_pseudo_steps):

        #* Preparation of all cells (m)
        for i in range(2, N_POINTS-1):

            #* primitive variables 
            rho = cells[i].U_m[0]
            u   = cells[i].U_m[1]/rho
            tE  = cells[i].U_m[2]/rho
            p   = (GAMMA-1)*(tE-0.5*rho*u**2)
            a   = np.sqrt(GAMMA*p/rho)
            
            #* Calculate eigenvalues
            cells[i].abs_eigenvalues = np.array([abs(u+a), abs(u-a), abs(u)])
            cells[i].lambda_max_m = np.max(cells[i].abs_eigenvalues)
            
            #* Calculate pseudo_dt
            cells[i].pseudo_dt = cfl*dx/cells[i].lambda_max_m
            
            #* Calculate residual R(U(m))
            cells[i].residual = explicit_residual(
                cells[i-2].U_m, cells[i-1].U_m, cells[i].U_m, cells[i+1].U_m, cells[i+2].U_m)
            
            #* Calculate [A]
            cells[i].mA_m = Cell.JacobinA(u, tE)
            
            #* Calculate ratio of (RHS+[A+] DU) or [A-] DU
            denominator = dx/cells[i].pseudo_dt + (1+phi)*dx/physical_dt \
                        + RATIO_LAMBDA*cells[i].lambda_max_m
            cells[i].ratio_lu = 1.0/denominator


        #* L sweep
        for i in range(2, N_POINTS-1):
            
            II = i-1

            #* Calculate [A+]
            mAp = Cell.JacobinA_plus(cells[II].mA_m, cells[II].lambda_max_m, ratio=RATIO_LAMBDA)
            
            #* Calculate RHS
            rhs  =    phi *dx/physical_dt*(cells[i].U_n-cells[i].U_nm1)
            rhs -= (1+phi)*dx/physical_dt*(cells[i].U_m-cells[i].U_n)
            rhs += cells[i].residual

            #* Calculate dU*
            numerator = rhs + np.dot(mAp, cells[II].DU_m)
            cells[i].DU_star = cells[i].ratio_lu * numerator
        
        
        #* U sweep
        for i in range(N_POINTS-1, 2, -1):
            
            II = i+1
            
            #* Calculate [A-]
            mAm = Cell.JacobinA_minus(cells[II].mA_m, cells[II].lambda_max_m, ratio=RATIO_LAMBDA)
            
            #* Calculate dU(m)
            numerator = np.dot(mAm, cells[II].DU_m)
            cells[i].DU_m = cells[i].DU_star + cells[i].ratio_lu * numerator
            
            
        #* Update conserved variables
        for i in range(2, N_POINTS-1):
            cells[i].U_m = cells[i].U_m + cells[i].DU_m
    
    
    #* Update conserved variables
    for i in range(2, N_POINTS-1):
        cells[i].U_nm1 = cells[i].U_n.copy()
        cells[i].U_n   = cells[i].U_m.copy()


    #* Residual
    residual = {}
    residual['physical-density'] = np.max([abs(cell.U_n[0] - cell.U_nm1[0]) for cell in cells[2:N_POINTS-1]])
    residual['pseudo-density']   = np.max([abs(cell.DU_m[0]) for cell in cells[2:N_POINTS-1]])
    
    return residual


if __name__ == "__main__":
    
    physical_dt = T0/N_PHYSICAL_STEP
    
    mesh, initial_solution, DX = initialization(N_POINTS, I_PROBLEM)

    cells = [Cell() for _ in range(mesh.shape[0])]
    for i in range(mesh.shape[0]):
        cells[i].U_n   = initial_solution[i,:].copy()
        cells[i].U_nm1 = initial_solution[i,:].copy()

    phi = 0.0
    for i_physical in range(N_PHYSICAL_STEP):
        
        if i_physical >= 2:
            phi = DS_PHI
        
        residual = LU_SGS(physical_dt, DX, CFL, cells, N_PSEUDO_STEP, phi)
        
        print('Physical time = %.3f | pseudo residual = %.3E (%.3E)'%(
            (i_physical+1)/N_PHYSICAL_STEP*T0, residual['pseudo-density'], 
            residual['pseudo-density']/residual['physical-density']))

    solution = np.zeros_like(initial_solution)
    for i in range(mesh.shape[0]):
        solution[i,:] = cells[i].U_n
    
    plt.figure()

    with open('../figures/example_01_exact_%d.dat'%(I_PROBLEM), 'r') as f:

        exact_mesh = []
        exact_solution = []
        
        lines = f.readlines()
        for line in lines:
            line = line.split()
            exact_mesh.append(float(line[0]))
            exact_solution.append([float(line[1]), float(line[2]), float(line[3])])
            
        exact_mesh = np.array(exact_mesh)
        exact_solution = np.array(exact_solution)
        
        plt.plot(exact_mesh[2:N_POINTS-1], pressure(exact_solution[2:N_POINTS-1, :]), 'k') 

    plt.plot(mesh[2:N_POINTS-1], pressure(solution[2:N_POINTS-1, :]), 'r--')
    
    plt.title('pressure')
    plt.legend(['exact', 'Roe (n= %d, %d)'%(N_PHYSICAL_STEP, N_PSEUDO_STEP)])
    plt.savefig('../figures/example_02.jpg', dpi=300)


        
        
        
        