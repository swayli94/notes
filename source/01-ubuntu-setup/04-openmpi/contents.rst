OpenMPI
====================

参考网站
--------------------

`FAQ: Building Open MPI (open-mpi.org) 
<https://www.open-mpi.org/faq/?category=building#build-compilers>`_

`Compile from source (Ubuntu) | DAFoam
<https://dafoam.github.io/mydoc_installation_source.html#prerequisites>`_

`Third Party Packages | ADflow
<https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/installInstructions/install3rdPartyPackages.html>`_


安装过程
--------------------

.. code-block:: bash
   :linenos:
   
   wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.4.tar.gz
   tar -xvf openmpi-4.1.4.tar.gz

   cd openmpi-4.1.4

   # ./configure 
   # 默认安装目录: /usr/local/lib/openmpi
   # 自定义目录:  ./configure --prefix=$HOME/opt/openmpi
   # 指定编译器 ./configure CC=gcc CXX=g++ F77=gfortran FC=gfortran

   ./configure --prefix=$HOME/opt/openmpi
   make all install


添加环境变量
--------------------

To use MPI you will have to adapt your ``PATH`` and ``LD_LIBRARY_PATH`` 
environment variable. This appends the two lines to `.bashrc` file 
which is executed when starting a terminal session.

.. code-block:: bash
   :linenos:

   # 有多个版本的mpi时, 默认使用路径中靠前的版本

   echo "# OpenMPI-4.1.4" >> $HOME/.bashrc
   echo "MPI_HOME=$HOME/opt/openmpi"
   echo "export PATH=${MPI_HOME}/bin:$PATH" >> $HOME/.bashrc
   echo "export LD_LIBRARY_PATH=${MPI_HOME}/lib:$LD_LIBRARY_PATH" >> $HOME/.bashrc
   echo "export MANPATH=${MPI_HOME}/share/man:$MANPATH" >> $HOME/.bashrc
   echo ' ' >> $HOME/.bashrc
   source ~/.bashrc

   mpicc -v


卸载
--------------------

The make uninstall process from Open MPI a.b.c build tree should completely 
uninstall that version from the installation tree. Remove the old 
installation directory entirely and then install the new version.


测试
--------------------

.. code-block:: bash
   :linenos:

   cd openmpi-4.1.4/examples
   make


mpi4py
--------------------

.. code-block:: bash
   :linenos:

   pip install mpi4py

