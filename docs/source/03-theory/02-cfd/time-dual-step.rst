双时间步隐式时间推进
=================================


通用坐标系下的无量纲三维非定常可压缩 Navier-Stokes 方程组 (:eq:`rans-eqn-general`)
可以写为半离散形式:

.. math::
    \frac{1}{J} \frac{\partial \mathbf{U}}{\partial t} = \mathbf{R}(\mathbf{U})
    :label: half-discrete-ns

其中, 

.. math::
    \mathbf{R} = -\left[ 
    \frac{\partial (\hat{\mathbf{F}}-\hat{\mathbf{F}}_{\nu})}{\partial \xi} + 
    \frac{\partial (\hat{\mathbf{G}}-\hat{\mathbf{G}}_{\nu})}{\partial \eta} + 
    \frac{\partial (\hat{\mathbf{H}}-\hat{\mathbf{H}}_{\nu})}{\partial \zeta}
    \right]
    :label: residual-3d-general

显式时间推进方法可参考式 :eq:`explicit-method`, :eq:`rk-3-tvd`。

隐式时间推进采用以下格式离散:

.. math::
    \frac{(1+\phi)(\mathbf{U}^{n+1}-\mathbf{U}^n) 
    - \phi(\mathbf{U}^n-\mathbf{U}^{n-1})}{J \Delta t} =
    \mathbf{R}(\mathbf{U}^{n+1})
    :label: implicit-time-phi

其中, :math:`\phi=0.5` 时时间方向为二阶精度, :math:`\phi=0` 时时间方向为一阶精度。
该式在全流场联立，得到一个巨大的非线性方程组。


(1) 虚拟时间步与物理时间步
---------------------------------

为了计算非定常流动，在式 :eq:`implicit-time-phi` 中引入虚拟时间项 :math:`\partial \mathbf{U}/\partial \tau`, 
从而在每一个物理时间步 :math:`\Delta t` 内降低线化方程组的残差。
此方法称为双时间步 (dual time stepping)。
其中, :math:`(m)` 是子迭代步数 (sub-iteration counter)。记:

.. math::
    \frac{\mathbf{U}^{(m+1)}-\mathbf{U}^{(m)}}{J \Delta \tau} + 
    \frac{(1+\phi)(\mathbf{U}^{(m+1)}-\mathbf{U}^n) 
    - \phi(\mathbf{U}^n-\mathbf{U}^{n-1})}{J \Delta t} = \\
    \mathbf{R}(\mathbf{U}^{(m+1)})
    :label: implicit-dual-step

已知 :math:`\mathbf{U}^{(m)}` 时可以计算出 :math:`\mathbf{U}^{(m+1)}`, 
规定 :math:`\mathbf{U}^{(0)} = \mathbf{U}^{n}`。 
那么，迭代收敛时虚拟时间的时间导数项趋近于零, :math:`\mathbf{U}^{(m+1)} \rightarrow \mathbf{U}^{n+1}`。
迭代的最终收敛值与虚拟时间项无关。
这种引入虚拟时间计算非定常流动的方法称为双时间步方法
(dual time stepping, 或 pseudo time sub-iteration :math:`\tau`-TS)。

式 :eq:`implicit-dual-step` 中计算 :math:`\mathbf{U}^{(m+1)}` 时仍需求解非线性方程组。
因此，对方程右端项进行线性化:

.. math::
    \mathbf{R}(\mathbf{U}^{(m+1)}) \cong 
    \mathbf{R}(\mathbf{U}^{(m)}) + \left[ \frac{\partial \mathbf{R}}{\partial \mathbf{U}} \right]^{(m)} 
    \Delta \mathbf{U}^{(m)}
    :label: linearized-r

.. important::
    对方程右端项的线性化，其梯度为 :math:`(m)` 时刻的取值。

    残差 (residual) :math:`\mathbf{R}(\mathbf{U}^{(m)})`
    的计算则与显式时间推进中的处理方法相同 (式 :eq:`euler-1d-c-discrete`)。 

