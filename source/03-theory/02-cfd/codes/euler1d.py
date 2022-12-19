
from typing import List, Tuple

import exactRP as RP
import numpy as np

GAMMA = 1.4
EPSILON = 1e-6

class Exact():
    '''
    This function uses the exact Riemann solver `ToroExact` from
    https://github.com/tahandy/ToroExact to calculate the face flux.
    '''

    def __init__(self) -> None:
        pass

    @staticmethod
    def flux_face(UL: np.ndarray, UR: np.ndarray) -> np.ndarray:

        rhoL = UL[0]; uL = UL[1]/rhoL; pL=(GAMMA-1)*(UL[2]-0.5*rhoL*uL**2)
        rhoR = UR[0]; uR = UR[1]/rhoR; pR=(GAMMA-1)*(UR[2]-0.5*rhoR*uR**2)

        state_l = [rhoL, uL, pL]
        state_r = [rhoR, uR, pR]
        rp = RP.exactRP(GAMMA, state_l, state_r)
        success = rp.solve()
        
        if not success:
            raise Exception(f"Exact Riemann solver fails at interface!")
        
        rho, p, u, _, _ = rp.sample([0])
        rho, p, u = rho[0], p[0], u[0]
        rhoE = 0.5*rho*u**2 + p/(GAMMA-1)
        
        fFace = np.zeros(3)
        fFace[0] = rho*u
        fFace[1] = rho*u**2 + p
        fFace[2] = (rhoE+p) * u

        return fFace


class AUSM():
    '''
    AUSM flux vector splitting scheme
    '''
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def flux_face(UL: np.ndarray, UR: np.ndarray) -> np.ndarray:

        rhoL = UL[0]; uL = UL[1]/rhoL; pL=(GAMMA-1)*(UL[2]-0.5*rhoL*uL**2)
        rhoR = UR[0]; uR = UR[1]/rhoR; pR=(GAMMA-1)*(UR[2]-0.5*rhoR*uR**2)
        tHL  = (UL[2]+pL)/rhoL; aL = np.sqrt(GAMMA*pL/rhoL); mL = uL/aL
        tHR  = (UR[2]+pR)/rhoR; aR = np.sqrt(GAMMA*pR/rhoR); mR = uR/aR

        # The positive M is calculated from the left M
        if mL <= -1:
            Mp = 0.0 
            Pp = 0.0
        elif mL < 1:
            Mp = (mL + 1) * (mL + 1) / 4.0
            Pp = (mL + 1) * (mL + 1) / 4.0 * (2.0 - mL) * pL
        else:
            Mp = mL
            Pp = pL

        # The negative M is calculated from the right M
        if mR <= -1:
            Mn = mR
            Pn = pR
        elif mR < 1:
            Mn = -(mR - 1) * (mR - 1) / 4.0
            Pn = pR * (1 - mR) * (1 - mR) * (2 + mR) / 4.0
        else:
            Mn = 0.0
            Pn = 0.0

        # Decide the flux based on the sign of Mn + Mp
        selectL = (np.sign(Mn + Mp) + 1) / 2.0 * (Mn + Mp)
        selectR = (1 - np.sign(Mn + Mp)) / 2.0 * (Mn + Mp)
        
        fFace = np.zeros(3)
        fFace[0] = selectL * rhoL * aL + selectR * rhoR * aR
        fFace[1] = selectL * rhoL * aL * uL  + selectR * rhoR * aR * uR + Pn + Pp
        fFace[2] = selectL * rhoL * aL * tHL + selectR * rhoR * aR * tHR
        
        return fFace


