CGNS
====================

The `CFD General Notation System (CGNS) <https://cgns.github.io/>`_ 
provides a general, portable, and extensible standard for the 
storage and retrieval of computational fluid dynamics (CFD) analysis data. 

`Third Party Packages | ADflow
<https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/installInstructions/install3rdPartyPackages.html>`_


安装过程
--------------------

.. code-block:: bash
   :linenos:
   
   # unzip in the package direcotry, e.g., $HOME/opt/
   cd ~/opt/
   wget https://github.com/CGNS/CGNS/archive/v4.1.2.tar.gz
   tar -xvaf v4.1.2.tar.gz

   # 安装路径为当前路径
   cd CGNS-4.1.2
   mkdir -p build
   cd build
   cmake .. -DCGNS_ENABLE_FORTRAN=1 \
   -DCMAKE_INSTALL_PREFIX=$HOME/opt/CGNS-4.1.2/opt-gfortran -DCGNS_BUILD_CGNSTOOLS=0

   make
   make install

   # Add environment variables
   echo '# CGNS-4.1.2' >> $HOME/.bashrc
   echo 'export CGNS_HOME=$HOME/opt/CGNS-4.1.2/opt-gfortran' >> $HOME/.bashrc
   echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $HOME/.bashrc
   echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $HOME/.bashrc
   echo ' ' >> $HOME/.bashrc
   source ~/.bashrc

Python CGNS 接口：

`A python package for CGNS <https://pycgns.sourceforge.net/>`_


安装 CGNS 工具 (Optional)
------------------------------

The CGNS Library comes with a set of tools to view and edit CGNS files manually. 
To install these tools, use the flag ``-D CGNS_BUILD_CGNSTOOLS=ON`` during 
the configure step. Note that these tools should be installed on a local computer 
and not on a cluster.

To enable this option you may need to install the following packages:

.. code-block:: bash

   sudo apt-get install libxmu-dev libxi-dev

CGNS library sometimes complains about missing includes and libraries. 
Most of the time this is either Tk/TCL or OpenGL. This can be solved by 
installing the following packages. Note that the version of these libraries 
might be different on your machine:

.. code-block:: bash

   sudo apt-get install freeglut3
   sudo apt-get install tk8.6-dev

If needed, install the following package as well:

.. code-block:: bash

   sudo apt-get install freeglut3-dev

If you compiled with ``-D CGNS_BUILD_CGNSTOOLS=ON``, you either need to add the
binary path to your PATH environmental variable or you can install the binaries 
system wide. By specifying the installation prefix as shown in the example 
configure commands above, the binary path is in your PATH environmental variables;
without specifying the prefix, the default is a system path, which requires sudo.