将 :math:`-(1+\phi)\mathbf{U}^{(m)}/(J \Delta t)` 加到式 :eq:`implicit-dual-step` 两端。
并将 :math:`\left[ \frac{\partial \mathbf{R}}{\partial \mathbf{U}} \right]`
展开为 :math:`\xi, \eta, \zeta` 方向上的差分，记 :math:`\delta_\xi, \delta_\eta, \delta_\zeta` 
为 :math:`\xi, \eta, \zeta` 方向的差分算子，空间半离散格式在这里进行体现。 

.. math::
    \left[
    \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) I 
    + \delta_\xi A^{(m)} + \delta_\eta B^{(m)} + \delta_\zeta C^{(m)}
    \right] \Delta \mathbf{U}^{(m)} = \\
    \frac{\phi \Delta \mathbf{U}^{n-1}}{J \Delta t} -
    \frac{ (1+\phi)( \mathbf{U}^{(m)}-\mathbf{U}^{n} ) }{J \Delta t} +
    \mathbf{R}(\mathbf{U}^{(m)})
    :label: implicit-dual-step-eqn

其中,

.. math::
    \begin{array} {l}
    \Delta \mathbf{U}^{(m)} = \mathbf{U}^{(m+1)} - \mathbf{U}^{(m)}, 
    &A = \frac{\partial (\hat{\mathbf{F}} - \hat{\mathbf{F}}_v )}{\partial \mathbf{U}} \\
     B = \frac{\partial (\hat{\mathbf{G}} - \hat{\mathbf{G}}_v )}{\partial \mathbf{U}},
    &C = \frac{\partial (\hat{\mathbf{H}} - \hat{\mathbf{H}}_v )}{\partial \mathbf{U}}
    \end{array}
    :label: implicit-dual-step-matrix

:math:`\Delta \tau` 由 :math:`\text{CFL}_{\tau}` 和当地 :math:`\mathbf{U}` 计算得到, 
内迭代直到 :math:`\Delta \mathbf{U}^{(m)}` 趋近于零，进入下一物理时间步
(物理时间步需要全局统一)。


.. important::
    将 :math:`\Delta \mathbf{U}^{(m)}` 看作未知量，式 :eq:`implicit-dual-step-eqn` 
    中左端方括号内的方阵，就是隐式时间推进 :eq:`implicit-method` 的线性方程组形式
    :math:`[A] \Delta\mathbf{U}^{(m)}=\mathbf{b}^{(m)}` 中的 :math:`[A]`。
    因此，方程组的解在零附近。


在计算定常流动时，式 :eq:`implicit-time-phi` 只在 :math:`(m)` 上迭代，
其中, :math:`(m)` 是子迭代步数。

.. math::
    \frac{(1+\phi)(\mathbf{U}^{(m+1)}-\mathbf{U}^n) 
    - \phi(\mathbf{U}^n-\mathbf{U}^{n-1})}{J \Delta t} =
    \mathbf{R}(\mathbf{U}^{(m+1)})
    :label: implicit-steady


(2) 时间步长与修正
---------------------------------

在进行内迭代 (或定常问题) 时，一般采用局部时间步长，
即每个网格采用当地稳定性允许的最大时间步长，全场可以不同。
这样求解的中间过程虽无真实物理意义，但最终的收敛结果是我们期望得到的解。

.. math::
    \Delta \tau = \text{CFL}/
    (|\nabla \xi|t_1 + |\nabla \eta|t_2 + |\nabla \zeta|t_3) \\
    t_1 = |\bar U| + a + 2|\nabla \xi|   (\mu + \mu_T) \max(\frac{4}{3}, \frac{\gamma}{Pr})
    \frac{Ma}{\rho Re_R} \\
    t_2 = |\bar V| + a + 2|\nabla \eta|  (\mu + \mu_T) \max(\frac{4}{3}, \frac{\gamma}{Pr})
    \frac{Ma}{\rho Re_R} \\
    t_3 = |\bar W| + a + 2|\nabla \zeta| (\mu + \mu_T) \max(\frac{4}{3}, \frac{\gamma}{Pr})
    \frac{Ma}{\rho Re_R}
    :label: tau-cfl