class Roe():

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def average(rhoL, rhoR, uL, uR, tHL, tHR):
        '''
        Calculate ROE average rho, u, H, a
        '''
        ratio = np.sqrt(rhoR/rhoL)
        roe_rho = np.sqrt(rhoL*rhoR)
        roe_u = (uL  + ratio*uR )/(1+ratio)
        roe_H = (tHL + ratio*tHR)/(1+ratio)
        roe_a = np.sqrt((GAMMA-1)*(roe_H-0.5*roe_u**2))
        return roe_rho, roe_u, roe_H, roe_a

    @staticmethod
    def eigenvalue(u: float, a: float) -> np.ndarray:
        '''
        Calculate ROE eigenvalue[3] (with entropy fix)
        '''
        eps = 0.3*(a+abs(u))
        eig = np.abs(np.array([u-a, u, u+a]))
        for i in range(3):
            if eig[i]<eps:
                eig[i] = 0.5*(eig[i]**2/eps+eps)
        return eig

    @staticmethod
    def eigenvector(u: float, a: float, tH: float) -> List[np.ndarray]:
        '''
        Calculate the eigenvectors v[3][3]
        '''
        vec = [None, None, None]
        vec[0] = np.array([1.0, u-a, tH-u*a  ])
        vec[1] = np.array([1.0, u,   0.5*u**2])
        vec[2] = np.array([1.0, u+a, tH+u*a  ])
        return vec
    
    @staticmethod
    def jump_weight(rhoL, rhoR, uL, uR, pL, pR, roe_rho, roe_a) -> np.ndarray:
        '''
        Calculate the weight (alpha[3]) of eigenvectors for 
        the jump on the face between the Left and Right values.
        '''
        dr = rhoR - rhoL
        dp = pR - pL
        du = uR - uL
        
        alpha = np.zeros(3)
        alpha[0] = 0.5*(dp-roe_a*roe_rho*du)/roe_a**2
        alpha[1] = dr - dp/roe_a**2
        alpha[2] = 0.5*(dp+roe_a*roe_rho*du)/roe_a**2
        
        return alpha

    @staticmethod
    def flux_face(UL: np.ndarray, UR: np.ndarray) -> np.ndarray:
        '''
        Calculate ROE scheme flux on the face between Left and Right values.
        '''
        rhoL = UL[0]; uL = UL[1]/rhoL; pL=(GAMMA-1)*(UL[2]-0.5*rhoL*uL**2)
        rhoR = UR[0]; uR = UR[1]/rhoR; pR=(GAMMA-1)*(UR[2]-0.5*rhoR*uR**2)
        tHL  = (UL[2] + pL)/rhoL
        tHR  = (UR[2] + pR)/rhoR
        
        fL = np.array([UL[1], UL[1]*uL+pL, uL*(UL[2]+pL)])
        fR = np.array([UR[1], UR[1]*uR+pR, uR*(UR[2]+pR)])
        
        roe_rho, roe_u, roe_H, roe_a \
            = Roe.average(rhoL, rhoR, uL, uR, tHL, tHR)
        
        eigenvalue  = Roe.eigenvalue (roe_u, roe_a)
        eigenvector = Roe.eigenvector(roe_u, roe_a, roe_H)
        alpha       = Roe.jump_weight(rhoL, rhoR, uL, uR, pL, pR, roe_rho, roe_a)

        fUpwind = np.zeros(3)
        for i in range(3):
            fUpwind += alpha[i]*eigenvalue[i]*eigenvector[i]
        
        fFace = 0.5*(fL+fR) - 0.5*fUpwind
        
        return fFace


