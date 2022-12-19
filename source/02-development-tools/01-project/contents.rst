项目架构示例
===========================

参考网站
--------------------

`JackWetherell/cpp-project-structure: C++ project directory and file structure.
<https://github.com/JackWetherell/cpp-project-structure>`_

`ugnelis/cmake-cpp-project: A simple CMake C++ project structure. (github.com)
<https://github.com/ugnelis/cmake-cpp-project>`_


通用示例
--------------------

.. code-block:: bash
   :linenos:
   
    project/
    ├─bin/
    |   # 可执行文件和动态链接库
    ├─build/
    |   # 编译/链接中间目标文件
    ├─doc/
    |   # 文档
    ├─example/
    |   # 示例项目
    ├─include/
    |   # Public 头文件
    ├─lib/
    |   # 第三方库（或自己编译的静态库）
    ├─src/
    |   # Private 源文件和头文件
    ├─test/
    |   # 测试代码
    ├─COPYRIGHT
    ├─LICENSE
    ├─README.md