其中, :math:`\bar U = U/|\nabla \xi|, \bar V = V/|\nabla \eta|, \bar W = W/|\nabla \zeta|`,
:math:`U, V, W` 见式 :eq:`contravariant-velocities`。

梯度矩阵:

.. math::
    M = \left[\begin{array} {c}
    \frac{\partial \rho}{\partial \rho}  & ... & \frac{\partial \rho}{\partial p} \\
    \vdots & \ddots & \vdots \\
    \frac{\partial \rho E}{\partial \rho} & ... & \frac{\partial \rho E}{\partial p}
    \end{array}\right] = 
    \left[\begin{array} {c}
    1 & 0 & 0 & 0 & 0 \\
    u & \rho & 0 & 0 & 0 \\
    v & 0 & \rho & 0 & 0 \\
    w & 0 & 0 & \rho & 0 \\
    V^2/2 & \rho u & \rho v & \rho w & 1/(\gamma-1)
    \end{array}\right]
    :label: matrix-m

.. math::
    M^{-1} = \left[\begin{array} {c}
    1 & 0 & 0 & 0 & 0 \\
    -u/\rho & 1/\rho & 0 & 0 & 0 \\
    -v/\rho & 0 & 1/\rho & 0 & 0 \\
    -w/\rho & 0 & 0 & 1/\rho & 0 \\
    (\gamma-1)V^2/2 & -u(\gamma-1) & -v(\gamma-1) & -w(\gamma-1) & 1
    \end{array}\right]
    :label: matrix-inv-m

空间差分项 :math:`\delta_\xi, \delta_\eta, \delta_\zeta`:

以结构网格为例 (网格中心 :math:`i`, 网格界面 :math:`i-1/2, i+1/2`)

.. math::
    \delta_\xi \hat{\mathbf{F}}_i = \hat{\mathbf{F}}_{i+1/2} - \hat{\mathbf{F}}_{i-1/2} \\
    \delta_\xi (A \Delta \mathbf{U})_i = (A \Delta \mathbf{U})_{i+1/2} - (A \Delta \mathbf{U})_{i-1/2}
    :label: spatial-difference

为了保证 :math:`p, \rho` 为正数, 需要进行以下修正:

.. math::
    p^{n+1} = p^n + \Delta p \left[
        1+\phi_c \left( \alpha_c + |\Delta p/p^n| \right) \right]^{-1}, 
    \text{when } \Delta p/p^n \le \alpha_c
    :label:  thermodynamic-variable-correction

其中, :math:`\alpha = -0.2, \phi_c = 2.0`。

.. note::
    In the limit of :math:`\Delta p/p^n \rightarrow - \infty`, :math:`p^{n+1} \rightarrow p^n/2`.
    This modification improves the robustness of the method by allowing it to proceed through 
    local transients encountered during the convergence process which would otherwise terminate 
    the calculation.


(3) 空间导数项的处理
---------------------------------

式 :eq:`implicit-dual-step-eqn` 和 :eq:`implicit-steady` 中的空间差分算子代表了空间导数项。

以 :math:`\xi` 方向为例, 有限体积格式的无粘通量导数：

.. math::
    \delta_\xi \hat{\mathbf{F}}_i = \hat{\mathbf{F}}_{i+1/2} - \hat{\mathbf{F}}_{i-1/2}
    :label: spatial-derivative-xi

其中，需要对界面的左右值进行重构。

若采用矢通量分裂方法 (flux-vector splitting, FVS):

.. math::
    \delta_\xi \hat{\mathbf{F}}_i = 
    \left( \delta_\xi^{-} \hat{\mathbf{F}}^{+} + \delta_\xi^{+} \hat{\mathbf{F}}^{-} \right)_i =
    \left[\hat{\mathbf{F}}_L^{+} + \hat{\mathbf{F}}_R^{-} \right]_{i+1/2} - 
    \left[\hat{\mathbf{F}}_L^{+} + \hat{\mathbf{F}}_R^{-} \right]_{i-1/2}
    :label: spatial-derivative-xi-fvs


