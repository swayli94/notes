控制方程
===========================

(1) Navier-Stokes 方程组
---------------------------

守恒形式控制方程：

.. math:: 
   \frac{\partial \mathbf{U}}{\partial t} + 
   \frac{\partial \mathbf{F}}{\partial x} + 
   \frac{\partial \mathbf{G}}{\partial y} + 
   \frac{\partial \mathbf{H}}{\partial z} = J
   :label: ns-eqn-c

守恒变量 (conserved variables) 解向量：

.. math:: 
   \mathbf{U} = [\rho, \rho u, \rho v, \rho w, \rho E]^T
   :label: conserved-variable

相应的原始变量 (primitive variables): :math:`\rho, u, v, w, p`。
其中, :math:`p` 是压力, :math:`\rho` 是密度, :math:`V` 是速度模长。

比内能 (specific internal energy) :math:`e`,
比总能 (specific total energy) :math:`E=e+\frac{V^2}{2}`

比焓 (specific enthalpy) :math:`h=e+p/ \rho`, 
比总焓 :math:`H=h+\frac{V^2}{2}`。

对于量热完全气体，比热比 :math:`\gamma` 为常数, 
:math:`R` 为普适气体常数，:math:`T` 为温度，有：

.. math:: 
   e=c_vT=\frac{RT}{\gamma-1}=\frac{p}{(\gamma-1)\rho}
   :label: eqn-e

.. math:: 
   p = \rho R T
   :label: state-eqn

.. math::
   h = \gamma e
   :label: enthalpy-eqn

.. math::
   H = \gamma E - \frac{1}{2}(\gamma-1)V^2 = E + p/\rho
   :label: total-enthalpy-eqn

从守恒变量计算压力的公式：

.. math::
   p = (\gamma-1)[(\rho E) - 0.5 \rho V^2]
   :label: p-from-c

通量向量：

.. math:: 
   \mathbf{F} = \left[
      \begin{array}{lr}
         \rho u \\
         \rho u^2+p-\tau_{xx} \\
         \rho uv-\tau_{xy} \\
         \rho uw-\tau_{xz} \\
         \rho Eu + pu - k\frac{\partial T}{\partial x}
         -u \tau_{xx} -v \tau_{xy} -w \tau_{zx}
      \end{array}
   \right]
   :label: ns-f

.. math:: 
   \mathbf{G} = \left[
      \begin{array}{lr}
         \rho v \\
         \rho uv-\tau_{xy} \\
         \rho v^2+p-\tau_{yy} \\
         \rho vw-\tau_{yz} \\
         \rho Ev + pv - k\frac{\partial T}{\partial y}
         -u \tau_{xy} -v \tau_{yy} -w \tau_{yz}
      \end{array}
   \right]
   :label: ns-g

.. math:: 
   \mathbf{H} = \left[
      \begin{array}{lr}
         \rho w \\
         \rho uw-\tau_{zx} \\
         \rho vw-\tau_{yz} \\
         \rho w^2+p-\tau_{zz} \\
         \rho Ew + pw - k\frac{\partial T}{\partial z}
         -u \tau_{zx} -v \tau_{yz} -w \tau_{zz}
      \end{array}
   \right]
   :label: ns-h

源项向量：

.. math:: 
   \mathbf{J} = \left[
      \begin{array}{lr}
         0 \\
         \rho g_x \\
         \rho g_y \\
         \rho g_z \\
         \rho(ug_x+vg_y+wg_z)+\rho \dot {q}
      \end{array}
   \right]
   :label: ns-j

其中, :math:`\tau` 是粘性应力张量, 形式为 :eq:`vis-stress`。
:math:`\tau_{ij}` 是粘性应力张量的 :math:`i,j` 分量。

式 :eq:`vis-stress` 中 :math:`\mu` 是分子粘性系数，对于量热完全气体，有 
Sutherland's Formula: 

.. math::
    \mu = \mu_0 \left(\frac{T}{T_0}\right)^{3/2} \frac{T_0+110}{T+110}
    :label: sutherland-eqn

其中, :math:`\mu_0` 和 :math:`T_0` 是标准海平面条件下的分子粘性和温度 (单位: K)。

:math:`\mathbf{g}` 是体积力向量, :math:`g_{i}` 是体积力的 :math:`i` 分量。
:math:`k` 是热导率, 热流通量 :math:`\dot{\mathbf{q}}=-k \nabla T`。


(2) Euler 方程组
---------------------------

非守恒形式：

