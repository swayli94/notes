偏微分方程概述
===========================

.. seealso::

    `Numerical Methods for Partial Differential Equations: FDM and FVM, Sandip Mazumder, 2016
    <https://www.sciencedirect.com/book/9780128498941/numerical-methods-for-partial-differential-equations>`_


(1) 基础概念
---------------------------


(1.a) 方程性质
+++++++++++++++++++++++++++

偏微分方程 :eq:`general-pde` 中 :math:`x, y` 是两个自变量，
:math:`\phi` 是因变量，:math:`A, B, C` 是标量常数或方程。
对于以上两个自变量，记 :math:`K=B^2-4AC`。

.. math:: 
   A\frac{\partial^2 \phi}{\partial x^2} +
   B\frac{\partial^2 \phi}{\partial x \partial y} +
   C\frac{\partial^2 \phi}{\partial y^2} = 0
   :label: general-pde

若 :math:`K<0` 则称为椭圆型方程，需要在自变量空间的所有边界上定义边界条件。
`Laplace` 算子 :math:`\nabla^2` 也被称为椭圆型算子。

若 :math:`K=0` 则称为抛物型方程，
需要在自变量空间的上游边界上定义一个边界条件。
对于时间推进的常微分方程，也就是需要一个初始条件。

若 :math:`K>0` 则称为双曲型方程，


(2) 常见偏微分方程
---------------------------


(2.a) 扩散方程
+++++++++++++++++++++++++++

扩散方程 (diffusion equation) 描述物质的扩散过程，一般形式为 :eq:`diffusion-eqn`。
其中，扩散系数 :math:`\Gamma` 为正数，:math:`S_{\phi}` 为源项。
若没有时间导数项且源项为零，则称为 `Laplace` 方程。
若没有时间导数项且源项为非零常数，则称为 `Poisson` 方程。
若没有时间导数项且源项为 :math:`\phi` 的线性函数，则称为 `Helmholtz` 方程。

.. math:: 
   \frac{\partial \phi}{\partial t} = \nabla \cdot (\Gamma\nabla \phi) + S_{\phi}
   :label: diffusion-eqn

若源项为常数，则表现为热传导方程 :eq:`heat-transfer`，其中 :math:`T` 是温度。

.. math:: 
   \frac{\partial T}{\partial t} = \Gamma \nabla ^{2} T + S
   :label: heat-transfer

扩散方程通常是 **时间抛物-空间椭圆型** 方程。
若将计算 :math:`K=B^2-4AC` 的两个自变量选为 :math:`t` 和 :math:`x (y, z)`, 
此时 :math:`A=0, B=0`，因此，时间推进方向为抛物型。相应地，一维扩散方程是抛物型方程。

.. note::
   时间推进与空间离散的不同方程性质，以及相应造成的不同的边界条件需求，
   就是数值模拟中采用 **半离散方法** 的核心原因。


(2.b) 对流方程 (连续方程)
+++++++++++++++++++++++++++

对流方程描述守恒量在背景流动 (a bulk motion of a fluid) 
中的运移过程。以密度 :math:`\rho` 为例，对流方程即为 **连续方程** 
(:eq:`convection-eqn`)。其中，:math:`\mathbf{v}` 是速度矢量。

.. math:: 
   \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0
   :label: convection-eqn

Convection 和 advection 的中文翻译都是对流，两者在英文中也大都通用。
在地球物理中分别用于描述空气的垂直方向运动和水平方向运动。
在力学中 convection 一般用于指代 `热对流` 或数值模拟方法中的 `对流扩散方程` 。
而 advection 的意思更接近于 `输运`，维基百科中的解释是 
"advection is the transport of a substance or quantity by bulk motion, e.g., 
a velocity field"。

对于不可压缩流体，方程 :eq:`convection-eqn` 可简化为 :eq:`convection-eqn-simple`:

.. math:: 
   \frac{\partial \phi}{\partial t} + \mathbf{v} \cdot  \nabla \phi = 0
   :label: convection-eqn-simple

是一个 **时间抛物-空间双曲型** 方程。

其他一些简单形式的对流方程有线性对流方程:

.. math::
   \frac{\partial u}{\partial t} + a \frac{\partial u}{\partial x} = 0, \;\;
   a = \text{constant}
   :label: linear-convection

Burgers 方程：

.. math::
   \frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = 0
   :label: burgers-eqn


(2.c) 对流-扩散方程
+++++++++++++++++++++++++++

对流扩散方程 (convection-diffusion equation) 如 :eq:`conv-diff` 所示。

.. math:: 
   \frac{\partial \phi}{\partial t} = \nabla \cdot (\Gamma \nabla \phi)
   - \nabla \cdot (\mathbf{v} \phi) + S_{\phi}
   :label: conv-diff

对于不可压缩流体，方程 :eq:`conv-diff` 可简化为 :eq:`conv-diff-simple`:

.. math:: 
   \frac{\partial \phi}{\partial t} = \Gamma \nabla ^{2} \phi
   - \mathbf{v} \cdot \nabla \phi
   :label: conv-diff-simple