若采用通量微分分裂方法 (flux-difference splitting, FDS), 如 ROE 格式, 参见式 :eq:`roe-flux-1`:

.. math::
    \delta_\xi \hat{\mathbf{F}}_i = 
    \left[\frac{1}{2}(\hat{\mathbf{F}}_L+\hat{\mathbf{F}}_R) -
    \frac{1}{2} |\tilde A| (\hat{\mathbf{F}}_R-\hat{\mathbf{F}}_L)\right]_{i+1/2} \\
    -\left[\frac{1}{2}(\hat{\mathbf{F}}_L+\hat{\mathbf{F}}_R) -
    \frac{1}{2} |\tilde A| (\hat{\mathbf{F}}_R-\hat{\mathbf{F}}_L)\right]_{i-1/2}
    :label: spatial-derivative-xi-roe


通用坐标系下的无量纲三维非定常可压缩 NS 方程组 (:eq:`rans-eqn-general`) 
的详细处理方法，见后续章节。


(4) 原始变量形式
---------------------------------

非定常流动中，可以对式 :eq:`implicit-dual-step-eqn` 进行近似分解并写为原始变量形式
(approximately factored and written in primitive variable form),
然后在不同方向上分别扫描推进 (it is solved as a series of sweeps in each coordinate direction)。

.. math::
    \left[ \left(\frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) M + \delta_\xi A^* \right] 
    \Delta \mathbf{q}' = \\ 
    \frac{\phi}{J \Delta t} M \Delta \mathbf{q}^{n-1} -
    \frac{1+\phi}{J \Delta t} M(\mathbf{q}^{(m)}-\mathbf{q}^{n}) + \mathbf{R}(\mathbf{q}^{(m)}) \\
    \\
    \left[ \left(\frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) M + \delta_\eta B^* \right] 
    \Delta \mathbf{q}'' = \\ 
    \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) M \Delta \mathbf{q}' \\
    \\
    \left[ \left(\frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) M + \delta_\zeta C^* \right] 
    \Delta \mathbf{q}^{(m)} = \\ 
    \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) M \Delta \mathbf{q}'' \\
    \\
    \Delta \mathbf{q}^{(m)} = \mathbf{q}^{(m+1)} - \mathbf{q}^{(m)}
    :label: implicit-sweep-tau

其中, :math:`\mathbf{q} = [\rho, u, v, w, p]^T`, 

.. math::
    \begin{array} {l}
    M = \frac{\partial \mathbf{U}} {\partial \mathbf{q}},
    &A^* = \frac{\partial (\hat{\mathbf{F}} - \hat{\mathbf{F}}_v )}{\partial \mathbf{q}} = A M \\
     B^* = \frac{\partial (\hat{\mathbf{G}} - \hat{\mathbf{G}}_v )}{\partial \mathbf{q}} = B M,
    &C^* = \frac{\partial (\hat{\mathbf{H}} - \hat{\mathbf{H}}_v )}{\partial \mathbf{q}} = C M
    \end{array}
    :label: implicit-primitive-matrix

.. note::
    The CFL3D code is advanced in time with an implicit approximate-factorization
    method. The implicit derivatives are written as spatially first-order accurate, which results
    in block-tridiagonal inversions for each sweep. However, for solutions that utilize FDS the
    block-tridiagonal inversions are usually further simplified with a diagonal algorithm (with
    a spectral radius scaling of the viscous terms).


(5) 直接求解的困难
---------------------------------

以一维 Euler 方程为例, 
非定常流动的时间推进方程 (:eq:`implicit-dual-step-eqn`) 可写作:

.. math::
    \left[
    \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) I + \delta_x A^{(m)} \right]
    \Delta \mathbf{U}^{(m)} = \\
    \frac{\phi \Delta \mathbf{U}^{n-1}}{J \Delta t} -
    \frac{ (1+\phi)( \mathbf{U}^{(m)}-\mathbf{U}^{n} ) }{J \Delta t} +
    \mathbf{R}(\mathbf{U}^{(m)})
    :label: implicit-dual-step-eqn-1d

