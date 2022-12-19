PDE 数值模拟方法概述
===========================

.. seealso::

    `Numerical Methods for Partial Differential Equations: FDM and FVM, Sandip Mazumder, 2016
    <https://www.sciencedirect.com/book/9780128498941/numerical-methods-for-partial-differential-equations>`_


(1) 基础概念
---------------------------


(1.a) 常见名词对照及解释
+++++++++++++++++++++++++++

.. list-table:: 常见名词对照表
   :width: 100
   :header-rows: 1
   :align: center

   * - 名词
     - 英文及缩写
     - 解释
    
   * - 有限差分方法
     - finite difference method (FDM)
     - 数据 (原始变量) 存储于 node

   * - 有限体积方法
     - finite volume method (FVM)
     - 数据 (守恒变量的体积平均值) 存储于 cell center

   * - 有限元方法
     - finite element method (FEM)
     - 数据 (基函数系数) 存储于 node

   * - 原始变量
     - primitive variable
     - 速度 :math:`\mathbf{v}`、压力 :math:`p`、温度 :math:`T`

   * - 守恒变量
     - conserved variable
     - :math:`\rho`, :math:`\rho \mathbf{v}`, :math:`\rho e`

   * - 计算单元
     - node
     - 离散方程的数据存储单元

   * - 网格
     - grid, mesh
     - FDM 的 node

   * - 控制体
     - control volume
     - FVM 的理论分析单元，计算单元 (cell)

   * - 网格单元
     - cell
     - FVM 的 node, 通常二维是三角形/四边形，三维是四面体/六面体
   
   * - 网格点
     - vertex (vertices)
     - FVM cell 的角点，等同于 node

   * - 网格面
     - face
     - FVM cell 的边界，二维是线段，三维是面

   * - 通量
     - flux
     - 原始变量在单位面积上的流量

   * - 离散误差
     - discretization/truncation error
     - 有限的离散 node 对连续函数进行近似的误差

   * - 截断误差
     - round-off error
     - 计算机数据储存的有效位数有限导致的误差

   * - 离散误差阶数
     - order of the truncation error
     - 与网格尺度呈指数关系

   * - 格式阶数
     - order of the scheme
     - 格式阶数只在均匀网格上达到离散误差阶数


(1.b) FDM 与 FVM 的区别
+++++++++++++++++++++++++++

#. FDM 是对偏微分方程的直接离散，称为强形式 (strong form)。
   FDM 不能保证解的守恒性。

   FVM 首先对偏微分方程的守恒变量在控制体上积分，
   再用网格中心数值对物理场进行近似 (离散)，称为弱形式 (weak form)。  
   FVM 本质上保证了解的局部和全局守恒性。

#. 单元方程 (nodal equation) 形式不同:

   FDM: 网格上的导数需要使用其他网格进行重构。

   FVM: :math:`\sum_{k}{\mathbf{J}_{i,k}}=S_iV_i`,
   :math:`\mathbf{J}_{i,k}` 是网格单元 :math:`i` 的 :math:`k` 网格面上的通量。
   通量需要使用其他网格单元进行重构。

#. 两种离散形式对格式误差没有本质影响，
   但是 FDM 对于复杂几何的处理能力较差。

#. FDM 和 FVM 的边界条件处理形式完全不同，这是两者的主要区别。


(1.c) 离散方程形式
+++++++++++++++++++++++++++

一般形式：

.. math:: 
   [A] [\phi] = [Q]
   :label: general-discrete-eqn

其中，:math:`[\phi]` 为因变量向量, :math:`[Q]` 为右端项向量。
:math:`[A]` 为系数矩阵，每行代表一个单元方程 (nodal equation), 
由于每个 node 只依赖于少数其他模板点 (stencil), 因此 :math:`[A]` 是一个稀疏矩阵。

有限差分方法：

.. math:: 
   \sum_{k=1}^{N_\text{node}}A_{i,k}\phi_k=Q_i, \;\;\;\; 
   \forall i=1,2,...,N_\text{node}
   :label: discrete-fdm

有限体积方法：

.. math:: 
   \sum_{k=1}^{N_\text{cell}}A_{i,k}\phi_k=Q_i V_i, \;\;\;\; 
   \forall i=1,2,...,N_\text{cell}
   :label: discrete-fvm

:math:`V` 为网格单元体积。


(1.d) 有限体积方法简介
+++++++++++++++++++++++++++

有限体积方法主要包括两个关键环节: 重构和演化。

 由 :math:`\bar{u}_k^n (k=1,2,\cdots,M)` 求出 :math:`n` 时刻数值解沿 *x* 方向的分布
 :math:`u^n (x)`, 这一过程称为重构 (reconstruction)。

 由 :math:`t_n` 时刻刻数值解沿 *x* 方向的分布 :math:`u^n (x)`, 
 求出 :math:`[t_n, t_{n+1}]` 之间的 :math:`u_{j+1/2} (t)` 以及数值通量 
 :math:`\hat{f}^n_{j+1/2} = \frac{1}{\Delta t} \int _{t_n} ^ {t_{n+1}} f(u_{j+1/2}(t)) dt`,
 这一过程称为演化 (evolution) 过程。

