Sphinx
====================

参考网站
--------------------

`Sphinx documentation (sphinx-doc.org)
<https://www.sphinx-doc.org/en/master/index.html>`_

`reStructuredText Primer — Sphinx documentation (sphinx-doc.org)
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_

`reStructuredText directives
<https://docutils.sourceforge.io/docs/ref/rst/directives.html>`_

`A Brief Tutorial On Sphinx (iridescent.ink)
<https://iridescent.ink/HowToMakeDocs/index.html>`_

`Sphinx + Read the Docs 从懵逼到入门 - 知乎 (zhihu.com)
<https://zhuanlan.zhihu.com/p/264647009>`_


安装
--------------------

.. code-block:: bash
   :linenos:
   
   # 卸载 ubuntu 低版本 sphinx
   sudo apt remove python3-sphinx

   # 安装新版本 sphinx
   conda install sphinx
   pip install sphinx-autobuild
   pip install sphinx_rtd_theme


初始化文档
--------------------

.. code-block:: bash
   :linenos:
   
   # 新建文档目录 doc
   cd doc
   sphinx-quickstart

   # > Separate source and build directories (y/n) [n]: y
   # > Project name: Notes
   # > Author name(s): Li Runze
   # > Project release []: v0.1
   # > Project language [en]: zh_CN   (中文)

   # 手动更新 html 文件
   make html

   # 自动更新 html 文件
   sphinx-autobuild source build/html

   # 如果报错无法找到 sphinx-autobuild, 需要进行软链接
   # sudo ln -s {conda 安装的路径} {ubuntu 默认的路径}
   sudo ln -s /home/lrz/opt/miniconda3/bin/sphinx-autobuild /usr/bin/sphinx-autobuild

   # 在浏览器中打开 html 文件
   # http://127.0.0.1:8000 


目录设置
--------------------

编写 source/index.rst

.. code-block:: rst
   :linenos:

   文档标题
   =================================

   .. toctree 目录
      maxdepth 目录层级
      numbered 章节自动编号层级

   .. toctree::
      :maxdepth: 2
      :numbered: 3
      :caption: 目录:

      chapter-1/index
      chapter-2/index

      about

   索引与表格
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


文档配置文件
--------------------

修改 conf.py

.. code-block:: python
   :linenos:
   

   # HTML 网页查看源码时，出现中文乱码
   # 需要确保编码的匹配: 源码文件编码, 源码编码设置值, 浏览器编码 要一致
   #   1) 源码文件 *.rst 采用 UTF-8 来支持不同特殊的字符
   #   2) conf.py 中的编码为 UTF-8
   source_encoding = 'utf-8-sig'
   
   #   3) 更改浏览器编码
   #      Edge 浏览器可以使用插件 “网页编码修改 (Charset)”

   # -------------------------------------------------------------------

   # 修改主题 Read the Docs Sphinx Theme
   # https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html
   html_theme = 'sphinx_rtd_theme'
   extensions = [
      ...,
      'sphinx_rtd_theme'
   ]
   html_static_path = ['_static']
   html_css_files = ['css/custom.css']

   # 配置主题
   # https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html

   html_theme_options = {
      # Toc options
      'collapse_navigation': True,
      'sticky_navigation': False,
      'navigation_depth': 4,
      'includehidden': True,
      'titles_only': False
   }

   # -------------------------------------------------------------------

   # 添加数学公式 (MathJax) 支持
   # https://docs.mathjax.org/en/latest/
   extensions = [
      ...,
      'sphinx.ext.mathjax'
   ]

   # -------------------------------------------------------------------

   # 激活 图、表、代码块、公式 的自动编号
   # 仅针对 有 caption (图例) 标签的对象，该对象的 `numref` 同时生效
   numfig = True

   # 图例形式
   numfig_format = {
      'figure': '图 %s',
      'table': '表 %s',
      'code-block': '代码 %s',
      'section': '节 %s',
   }

   # 设置公式编号形式, 如 Eq.10.
   math_eqref_format = 'Eq.{number}'  

   # 设置所有公式自动编号
   # 否则需自己标注 :label:
   math_number_all = False

   # 设置公式编号包含的章节层级
   math_numfig = True
   numfig_secnum_depth = 2



数学公式
--------------------

`Sphinx Doc: Math directives 
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-math>`_


行内公式 
++++++++++++++++++

在文本中写入 ``{:math:`\sum\limits_{k=1}^\infty \frac{1}{2^k} = 1`}``

显式效果：:math:`\sum\limits_{k=1}^\infty \frac{1}{2^k} = 1`

单独公式
++++++++++++++++++

.. code-block:: rst
   :linenos:

   .. math:: 
      e^{i\pi} + 1 = 0
      :label: euler

公式 :math:numref:`euler` 显式效果：

.. math:: e^{i\pi} + 1 = 0
   :label: euler

交叉引用公式的标识为 ``:eq:`euler``` 或 ``:math:numref:`euler``。

内部换行公式：

.. code-block:: rst
   :linenos:

   .. math:: 
      (a + b)^2  &=  (a + b)(a + b) \\
               &=  a^2 + 2ab + b^2
      :label: 2line

公式 :math:numref:`2line` 显式效果：

.. math:: 
   (a + b)^2  &=  (a + b)(a + b) \\
            &=  a^2 + 2ab + b^2
   :label: 2line


编号形式调整
++++++++++++++++++

链接：`公式编号右侧对齐的设置
<https://stackoverflow.com/questions/14110790/numbered-math-equations-in-restructuredtext/52509369#52509369>`_
, 需要自定义 css 文件。

在 _static/css/cutsom.css 中写入：

.. code-block:: css

   .math {
      text-align: left;
   }

   .eqno {
      float: right;
   }




