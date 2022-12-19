简介
====================

The `CFD General Notation System (CGNS) <https://cgns.github.io/>`_ 
provides a general, portable, and extensible standard for the 
storage and retrieval of computational fluid dynamics (CFD) analysis data. 

.. seealso::

    `A User's Guide to CGNS <https://cgns.github.io/CGNS_docs_current/user/index.html>`_


(1) 数据类型
--------------------------------------

The CGNS standard includes the following types of data. 

- Structured, unstructured, and hybrid grids
- Flow solution data, which may be nodal, cell-centered, face-centered, or edge-centered
- Multi-zone interface connectivity, both abutting and overset
- Boundary conditions
- Flow equation descriptions, including the equation of state, viscosity 
  and thermal conductivity models, turbulence models, multi-species chemistry models, 
  and electromagnetics
- Time-dependent flow, including moving and deforming grids
- Dimensional units and non-dimensionalization information
- Reference states
- Convergence history
- Association to CAD geometry definitions
- User-defined data 

Disciplines other than fluid dynamics would need to augment the data definitions and 
storage conventions, but the fundamental database software, which provides platform 
independence, is not specific to fluid dynamics.


(2) 数据存储格式: HDF5
--------------------------------------

The data are stored in a compact, binary format and are accessible through 
a complete and extensible library of functions.  

HDF5 (`Hierarchical Data Format <https://www.hdfgroup.org/solutions/hdf5/>`_)
由美国 UIUC (University of Illinois at Urbana-Champaign) 开发，是一种常见的跨平台数据储存文件，
可以存储不同类型的数据并在不同类型的机器上传输，同时还有统一处理这种格式的函数库。

HDF5 文件一般以 .h5 或者 .hdf5 作为后缀名, 需要专门的软件才能打开预览文件的内容。
HDF5 文件结构中有两个主要对象: Groups 和 Datasets。
Groups 类似于文件夹, Datasets 类似于数组。

python 库 `h5py <https://github.com/h5py/h5py>`_ 可以用于读写 HDF5 文件。


(3) 数据结构
--------------------------------------

CGNS 文件内部以树状结构 (tree structure) 存储数据，每个节点 (node) 由 {Name, Label, Data} 组成。
具体的计算流体力学数据存储规则见 `Standard Interface Data Structures (SIDS)
<https://cgns.github.io/CGNS_docs_current/sids/index.html>`_。



(4) pyCGNS
--------------------------------------

.. seealso::

    `A Python package for CGNS <https://pycgns.sourceforge.net/index.html>`_


(4.a) pyCGNS.MAP
++++++++++++++++++++++++++++++++++++++

`MAP <https://pycgns.sourceforge.net/MAP/_index.html>`_ 模块用于 `CGNS/HDF5` 与 
`CGNS/Python Tree` 之间的格式转换和读写。

.. code-block:: python

    import CGNS

    (tree, links, paths) = CGNS.MAP.load("mesh.cgns")

    CGNS.MAP.save("solution.hdf", tree)

读入 CGNS 的 HDF5 格式文件时，除了 CGNS/Python Tree (`tree`), 
还定义一了个特殊的链接结构 (`links`) 用于正确组织 CGNS 文件 (`paths`)。

The `links` is the correct mapping of the management of files on the disk,
it is used to set and get CGNS symbolic links information. 
This information is relevant only during read/write operations on disks.


(4.b) CGNS/Python Tree
++++++++++++++++++++++++++++++++++++++

`CGNS/Python Tree <https://pycgns.sourceforge.net/MAP/sids-to-python.html>`_ 
定义了一种基于 `Python` 语言的 CGNS 树状结构。

每个节点 (node) 由 {Name, Value, Children, Type} 组成, 其数据类型依次为:
`string`, `numpy array`, `list of CGNS/Python nodes`, `string` 。
实际上, CGNS/Python tree 就是一个 node。
所有的数据，即使是单个值也需要保存为 `numpy array`, 空白值可以使用 `None`。

**CGNS/Python node** :

.. code-block:: python

    node = [ <name:string>, <value:numpy.array>, [ <child:node>* ], <cgns-type:string> ]

    RefValues = [
            ['Mach',numpy.array([0.2]),[],'DataArray_t']
            ['Reynolds',numpy.array([23300000.0]),[],'DataArray_t']
            ['LengthReference',numpy.array([0.5]),[],'DataArray_t']
            ['Density',numpy.array([1.22524863848]),[],'DataArray_t'] ]

    RefState = ['ReferenceState', None, RefValues, 'ReferenceState_t']