.. math:: 
   & \left\{
        \begin{array}{l}
            \frac{D \rho}{D t} = - \rho \nabla \cdot \mathbf{v}  \\
            \frac{D \mathbf{v}}{D t} = 
            - \frac{\nabla p}{\rho} + \mathbf{g} \\
            \frac{D e}{D t} = 
            - \frac{p}{\rho} \nabla \cdot \mathbf{v} \\
      \end{array}
   \right.
   :label: euler-eqn-nc

守恒形式控制方程仍然是 :eq:`ns-eqn-c`。
通量向量中取 :math:`\tau_{ij}=0`, 并去掉温度梯度项。

声速为 :math:`a=\sqrt{\gamma p/\rho}`。


(3) 通用坐标系 NS 方程组
---------------------------

假定计算是在贴体正交网格坐标系 (通用坐标系, generalized coordinates) 下进行，
且网格刚性地固联于物体做非定常运动。
通用坐标系下的无量纲三维非定常可压缩 Navier-Stokes 方程组:

.. math:: 
   \frac{\partial \hat{\mathbf{U}}}{\partial t} + 
   \frac{\partial (\hat{\mathbf{F}}-\hat{\mathbf{F}}_{\nu})}{\partial \xi} + 
   \frac{\partial (\hat{\mathbf{G}}-\hat{\mathbf{G}}_{\nu})}{\partial \eta} + 
   \frac{\partial (\hat{\mathbf{H}}-\hat{\mathbf{H}}_{\nu})}{\partial \zeta} = 0
   :label: rans-eqn-general

其中，笛卡尔坐标 :math:`x, y, z` 与通用坐标 :math:`\xi(x,y,z,t), \eta(x,y,z,t), \zeta(x,y,z,t)` 
的转换雅可比矩阵 (Jacobian of the transformation) 为:

.. math::
   J = \frac{\partial (\xi, \eta, \zeta, t)}{\partial (x,y,z,t)}
   :label: jacobian-coordinates

通常认为通用坐标系中, 两个网格中心间的空间坐标差量 :math:`\Delta \xi, \Delta \eta, \Delta \zeta` 等于 1。

.. note::
   为了简单起见，将坐标转换雅可比矩阵的模记为 :math:`J`, 数值上等于网格单元体积的倒数。

守恒变量向量 (vector of conserved variables):

.. math::
   \hat{\mathbf{U}} = \mathbf{U}/J = [\rho, \rho u, \rho v, \rho w, \rho E]^T/J
   :label: conserved-variable-general

无粘通量 (inviscid flux):

.. math::
   \hat{\mathbf{F}} = \frac{1}{J}
   \left[\begin{array}{c}
   \rho U \\ \rho U u + \xi_x p \\ \rho U v + \xi_y p \\
   \rho U w + \xi_z p \\ \rho H U - \xi_t p
   \end{array}\right], 
   \hat{\mathbf{G}} = \frac{1}{J}
   \left[\begin{array}{c}
   \rho V \\ \rho V u + \eta_x p \\ \rho V v + \eta_y p \\
   \rho V w + \eta_z p \\ \rho H V - \eta_t p
   \end{array}\right], 
   \hat{\mathbf{H}} = \frac{1}{J}
   \left[\begin{array}{c}
   \rho W \\ \rho W u + \zeta_x p \\ \rho W v + \zeta_y p \\
   \rho W w + \zeta_z p \\ \rho H W - \zeta_t p
   \end{array}\right]
   :label: inviscid-flux-general

逆变速度 (contravariant velocities):

.. math::
   \begin{array}{l}
   U &= \xi_x u + \xi_y v +\xi_z w + \xi_t \\
   V &= \eta_x u + \eta_y v +\eta_z w + \eta_t \\
   W &= \zeta_x u + \zeta_y v +\zeta_z w + \zeta_t
   \end{array}
   :label: contravariant-velocities

粘性通量 (viscous flux):

.. math::
   \hat{\mathbf{F}}_v = \frac{1}{J}
   \left[\begin{array}{c}
   0 \\ 
   \xi_x \tau_{xx} + \xi_y \tau_{xy} + \xi_z \tau_{xz} \\
   \xi_x \tau_{xy} + \xi_y \tau_{yy} + \xi_z \tau_{yz} \\
   \xi_x \tau_{xz} + \xi_y \tau_{yz} + \xi_z \tau_{zz} \\
   \xi_x b_x + \xi_y b_y + \xi_z b_z
   \end{array}\right]
   :label: viscous-flux-general-f

.. math::
   \hat{\mathbf{G}}_v = \frac{1}{J}
   \left[\begin{array}{c}
   0 \\ 
   \eta_x \tau_{xx} + \eta_y \tau_{xy} + \eta_z \tau_{xz} \\
   \eta_x \tau_{xy} + \eta_y \tau_{yy} + \eta_z \tau_{yz} \\
   \eta_x \tau_{xz} + \eta_y \tau_{yz} + \eta_z \tau_{zz} \\
   \eta_x b_x + \eta_y b_y + \eta_z b_z
   \end{array}\right]
   :label: viscous-flux-general-g

.. math::
   \hat{\mathbf{H}}_v = \frac{1}{J}
   \left[\begin{array}{c}
   0 \\ 
   \zeta_x \tau_{xx} + \zeta_y \tau_{xy} + \zeta_z \tau_{xz} \\
   \zeta_x \tau_{xy} + \zeta_y \tau_{yy} + \zeta_z \tau_{yz} \\
   \zeta_x \tau_{xz} + \zeta_y \tau_{yz} + \zeta_z \tau_{zz} \\
   \zeta_x b_x + \zeta_y b_y + \zeta_z b_z
   \end{array}\right]
   :label: viscous-flux-general-h

切应力张量 (shear stress) 和热流 (heat flux) 以张量形式给出
(含爱因斯坦求和假设):

.. math::
   \tau_{ij} = \frac{M_{\infty}}{Re_R}
   \left[\mu \left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i} \right)
   + \lambda \left( \frac{\partial u_k}{\partial x_k} \right) \delta_{ij} \right]
   :label: shear-stress