有限体积方法中将在这两个过程中引入近似，从而把积分型方程化为代数方程。
当演化步用精确的特征关系计算时，有限体积的精度取决于重构步。

在实际应用中，对半离散方法的时间导数项进行离散后，即可得到进行数值计算的全离散形式。
时间方向的离散可以采用前面介绍过的 Runge-Kutta 方法、Crank-Nicolson 方法等。

重构过程：已知所有网格单元的体积平均守恒变量 
:math:`\bar{\mathbf{U}}_j = \int_{\Omega_j} {\mathbf{U}(\mathbf{x})} d \mathbf{x} / \bar{\Omega}_j`,
在每个网格单元 :math:`\Omega_j` 上求一个 *k* 次多项式 
:math:`{\mathbf{u}}_j (\mathbf{x})`,
使得在 :math:`\Omega_j` 上成立
:math:`{\mathbf{u}}_j (\mathbf{x}) = {\mathbf{V}}_j (\mathbf{x}) + O(h^{k+1})`。
其中, :math:`\mathbf{V} (\mathbf{x})` 是精确解, :math:`h` 是网格单元长度尺度。


重构的基本要求:

- 守恒性: :math:`\bar{\mathbf{U}}_j = \int_{\Omega_j} {{\mathbf{u}}_j(\mathbf{x})} d \mathbf{x} / \bar{\Omega}_j``;

- 紧致性: *k* 次多项式 :math:`{\mathbf{u}}_j(\mathbf{x})` 仅由 :math:`\Omega_j` 及其邻近的有限控制体决定;

- K-exactness: 若精确解 :math:`\mathbf{V} (\mathbf{x})` 
  在 :math:`\Omega_j` 附近是次数小于等于 *k* 的多项式, 则
  :math:`{\mathbf{u}}_j(\mathbf{x}) = \mathbf{V} (\mathbf{x})`。

现状: 有限体积方法的重构以线性重构 (空间二阶精度) 为主。

演化过程:

与某个界面相邻的两个单元内有两个重构多项式, 其在界面两侧的值一般有间断。
演化过程需要根据有间断的初值得到界面处物理量的演化过程。
计算演化过程有多种方法: Jameson 中心型, 迎风型 (FVS, AUSM, Godunov, Roe) 等。


(2) 时间导数项
---------------------------

虽然定常问题没有时间导数项，但是直接求解定常问题的系数矩阵通常条件数较大。
在存在多解的情况下，直接求解定常方程会导致解的跳跃。总体而言，
使用时间推进求解定常问题也是一个不错的选择。


(2.a) Method of lines
++++++++++++++++++++++++++++++++++

一种将 PDE 转换为一组 ODE 的方法，进而可以使用不同的常微分方法进行时间推进。

偏微分方程可以写为 :eq:`half-discrete-pde` 形式，
其中, :math:`R` 是关于 :math:`\phi` 的空间偏微分函数。

.. math:: 
   \frac{\partial \phi}{\partial t} = R(\phi, \mathbf{x})
   :label: half-discrete-pde

那么，对于离散后的各个 node, :math:`\phi_{x=x_i}` 
的值仅由有限个 node 的未知因变量 :math:`\phi` 以及自变量 :math:`\mathbf{x}` 决定。
因此，:eq:`half-discrete-pde` 变为常微分方程，可写为以下形式：

.. math:: 
   \left[ \frac{\partial \phi}{\partial t} \right]_{x=x_i} = 
   \frac{d \phi_i}{d t} = f_i(\phi_1, \phi_2, ..., \phi_N)
   :label: method-of-lines

注意，对于动网格而言, :eq:`method-of-lines` 不再成立。


(2.b) 半离散方法
++++++++++++++++++++++++++++++++++

为了方便分析计算方法的性质，常常保留时间/空间导数的连续形式，
只离散空间/时间导数，此时的计算格式称为半离散格式。
空间离散的半离散格式形式与 :eq:`method-of-lines` 相同。

引入空间离散的半离散格式的目的，在于方便分析差分格式的性质，
以发展性能良好的空间差分格式。空间离散方案确定后，
可采用任意的方法离散时间导数，从而得到实用的全离散格式。

常见的时间离散方法有：

- 一阶 Euler 显式格式；
- 一阶 Euler 隐式格式；
- 二阶 Crank-Nicolson 格式；
- Runge-Kutta 格式；


(2.c) Euler 显式格式
+++++++++++++++++++++++++++

显式时间推进 (Forward Euler method), 没有线性方程组求解或矩阵求逆，内存需求小，程序简单。
但是，由于有数值稳定性条件，时间推进步长很小。

:eq:`method-of-lines` 中 :math:`R(\phi, \mathbf{x})` 
全部使用当前时间步的 :math:`\phi` 计算下一时间步的 :math:`\hat \phi`:

.. math:: 
   \hat \phi_i = \phi_i + \Delta t \, f_i (\phi_k | k=1,...,N)
   :label: explicit-method


(2.d) Euler 隐式格式
+++++++++++++++++++++++++++

隐式时间推进 (Backward Euler method), 需要迭代求解线性方程组，无条件稳定。
但是，根据时间推进的格式阶数，也不能取过大的时间步长。
相比之下，隐式时间推进的时间步长还是远大于显示时间推进。

:eq:`method-of-lines` 中 :math:`R(\phi, \mathbf{x})` 
全部使用下一时间步的 :math:`\hat \phi` 来计算 :math:`\hat \phi`:

.. math:: 
   \hat \phi_i = \phi_i + \Delta t \, f_i (\hat \phi_k | k=1,...,N)
   :label: implicit-method


(2.e) Crank-Nicolson 格式
+++++++++++++++++++++++++++

二阶隐式时间推进，无条件稳定，可选取更大的时间步长。
:eq:`method-of-lines` 的右端项使用当前时间步和下一时间步的加权：

.. math:: 
   \hat \phi_i = \phi_i + \Delta t 
   \left[ \alpha f_i (\phi_k | k=1,...,N) +
   \beta f_i (\hat \phi_k | k=1,...,N) \right]
   :label: cn-method

其中，系数 :math:`\alpha=\beta=1/2`。
若 :math:`\alpha=1-\beta` 取其他值，那么称为综合格式。


(2.f) Runge-Kutta 格式
+++++++++++++++++++++++++++

显式分步时间推进格式，最为常用的是三步三阶 TVD 型 R-K 格式：

.. math:: 
   & \left\{
        \begin{array}{ll}
            \phi_i^{(1)} &= \phi_i + \Delta t f_i(\phi_k|k=1,...,N) \\
            \phi_i^{(2)} &= \frac{3}{4} \phi_i + \frac{1}{4} 
            [\phi_i^{(1)} + \Delta t f_i(\phi_k^{(1)}|k=1,...,N)] \\
            \hat \phi_i  &= \frac{1}{3} \phi_i + \frac{2}{3}
            [\phi_i^{(2)} + \Delta t f_i(\phi_k^{(2)}|k=1,...,N)]
      \end{array}
   \right.
   :label: rk-3-tvd


(3) 空间一阶导数项
---------------------------

(3.a) 有限差分方法
+++++++++++++++++++++++++++

二阶中心差分格式:

.. math::
   \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x}
   :label: dx-center-2

四阶中心差分格式:

.. math::
   \frac{-\phi_{i+2}+8\phi_{i+1}-8\phi_{i-1}+\phi_{i-2}}{12 \Delta x}
   :label: dx-center-4

Jameson 格式：

.. math::
   \frac{\phi_{i+1}-\phi_{i-1}}{\Delta x}
   + \epsilon \frac{\phi_{i+2}-4\phi_{i+1}+6\phi_{i}-4\phi_{i-1}+\phi_{i-2}}{\Delta x}
   :label: dx-jameson

空间二阶精度，含人工粘性 (:math:`\epsilon` 为小正数)。

记，空间一阶导数项 :math:`a \frac{\partial \phi}{\partial x}`。

一阶迎风格式:

.. math::
   & \left\{
        \begin{array}{ll}
            \frac{\phi_{i}-\phi_{i-1}}{\Delta x}, & a \ge 0 \\
            \frac{\phi_{i+1}-\phi_{i}}{\Delta x}, & a \lt 0
      \end{array}
   \right.
   :label: dx-u-1

二阶迎风格式:

.. math::
   & \left\{
        \begin{array}{ll}
            \frac{a}{2\Delta x}[3\phi_i-4\phi_{i-1}+\phi_{i-2}], & a \ge 0 \\
            \frac{a}{2\Delta x}[-3\phi_i+4\phi_{i+1}-\phi_{i+2}], & a \lt 0
      \end{array}
   \right.
   :label: dx-u-2

三阶迎风/中心型格式:

.. math::
   & \left\{
        \begin{array}{ll}
            \frac{a}{6\Delta x}[2\phi_{i+1}+3\phi_i-6\phi_{i-1}+\phi_{i-2}], 
            & a \ge 0 \\
            \frac{a}{6\Delta x}[-2\phi_{i-1}-3\phi_i+6\phi_{i+1}-\phi_{i+2}], 
            & a \lt 0
      \end{array}
   \right.
   :label: dx-u-3

.. note::
   空间二阶导数项通常使用中心差分格式。
