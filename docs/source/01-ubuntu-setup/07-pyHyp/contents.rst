pyHyp
===========================

pyHyp is a hyperbolic mesh generator that automatically generates two or three dimensional meshes 
around simple geometric configurations. The basic idea is to start with an initial surface (or curve) 
corresponding to the geometry of interest and then grow or extrude the mesh in successive layers until 
it reaches a sufficient distance from the original surface. 
In the process, the entire space surrounding the geometry is meshed.

.. seealso:: 

    `Hyperbolic mesh generator: pyHyp <https://mdolab-pyhyp.readthedocs-hosted.com/en/latest/index.html>`_


pyHyp 依赖于 `PETSc`, `CGNS Libarary`, `cgnsutilities`, `pyspline`, `pygeo`。


cgnsutilities
----------------------

说明文档参见 `CGNS Utilities <https://mdolab-cgnsutilities.readthedocs-hosted.com/en/latest/>`_。
从 MDOLab `cgnsutilities <https://github.com/mdolab/cgnsutilities>`_ Github 官网下载 release 版本。

使用 `cgnsutilities` 路径下的 `config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk` 作为配置文件，
将其复制并重命名到 `config/config.mk` 位置。

Open and edit the config file. 
You many have to adjust the CGNS_INCLUDE_FLAGS and CGNS_LINKER_FLAGS to match your installation of the CGNS library. 
You may also specify the C compiler with the CC variable and the flags for the C compiler with CFLAGS. 
The C-compiler is only used for the compiler f2py wrapper. 
The Fortran compiler may be specified with the FC variable and the corresponding flags with the FFLAGS variable. 
It has been tested with both Intel and GNU Fortran compilers.

.. code-block:: bash

    cd ~/opt/
    wget https://github.com/mdolab/cgnsutilities/archive/refs/tags/v2.7.1.tar.gz
    tar -xvaf v2.7.1.tar.gz

    cd cgnsutilities-2.7.1/
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk

    # Modify config.mk
    vim config.mk

    make

    pip install .


pyspline
----------------------

说明文档参见 `pyspline <https://mdolab-pyspline.readthedocs-hosted.com/en/latest/>`_。
从 MDOLab `Github pyspline 官网 <https://github.com/mdolab/pyspline>`_ 下载 release 版本。

.. code-block:: bash

    cd ~/opt/
    wget https://github.com/mdolab/pyspline/archive/refs/tags/v1.5.2.tar.gz
    tar -xvaf v1.5.2.tar.gz

    cd pyspline-1.5.2/
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk

    make
    
    pip install .


pygeo
----------------------

说明文档参见 `pygeo <https://mdolab-pygeo.readthedocs-hosted.com/en/latest/>`_。
从 MDOLab `Github pygeo 官网 <https://github.com/mdolab/pygeo>`_ 下载 release 版本。

Installation requires a working copy of the pyspline package, which requires a Fortran compiler.
Because of this dependency, pyGeo is only supported on Linux.

.. code-block:: bash

    cd ~/opt/
    wget https://github.com/mdolab/pygeo/archive/refs/tags/v1.12.3.tar.gz
    tar -xvaf v1.12.3.tar.gz

    cd pygeo-1.12.3/
    pip install .

测试安装结果

.. code-block:: bash

    pip install .[testing]

    testflo -v


pyHyp 安装
----------------------

说明文档参见 `pyHyp <https://mdolab-pyhyp.readthedocs-hosted.com/en/latest/index.html>`_。
从 MDOLab `Github pyHyp 官网 <https://github.com/mdolab/pyhyp>`_ 下载 release 版本。

.. code-block:: bash

    cd ~/opt/
    wget https://github.com/mdolab/pyhyp/archive/refs/tags/v2.6.1.tar.gz
    tar -xvaf v2.6.1.tar.gz

    cd pyhyp-2.6.1
    cp config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk

    make

    pip install .

测试安装结果

.. code-block:: bash

    pip install .[testing]

    chmod 777 ./tests/ref/get-ref-files.sh
    ./tests/ref/get-ref-files.sh

    testflo -v