**root** :

原始 CGNS 中 `root` 节点的形式与标准的 `node` 不同，但是在 CGNS/Python mapping 中，
尽量保持形式一致：

.. code-block:: python

    root = ['root', None, [ <CGNSLibraryVersion:node>, <CGNSBase:node>* ], 'CGNSTree_t' ]

**base** :

.. code-block:: python

    BaseDims = np.array([3, 3], dtype=np.int32, order='Fortran')

    base = ['Base', BaseDims, [ <CGNSZone:node>* ], 'CGNSBase_t' ]

    CellDimension       = BaseDims[0]
    PhysicalDimension   = BaseDims[1]

**zone** :

A 3D structured zone with (ni,nj,nk):

.. code-block:: python
    :linenos:

    ZoneDims = np.array([ni,ni-1,0], [nj,nj-1,0], [nk,nk-1,0], dtype=np.int32, order='Fortran')
    ZoneNode = ['Zone001', ZoneDims, ZoneChildrenList, 'Zone_t']

    ZoneVertexSize          = ZoneDims[:,0]
    ZoneCellSize            = ZoneDims[:,1]
    ZoneVertexBoundarySize  = ZoneDims[:,2]

**grid coordinates** :

.. code-block:: python

    GridChildrenList = [NodeCoordinateX, NodeCoordinateY, NodeCoordinateZ]
    
    GridNode = ['Grid#001', None, GridChildrenList, 'GridCoordinates_t']

.. tip::

    CGNS node 的数据类型参见 `CGNS Types <https://pycgns.sourceforge.net/PAT/_index.html#cgns-types>`_

    在 CGNS/Python 中定义了 `CGNS Keywords` 相应的 python 变量, 
    大部分为对应 keyword 尾部增加 `_s` 或 `s`, 如 `DataType -> DataType_s`, `DataType_t -> DataType_ts`。


(4.c) pyCGNS.PAT
++++++++++++++++++++++++++++++++++++++

`PAT <https://pycgns.sourceforge.net/PAT/_index.html>`_ (PATtern) 
模块提供了处理 `CGNS/Python Tree` 的函数。

`PAT.cgnslib <https://pycgns.sourceforge.net/PAT/_index.html#pat-cgnslib>`_ 
依照 `SIDS` 格式建立、读取、检查、修改 `CGNS/Python sub-trees`。

- newCGNSTree()
- newCGNSBase()
- newZone()
- newBoundary()

`PAT.cgnsutils <https://pycgns.sourceforge.net/PAT/_index.html#utilities>`_
包含大量工具函数处理 `CGNS/Python sub-trees`。

- nodeCreate()
- nodeCopy()
- nodeDelete()
- checkNode()
- getNodeByPath()
- getValueShape()
- copyArray()

`PAT.cgnskeywords <https://pycgns.sourceforge.net/PAT/_index.html#pat-cgnskeywords>`_
包含 `SIDS` 常数名称和字符串。

`PAT.cgnstypes <https://pycgns.sourceforge.net/PAT/_index.html#pat-cgnstypes>`_
包含 `SIDS` 数据类型描述 (types descriptions, enumerates, allowed list of children...)。

`PAT.cgnserrors <https://pycgns.sourceforge.net/PAT/_index.html#pat-cgnserrors>`_
包含 `SIDS` 错误代码和报错信息。

.. code-block:: python

    import CGNS.PAT.cgnslib as CL
    import CGNS.PAT.cgnskeywords as CK
    import CGNS.PAT.cgnsutils as CU

(4.c) Other modules
++++++++++++++++++++++++++++++++++++++

pyCGNS.NAV: CGNS tree browser

pyCGNS.VAL: CGNS/Python tree checker

pyCGNS.DAT: tools for database management

pyCGNS.APP: tools, examples, utilities, tests


(5) 注意事项
--------------------------------------

Whenever a new entity is created using the API, an integer index is returned. 
This index is used in subsequent API calls to refer to the entity.

The grid coordinate arrays can be written in single or double precision. 
The desired data type is communicated to the API using the keywords RealSingle or RealDouble. 
The user must insure that the data type transmitted to the API is consistent with the the one 
used in declaring the coordinates arrays. 

The CGNS file grid.cgns is a binary file that, internally, possesses the tree-like structure shown below. 
Each node has a name, a label, and may or may not contain data. In the example in the figure, 
all the nodes contain data except for the GridCoordinates node, for which MT indicates no data.



