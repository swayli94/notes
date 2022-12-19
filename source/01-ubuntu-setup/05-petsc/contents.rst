PESTc
====================

参考网站
--------------------

`Install — PETSc 3.18.2 documentation
<https://petsc.org/release/install/>`_

`Third Party Packages | ADflow
<https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/installInstructions/install3rdPartyPackages.html>`_


安装过程
--------------------

.. code-block:: bash
   :linenos:
   
   # unzip in the target directory, e.g., $HOME/opt/
   cd ~/opt/
   wget https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.18.2.tar.gz
   tar -xvf petsc-3.18.2.tar.gz

   # 安装路径为当前路径
   cd petsc-3.18.2

   ./configure --PETSC_ARCH=real-opt --with-mpi-dir=${MPI_HOME} \
   --with-scalar-type=real --with-debugging=0 \
   --download-metis=yes --download-parmetis=yes \
   --download-superlu_dist=yes --download-fblaslapack=yes \
   --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11   

   make PETSC_DIR=$HOME/opt/petsc-3.18.2 PETSC_ARCH=real-opt all

   # Check if the libraries are working
   make PETSC_DIR=$HOME/opt/petsc-3.18.2 PETSC_ARCH=real-opt check


添加环境变量
--------------------

.. code-block:: bash
   :linenos:
   
   echo '# Petsc-3.18.2' >> $HOME/.bashrc
   echo 'export PETSC_DIR=$HOME/opt/petsc-3.18.2' >> $HOME/.bashrc
   echo 'export PETSC_ARCH=real-opt' >> $HOME/.bashrc
   echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/.bashrc
   echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/.bashrc
   echo ' ' >> $HOME/.bashrc
   source ~/.bashrc


petsc4py
--------------------

.. code-block:: bash
   :linenos:

   # petsc4py-3.18.2
   cd $PETSC_DIR/src/binding/petsc4py
   pip install .

   # Conda 更新 **conda/lib/libstdc++.so.6
   conda install -c anaconda libstdcxx-ng