class Reconstruction():
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def min_mod(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        m = np.zeros_like(a)
        for i in range(a.shape[0]):
            if a[i]*b[i]>0:
                m[i] = np.sign(a[i])*min(abs(a[i]), abs(b[i]))
        return m
    
    @staticmethod
    def van_leer(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        m = a*b*(np.sign(a)+np.sign(b))
        m = m/(abs(a)+abs(b)+EPSILON)
        return m
    
    @staticmethod
    def van_albada(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        m = np.maximum(a*b, np.zeros_like(a))
        m = m*(a+b)/(a**2+b**2+EPSILON)
        return m
    
    @staticmethod
    def Upwind0(Uj: np.ndarray, Ujp1: np.ndarray):
        '''
        For L&R of face j+1/2
        '''
        uUL = Uj.copy()
        uUR = Ujp1.copy()
        return uUL, uUR
    
    @staticmethod
    def Upwind1_TVD(Ujm1: np.ndarray, Uj: np.ndarray, 
                    Ujp1: np.ndarray, Ujp2: np.ndarray,
                    limiter) -> Tuple[np.ndarray, np.ndarray]:
        '''
        For L&R of face j+1/2:
        
        limiter = min_mod, van_leer, van_albada
        '''
        uUL = Uj   + 0.5*limiter(Ujp1-Uj,   Uj-Ujm1)
        uUR = Ujp1 - 0.5*limiter(Ujp2-Ujp1, Ujp1-Uj)
        return uUL, uUR
    
    @staticmethod
    def Upwind1_TVD_eigen(Ujm1: np.ndarray, Uj: np.ndarray, Ujp1: np.ndarray, 
            Ujp2: np.ndarray, limiter, roe_average, dx, dt) \
            -> Tuple[np.ndarray, np.ndarray]:
        '''
        For L&R of face j+1/2:
        
        limiter = min_mod, van_leer, van_albada
        '''
        rhoL = Uj  [0]; uL = Uj  [1]/rhoL; pL=(GAMMA-1)*(Uj  [2]-0.5*rhoL*uL**2)
        rhoR = Ujp1[0]; uR = Ujp1[1]/rhoR; pR=(GAMMA-1)*(Ujp1[2]-0.5*rhoR*uR**2)
        tHL  = (Uj  [2] + pL)/rhoL
        tHR  = (Ujp1[2] + pR)/rhoR
        
        roe_rho, roe_u, roe_H, roe_a \
            = roe_average(rhoL, rhoR, uL, uR, tHL, tHR)

        mL = np.zeros([3,3])
        mR = np.zeros([3,3])

        g1 = GAMMA-1
        u2 = roe_u**2
        a2 = roe_a**2
        ua = roe_u*roe_a
        
        mR[0, :] = np.array([1,           1,      1          ])
        mR[1, :] = np.array([roe_u-roe_a, roe_u,  roe_u+roe_a])
        mR[2, :] = np.array([roe_H-ua,    0.5*u2, roe_H+ua   ])
        
        mL[0, :] = np.array([0.5*g1*u2+ua, -g1*roe_u-roe_a,  g1]) / (2*a2)
        mL[1, :] = np.array([a2-0.5*g1*u2,  g1*roe_u,       -g1]) / a2
        mL[2, :] = np.array([0.5*g1*u2-ua, -g1*roe_u+roe_a,  g1]) / (2*a2)
        
        aa = np.dot(mL, Uj  -Ujm1)
        bb = np.dot(mL, Ujp1-Uj  )
        cc = np.dot(mL, Ujp2-Ujp1)
        
        dL = limiter(bb, aa)/dx
        dR = limiter(cc, bb)/dx
        
        eig= np.array([roe_u-roe_a, roe_u, roe_u+roe_a])

        wL = np.dot(mL, Uj  ) + 0.5*dL*(dx-dt*eig)
        wR = np.dot(mL, Ujp1) - 0.5*dR*(dx+dt*eig)

        uUL = np.dot(mR, wL)
        uUR = np.dot(mR, wR)

        return uUL, uUR


def pressure(U: np.ndarray) -> np.ndarray:
    return (GAMMA-1)*(U[:,2]-0.5*U[:,1]**2/U[:,0])

def time_step(U: np.ndarray, dx: float, cfl: float) -> float:
    '''
    U[nCell, 3]: conservative variables of all cells 
    '''
    u  = U[:,1]/U[:,0]
    p  = (GAMMA-1)*(U[:,2]-0.5*U[:,0]*u**2)
    a  = np.sqrt(GAMMA*p/U[:,0])
    m  = np.max(np.vstack([abs(u+a), abs(u-a), abs(u)]))
    dt = cfl*dx/m
    return dt

