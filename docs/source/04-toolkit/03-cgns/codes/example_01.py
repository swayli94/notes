'''
Single-Zone Structured Grid

https://cgns.github.io/CGNS_docs_current/user/started.html#sec:singlegrid
'''

import CGNS.MAP as MAP
import CGNS.PAT.cgnslib as CL
import CGNS.PAT.cgnskeywords as CK
import numpy as np


if __name__ == "__main__":
    
    NI = 21
    NJ = 19
    NK = 9
    
    #* Grid points
    x = np.zeros([NI,NJ,NK])
    y = np.zeros([NI,NJ,NK])
    z = np.zeros([NI,NJ,NK])
    
    for k in range(NK):
        for j in range(NJ):
            for i in range(NI):
                x[i,j,k] = float(i)
                y[i,j,k] = float(j)
                z[i,j,k] = float(k)

    #* Flow solution
    density  = np.zeros([NI-1,NJ-1,NK-1])
    pressure = np.zeros([NI-1,NJ-1,NK-1])
    
    for k in range(NK-1):
        for j in range(NJ-1):
            for i in range(NI-1):
                density [i,j,k] = float(i)
                pressure[i,j,k] = float(i+j+k)


    #* ======================================================
    #* Create a new tree (i.e., root, CGNSTree_t node)
    Tree = CL.newCGNSTree()
    
    #* Add `Base` (CGNSBase_t node) to `Tree`
    nCellDim = 3
    nPhysDim = 3
    Base = CL.newBase(Tree, 'Base', nCellDim, nPhysDim)

    #* Add `Zone` (Zone_t node) to `Base`
    ZoneDims = np.array([[NI,NI-1,0],[NJ,NJ-1,0],[NK,NK-1,0]], 
                        dtype=np.int32, order='F')
    
    ZoneVertexSize          = ZoneDims[:,0]
    ZoneCellSize            = ZoneDims[:,1]
    ZoneVertexBoundarySize  = ZoneDims[:,2]
    
    Zone = CL.newZone(Base, 'Zone_1', zsize=ZoneDims, 
                      ztype=CK.Structured_s, family='Example')

    #* Add `Grid` (GridCoordinates_t node) to `Zone`
    Grid = CL.newGridCoordinates(Zone, CK.GridCoordinates_s)

    # Add coordinates (DataArray_t node) to `Grid`
    cx = CL.newDataArray(Grid, CK.CoordinateX_s, x)
    cy = CL.newDataArray(Grid, CK.CoordinateY_s, y)
    cz = CL.newDataArray(Grid, CK.CoordinateZ_s, z)
    
    if False:
        
        #* Add flow solution (FlowSolution_t node) to `Zone`
        Sol = CL.newFlowSolution(Zone, 'FlowSolution', CK.CellCenter_s)
        
        # Add data (DataArray_t node) to `Sol`
        sd = CL.newDataArray(Sol, CK.Density_s,  density)
        sp = CL.newDataArray(Sol, CK.Pressure_s, pressure)
    
    #* Output CGNS file
    filename = '../figures/example-01-structured.cgns'

    status = MAP.save(filename, Tree)
