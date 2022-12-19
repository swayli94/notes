三维有限体积方法
=================================

通用坐标系下的无量纲三维非定常可压缩 Navier-Stokes 方程组 (:eq:`rans-eqn-general`)
可以写为半离散有限体积形式，表现为满足守恒律的积分形式:

.. math::
    \frac{\partial}{\partial t} \int_V \mathbf{U} dV +
    \int_S \mathbf{f} \cdot \mathbf{n} dS = 0
    :label: fvm-3d

其中, :math:`\mathbf{f}` 是在控制体 :math:`V` 的表面 :math:`S` 上的净通量 (net flux),
:math:`\mathbf{n}` 是表面的单位法向量。