是一个 **时间抛物-空间双曲/椭圆混合型** 方程。


(2.d) 波动方程
+++++++++++++++++++++++++++

波动方程 (wave function, Maxwell's function) 有二阶时间导数，
因此，需要提供两个初始条件。

.. math:: 
   \frac{\partial^2 \phi}{\partial t^2} = c^2 \nabla ^{2} \phi
   :label: maxwell-eqn

是一个 **时间双曲-空间椭圆型** 方程。


(2.e) 柯西动量方程
+++++++++++++++++++++++++++

柯西动量方程 (Cauchy momentum equation, :eq:`cauchy-eqn`) 是描述连续流体中
非相对论动量传输的一般方程形式，其中最为典型的是 Navier-Stokes 动量方程 :eq:`ns-eqn`。

.. math:: 
   \frac{D \mathbf{v}}{D t} = \frac{1}{\rho} \nabla \cdot \mathbf{\sigma} 
   + \mathbf{g}
   :label: cauchy-eqn

其中，:math:`\mathbf{v}` 是流动速度矢量，:math:`\rho` 是密度，
:math:`\mathbf{\sigma}` 是应力张量，:math:`\mathbf{g}` 是体积力。

.. math:: 
   \rho \frac{D \mathbf{v}}{D t} = - \nabla p + \nabla \cdot \mathbf{\tau} 
   + \rho \mathbf{g}
   :label: ns-eqn

其中，:math:`p` 是压力，:math:`\mathbf{g}` 是体积力。
:math:`\frac{D}{D t} = \frac{\partial}{\partial t} + \mathbf{v}\cdot\nabla`
是质点导数。
:math:`\mathbf{\tau}` 是粘性应力张量 (viscous stress tensor) 
或切/偏应力张量 (deviatoric stress tensor), 形式为 :eq:`vis-stress`。

.. math:: 
   \mathbf{\tau}= \lambda (\nabla \cdot \mathbf{v}) \mathbf{I}
   + \mu \left[ \nabla \mathbf{v} + (\nabla \mathbf{v}) ^T \right]
   :label: vis-stress

其中, :math:`\mu` 是分子粘性系数，
第二粘性系数 :math:`\lambda=-\frac{2}{3}\mu` 是 Stokes 假设。

Navier-Stokes 动量方程是一个 **时间双曲-空间双曲/椭圆混合型** 方程。
当马赫数较小时，表现为空间椭圆型方程；当马赫数较大时，表现为空间双曲型方程。
不可压缩流体为空间椭圆型方程；无粘流动为空间双曲型方程。


(3) 边界条件
---------------------------


(3.a) 第一类边界条件
+++++++++++++++++++++++++++

Dirichlet boundary condition, 提供边界上的因变量值 :math:`\phi`。

在 :eq:`general-discrete-eqn` 中，
虽然理论上可以直接根据边界条件给 :math:`[\phi]` 向量中的边界 node 赋值，
并将该 node 对应的 nodal equation 从 :math:`[A] [\phi] = [Q]` 中去掉，
即缩减稀疏矩阵 :math:`[A]` 的维度。但是，这种做法过于复杂。
相反，对 :math:`[Q]` 向量中的相应位置按照边界条件计算其 "准确值",
从而约束 :math:`[\phi]` 的计算结果满足边界条件。

在右端项 :math:`[Q]` 向量中，可能出现 :math:`\phi` 的导数。
由于内点的差分格式中可能包含超出边界的模板点，需要重新推导边界的导数。
如，一维均匀网格上边界点 :math:`\phi_1` 由模板点 :math:`1,2,3` 计算：

.. math:: 
   \left [ \frac{\partial \phi}{\partial x} \right ]_1 = 
   \frac{4\phi_2-\phi_3-3\phi_1}{2 \Delta x}
   :label: boundary-1-d1

该边界导数由 Taylor 展开得到，为二阶精度。


(3.b) 第二类边界条件
+++++++++++++++++++++++++++

Neumann boundary condition, 
提供边界上的法向导数 :math:`\partial \phi / \partial n = J`,
也被称为通量边界条件。

虽然按照 :eq:`boundary-1-d1` 可以计算边界值 :math:`\phi_1`:

.. math:: 
   \frac{4\phi_2-\phi_3-3\phi_1}{2 \Delta x} = J
   :label: boundary-2-d1

但是 :eq:`boundary-2-d1` 丢失了控制方程的信息，
不能保证 :math:`\phi_1, \phi_2, \phi_3` 的值同时满足边界条件和控制方程。

需要使用 Taylor 展开和控制方程共同推导边界 node 的 nodal equation,
并相应修改系数矩阵 :math:`[A]`。


(3.c) 第三类边界条件
+++++++++++++++++++++++++++

Robin boundary condition,
提供边界上的因变量值和法向导数的线性组合 
:math:`\alpha \phi + \beta \partial \phi / \partial n`。