.. math::
   b_i = u_k \tau_{ik} - \dot q_i
   :label: heat-flux-b

.. math::
   \dot q_i = -\left[ \frac{M_{\infty} \mu}{Re_R \; Pr (\gamma-1)} \right]
   \frac{\partial a^2}{\partial x_i}
   :label: heat-flux-q

无量纲化参考变量: 来流密度 :math:`\tilde{\rho}_{\infty}`, 来流声速 :math:`\tilde{a}_{\infty}`,
来流分子粘性 :math:`\tilde{\mu}_{\infty}` (~ 代表有量纲参数)。

.. math::
   \begin{array}{l}
   \rho = \tilde{\rho}/\tilde{\rho}_{\infty}, u=\tilde{u}/\tilde{a}_{\infty},
   v=\tilde{v}/\tilde{a}_{\infty}, w=\tilde{w}/\tilde{a}_{\infty}, 
   p=\tilde{p}/(\tilde{\rho}_{\infty} \tilde{a}_{\infty}^2) \\
   \rho_{\infty}=1, p_{\infty}=1/\gamma, \\
   u_{\infty}=M_{\infty}\cos\alpha\cos\beta, 
   v_{\infty}= - M_{\infty}\sin \beta,
   w_{\infty}=M_{\infty}\sin\alpha\cos\beta \\
   e = \tilde{e}/(\tilde{\rho}_{\infty} \tilde{a}_{\infty}^2),
   a = \tilde{a}/\tilde{a}_{\infty}, 
   T = \tilde{T}/\tilde{T}_{\infty} = \gamma p/\rho = a^2 \\
   e_{\infty} = \frac{1}{\gamma(\gamma-1)} + \frac{M_{\infty}^2}{2},
   a_{\infty} = 1, T_{\infty}=1\\
   x = \tilde{x}/\tilde{L}_R, y = \tilde{y}/\tilde{L}_R, 
   z = \tilde{z}/\tilde{L}_R, t = \tilde{t}\tilde{a}_{\infty}/\tilde{L}_R
   \end{array}
   :label: non-dimensionalization

几何特征长度 :math:`\tilde{L}` (建议以 m 为单位), 
几何特征长度在网格中的数值 :math:`L_\text{ref}` (无量纲, 建议数值上乘1000, 即表现为以 mm 为单位),
程序中使用的参考长度 :math:`\tilde{L}_R=\tilde{L}/L_\text{ref}`。

那么, 雷诺数 :math:`Re=\tilde{\rho}\tilde{V}_{\infty}\tilde{L}/\tilde{\mu}_{\infty}`,
:math:`Re_R = Re / L_\text{ref}`。

:math:`M_\infty=\tilde{V}_{\infty}/\tilde{a}`, 
:math:`\tilde{V}_{\infty} = \sqrt{ \tilde{u}_{\infty}^2 + \tilde{v}_{\infty}^2 + \tilde{w}_{\infty}^2 }`。

无量纲分子粘性系数:

.. math::
   \mu = \tilde{\mu}/\tilde{\mu}_{\infty} = 
   T^{\frac{3}{2}}
   \left[
      \frac{1+\frac{\tilde c}{\tilde{T}_{\infty}}}
      {T+\frac{\tilde c}{\tilde{T}_{\infty}}}
   \right]
   :label: molecular-viscosity

其中, Sutherland's constant :math:`\tilde{c}=198.6 ^{\circ}R = 110.4 ^{\circ}K`。


