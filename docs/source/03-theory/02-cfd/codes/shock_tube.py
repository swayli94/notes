
import matplotlib.pyplot as plt
import numpy as np
from euler1d import AUSM, GAMMA, Exact, Roe, Reconstruction, pressure, time_step


N_POINTS = 201
I_PROBLEM = 0
T0 = 0.25


def initialization():
    
    sol = np.zeros([N_POINTS+4, 3])

    if I_PROBLEM==0:
        # Sod shock tube
        # https://en.wikipedia.org/wiki/Sod_shock_tube
        mesh = np.linspace(-1, 1, N_POINTS).tolist()
        DX   = mesh[1] - mesh[0]
        mesh = np.array([mesh[0]-2*DX, mesh[0]-DX] + mesh + [mesh[-1]+DX, mesh[-1]+2*DX])
        
        for i in range(mesh.shape[0]):
            if mesh[i] <=0 :
                sol[i,0] = 1.0
                sol[i,1] = 0   
                sol[i,2] = 1.0/(GAMMA-1)
            else:
                sol[i,0] = 0.125
                sol[i,1] = 0   
                sol[i,2] = 0.1/(GAMMA-1)
    
    else:
        # Shu-Osher Shock Tube Problem
        # http://www.ttctech.com/Samples/shockwave/shockwave.htm
        mesh = np.linspace(0, 10, N_POINTS).tolist()
        DX   = mesh[1] - mesh[0]
        mesh = np.array([mesh[0]-2*DX, mesh[0]-DX] + mesh + [mesh[-1]+DX, mesh[-1]+2*DX])
        
        for i in range(mesh.shape[0]):
            if mesh[i] <=1 :
                sol[i,0] = 3.857
                sol[i,1] = 2.629*sol[i,0]
                sol[i,2] = 10.333/(GAMMA-1)+0.5*sol[i,0]*2.629**2
            else:
                sol[i,0] = 1.0+0.2*np.sin(5*(mesh[i]-5))
                sol[i,1] = 0.0
                sol[i,2] = 1.0/(GAMMA-1)

    return mesh, sol, DX

def time_march_rhs(sol: np.ndarray, dx: float, dt: float) -> np.ndarray:
    '''
    Calculate the right hand side of the dU/dt=Q
    '''
    qq = np.zeros_like(sol)
    
    for i in range(2, N_POINTS-1):
        
        
        if I_RECON==1:
            uUL, uUR = Reconstruction.Upwind1_TVD(
                sol[i-2,:], sol[i-1,:], sol[i,:], sol[i+1,:], 
                limiter=Reconstruction.min_mod)
        elif I_RECON==2:
            uUL, uUR = Reconstruction.Upwind1_TVD_eigen(
                sol[i-2,:], sol[i-1,:], sol[i,:], sol[i+1,:], 
                limiter=Reconstruction.min_mod, roe_average=Roe.average,
                dx=dx, dt=dt)
        else:
            uUL, uUR = Reconstruction.Upwind0(sol[i-1,:], sol[i,:])
        
        if I_FLUX==1:
            fFaceL = AUSM.flux_face(uUL, uUR)
        elif I_FLUX==2:
            fFaceL = Roe.flux_face(uUL, uUR)
        else:
            fFaceL = Exact.flux_face(uUL, uUR)
        
        
        if I_RECON==1:
            uUL, uUR = Reconstruction.Upwind1_TVD(
                sol[i-1,:], sol[i,:], sol[i+1,:], sol[i+2,:], 
                limiter=Reconstruction.min_mod)
        elif I_RECON==2:
            uUL, uUR = Reconstruction.Upwind1_TVD_eigen(
                sol[i-1,:], sol[i,:], sol[i+1,:], sol[i+2,:], 
                limiter=Reconstruction.min_mod, roe_average=Roe.average,
                dx=dx, dt=dt)
        else:
            uUL, uUR = Reconstruction.Upwind0(sol[i,:], sol[i+1,:])
        
        if I_FLUX==1:
            fFaceR = AUSM.flux_face(uUL, uUR)
        elif I_FLUX==2:
            fFaceR = Roe.flux_face(uUL, uUR)
        else:
            fFaceR = Exact.flux_face(uUL, uUR)


        qq[i,:] = - (fFaceR - fFaceL)/dx
        
    return qq

def RungeKutta3(sol: np.ndarray, dx: float, time_remain: float) -> np.ndarray:
    
    global_dt = time_step(sol, dx, CFL)
    
    global_dt = min(global_dt, time_remain)

    next_sol = sol.copy()
    
    #* Step 1
    qq = time_march_rhs(next_sol, dx, global_dt)
    next_sol = sol + global_dt*qq
    
    #* Step 2
    qq = time_march_rhs(next_sol, dx, global_dt)
    next_sol = 3/4*sol + 1/4*(next_sol + global_dt*qq)
    
    #* Step 3
    qq = time_march_rhs(next_sol, dx, global_dt)
    next_sol = 1/3*sol + 2/3*(next_sol + global_dt*qq)
    
    return next_sol, global_dt


if __name__ == "__main__":
    
    mesh, initial_solution, DX = initialization()

    plt.figure()

    #* Exact solution
    I_FLUX=0; I_RECON=1; CFL=0.1
    current_solution=initial_solution; t0=0; n_iteration=0
    while t0<T0:
        current_solution, global_dt = RungeKutta3(current_solution, DX, T0-t0)
        t0 += global_dt; n_iteration += 1
    print('Exact solution: time = %.2f, n = %d'%(t0, n_iteration))
    plt.plot(mesh[2:N_POINTS-1], pressure(current_solution[2:N_POINTS-1, :]), 'k') 
    
    #* AUSM flux
    I_FLUX=1; I_RECON=1; CFL=0.6
    current_solution=initial_solution; t0=0; n_iteration=0
    while t0<T0:
        current_solution, global_dt = RungeKutta3(current_solution, DX, T0-t0)
        t0 += global_dt; n_iteration += 1
    print('AUSM flux:      time = %.2f, n = %d'%(t0, n_iteration))
    plt.plot(mesh[2:N_POINTS-1], pressure(current_solution[2:N_POINTS-1, :]), 'b') 
    
    #* Roe flux
    I_FLUX=2; I_RECON=1; CFL=1.2
    current_solution=initial_solution; t0=0; n_iteration=0
    while t0<T0:
        current_solution, global_dt = RungeKutta3(current_solution, DX, T0-t0)
        t0 += global_dt; n_iteration += 1
    print('Roe  flux:      time = %.2f, n = %d'%(t0, n_iteration))
    plt.plot(mesh[2:N_POINTS-1], pressure(current_solution[2:N_POINTS-1, :]), 'r--') 

    plt.title('pressure')
    plt.legend(['exact', 'AUSM', 'Roe'])
    plt.savefig('shock-tube-%d.jpg'%(I_PROBLEM), dpi=300)



