基础开发环境
====================

本节介绍后续使用的各个软件的安装命令。

.. code-block:: bash
   :linenos:
   
   # 更新 Ubuntu's Advanced Packaging Tool
   sudo apt update
   sudo apt-get update
   
   # 基础工具
   sudo apt-get install wget git git-lfs pkg-config tree apt-utils
   sudo apt-get install vim texinfo

   # 开发工具 
   sudo apt-get install build-essential gfortran flex swig bison
   sudo apt-get install gdb valgrind freeglut3-dev
   sudo apt-get install cmake cmake-curses-gui

   # 第三方库
   sudo apt-get install zlib1g-dev libfl-dev 
   sudo apt-get install liblapack-dev libmetis-dev libblas-dev
   sudo apt-get install libboost-system-dev libboost-thread-dev 
   sudo apt-get install libreadline-dev libncurses-dev 
   sudo apt-get install libxt-dev libscotch-dev libcgal-dev 
   sudo apt-get install libibverbs-dev ca-certificates  
   sudo apt-get install libxml2-utils
   sudo apt-get install libhdf5-dev

