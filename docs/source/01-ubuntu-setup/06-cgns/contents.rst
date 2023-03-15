CGNS
====================

The `CFD General Notation System (CGNS) <https://cgns.github.io/>`_ 
provides a general, portable, and extensible standard for the 
storage and retrieval of computational fluid dynamics (CFD) analysis data. 

`Third Party Packages | ADflow
<https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/installInstructions/install3rdPartyPackages.html>`_


安装 HDF5
--------------------

.. code-block:: bash

    sudo apt-get install libhdf5-dev


安装过程
--------------------

.. code-block:: bash

    # unzip in the package directory, e.g., $HOME/opt/
    cd ~/opt/
    wget https://github.com/CGNS/CGNS/archive/refs/tags/v4.3.0.tar.gz
    tar -xvaf v4.3.0.tar.gz

    # 安装路径为当前路径
    cd CGNS-4.3.0
    mkdir -p build
    cd build
    cmake .. -DCGNS_ENABLE_FORTRAN=1 \
    -DCMAKE_INSTALL_PREFIX=$HOME/opt/CGNS-4.3.0/opt-gfortran -DCGNS_BUILD_CGNSTOOLS=0

    make
    make install

    # Add environment variables
    echo '# CGNS-4.3.0' >> $HOME/.bashrc
    echo 'export CGNS_HOME=$HOME/opt/CGNS-4.3.0/opt-gfortran' >> $HOME/.bashrc
    echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $HOME/.bashrc
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $HOME/.bashrc
    echo ' ' >> $HOME/.bashrc
    source ~/.bashrc

Python CGNS 接口：

`A python package for CGNS <https://pycgns.sourceforge.net/>`_


安装 CGNS 工具 (Optional)
------------------------------

CGNS 提供了一系列在本地（非集群）查看、编辑 CGNS 文件的工具，需要先安装以下包，再配置 CGNS。

.. code-block:: bash

    sudo apt-get install libxmu-dev libxi-dev

    sudo apt-get install freeglut3
    sudo apt-get install tk8.6-dev
    sudo apt-get install freeglut3-dev

CGNS library sometimes complains about missing includes and libraries. 
Most of the time this is either Tk/TCL or OpenGL. This can be solved by 
installing freeglut3, tk8.6-dev (,freeglut3-dev, if needed). 
Note that the version of these libraries might be different on your machine.

.. code-block:: bash

    cd CGNS-4.3.0
    cd build
    cmake .. -DCGNS_ENABLE_FORTRAN=1 \
    -DCMAKE_INSTALL_PREFIX=$HOME/opt/CGNS-4.3.0/opt-gfortran -DCGNS_BUILD_CGNSTOOLS=1

    make
    make install

If you compiled with ``-D CGNS_BUILD_CGNSTOOLS=1``, you either need to add the
binary path to your PATH environmental variable or you can install the binaries 
system wide. By specifying the installation prefix as shown in the example 
configure commands above, the binary path is in your PATH environmental variables;
without specifying the prefix, the default is a system path, which requires sudo.