隐式格式 :eq:`implicit-method` 中的 :math:`f` 体现在 :math:`\delta_x A^{(m)}` 上，
:math:`A` 见式 :eq:`euler-1d-matrix-a`。

式 :eq:`implicit-dual-step-eqn-1d` 可以写为线性方程组形式 
:math:`[A]\mathbf{u}=\mathbf{b}`。其中，

.. math::
    \mathbf{u} = \left[ \rho_0, \rho_0 u_0, \rho_0 E_0, \cdots, 
    \rho_{n-1}, \rho_{n-1} u_{n-1}, \rho_{n-1} E_{n-1} \right]^T
    :label: implicit-euler-1d-u

即, :math:`\mathbf{u}` 是由各个网格的守恒变量拼接而成的长度为 :math:`3n` 的一维列向量。
相应地, :math:`\mathbf{b}` 是一个长度为 :math:`3n` 的一维列向量 (:math:`i = 0, \cdots, n-1`)。

.. math::
    \mathbf{b}[3i:3i+2] =
    \frac{\phi \Delta \mathbf{U}^{n-1}_i}{J \Delta t} -
    \frac{ (1+\phi)( \mathbf{U}^{(m)}_i-\mathbf{U}^{n}_i ) }{J \Delta t} +
    \mathbf{R}(\mathbf{U}^{(m)}_i)
    :label: implicit-euler-1d-b

:math:`[A]` 是大小为 :math:`3n \times 3n` 的对角分块方阵，每一个块大小为 :math:`3 \times 3`。 
每一块行有若干个非零块, 数量取决于重构的模板点数量。以下为 :math:`[A]` 的示意形式。

.. math::
    [A] = \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) I_{3n} + [\delta_x A^{(m)}]
    :label: implicit-euler-1d-a

那么，写出 :math:`x` 方向的净通量矩阵 :math:`[\delta_x A^{(m)}]` 的关键在于将以上空间半离散格式写为矩阵形式。


根据空间半离散形式 :eq:`euler-1d-c-discrete`, ROE 格式 :eq:`roe-flux-1` 和 
:math:`\mathbf{F} = A \mathbf{U}` (:eq:`inviscid-flux-au`),

如果采用零阶重构, 
式 :eq:`spatial-derivative-xi` 写作: 

.. math::
    \begin{array}{l}
    [\delta_x A^{(m)}] \mathbf{U} \\
    = \left[\frac{1}{2}(\mathbf{A}_{i}^{(m)}\mathbf{U}_{i}+\mathbf{A}_{i+1}^{(m)}\mathbf{U}_{i+1}) -
    \frac{1}{2} |\tilde{A}^{(m)}_{i+1/2}| 
    (\mathbf{A}_{i+1}^{(m)}\mathbf{U}_{i+1}-\mathbf{A}_{i}^{(m)}\mathbf{U}_{i})\right] \\
    -\left[\frac{1}{2}(\mathbf{A}_{i-1}^{(m)}\mathbf{U}_{i-1}+\mathbf{A}_{i}^{(m)}\mathbf{U}_{i}) -
    \frac{1}{2} |\tilde{A}^{(m)}_{i-1/2}| 
    (\mathbf{A}_{i}^{(m)}\mathbf{U}_{i}-\mathbf{A}_{i-1}^{(m)}\mathbf{U}_{i-1})\right]
    \end{array}
    :label: spatial-derivative-x-euler

则 :math:`[\delta_x A^{(m)}]` 是一个三对角块矩阵。如果采用一阶重构，则是一个五对角块矩阵。

可以看出，:math:`[A]` 矩阵非常巨大, 即便是稀疏矩阵，其维度也很高。而且，式 :eq:`spatial-derivative-x-euler`
中并不方便使用 TVD 格式等复杂的格式, 显式时间推进中的很多方法难以运用。









