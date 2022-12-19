非结构网格下的 PDE 求解
=================================

.. seealso::
    `Sezai, ME 555: Computational Fluid Dynamics (Chapter 11), Eastern Mediterranean University
    <https://opencourses.emu.edu.tr/pluginfile.php/13802/mod_resource/content/2/chapter%2011e.pdf>`_

以积分形式对流-扩散方程 (:eq:`conv-diff-integral`) 为例:

.. math:: 
    \frac{\partial}{\partial t} \int_V{\phi \, dV} 
    + \int_S{\mathbf{n} \cdot (\phi \mathbf{v}) dA}
    = \int_S{\mathbf{n} \cdot (\Gamma \nabla \phi) dA}
    + \int_V{S_{\phi} \, dV} 


(1) 对流项的离散
---------------------------------

对流项离散形式为 (:eq:`unstructured-convection`):

.. math::
    \int_S{(\phi \mathbf{v}) \cdot d\mathbf{A}} \approx
    \sum_f \dot m_f \phi_f

其中, 质量流率 :math:`\dot m_f = \mathbf{v}_f \cdot \mathbf{A}_f`, 
定义对流通量 (convective flux) 为 :math:`F_f = \dot m_f \phi_f`。

在不可压流体模拟中，
计算网格面中心的 :math:`\mathbf{v}_f` 需要动量差分方法 (momentum interpolation method, Rhie and Chow)。

对流项由于存在双曲性质，因此需要对网格面中心的 :math:`\phi_f` 进行合理的重构 (迎风格式)。


(1.a) 一阶迎风格式
+++++++++++++++++++++++++++++++++

.. math::
    F_f^U = \max(\dot m_f, 0) \phi_P + \min(\dot m_f, 0) \phi_N
    :label: unstructured-flux-upwind-1

(1.b) 二阶迎风格式
+++++++++++++++++++++++++++++++++

.. math::
    \tilde{\phi}_f = \left\{ \begin{array}{l}
    \phi_P + \nabla \phi_P \cdot \mathbf{r}_{Pf}, & \dot m_f \ge 0 \\
    \phi_N + \nabla \phi_N \cdot \mathbf{r}_{Nf}, & \dot m_f \lt 0
    \end{array}\right.
    :label: unstructured-flux-upwind-2

其中, :math:`\nabla \phi_P, \nabla \phi_N` 的计算见式 :eq:`cell-center-gradient-explicit`。

在显式时间推进中, :math:`F_f = \dot m_f \tilde{\phi}_f`。

在隐式时间推进 (:eq:`implicit-method`) 中，通常仅将一阶重构部分使用隐式格式:

.. math::
    F_f =& \hat{F}_f^U - F_f^U + \left\{ \begin{array}{l}
    \phi_P + \nabla \phi_P \cdot \mathbf{r}_{Pf}, & \dot m_f \ge 0 \\
    \phi_N + \nabla \phi_N \cdot \mathbf{r}_{Nf}, & \dot m_f \lt 0
    \end{array}\right. \\
    \hat{F}_f^U =& \max(\dot m_f, 0) \hat{\phi}_P + \min(\dot m_f, 0) \hat{\phi}_N
    :label: unstructured-flux-upwind-2-implicit

(1.c) Rhie-Chow interpolation
+++++++++++++++++++++++++++++++++

.. seealso::
    `Seok Ki Choi, Use of the momentum interpolation method for numerical solution of 
    incompressible flows in complex geometries: choosing cell face velocities, 1992
    <https://www.tandfonline.com/doi/abs/10.1080/10407799308914888>`_

Rhie-Chow 差分是非交错网格上 (collocated grid) 不可压缩流动模拟中避免奇偶失联现象 (checkerboard oscillations)
的一种修正的网格中心向网格面中心的插值方法 (交错网格, staggered grid)。


(2) 扩散项的离散
---------------------------------

扩散项离散形式为 (:eq:`unstructured-diffusion`):

.. math::
    \int_S{(\Gamma \nabla \phi) \cdot d\mathbf{A}} \approx
    \sum_f (\Gamma \nabla \phi)_f \cdot \mathbf{A}_f

根据式 :eq:`unstructured-face-diffusion-correction` 计算 :math:`\nabla \phi_f \cdot \mathbf{A}_f`,
根据式 :eq:`interpolation-face-center` 计算 :math:`\Gamma_f` 即可。

以上计算过程中只用到了相邻的网格 (neighbors), 因此相当于结构网格的中心格式。


(3) 源项的离散
---------------------------------

源项离散形式为 (:eq:`unstructured-source`):

.. math::
    \int_V{S_{\phi} \, dV} \approx S_{\phi} V




(4) 时间推进
---------------------------------

