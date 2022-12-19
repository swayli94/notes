隐式 LU-SGS 时间推进格式
=================================


(1) 方法简介
---------------------------------

LU-SGS 方法是一种迭代求解算法，意为三角分解-对称 Gauss-Seidel 迭代方法
(A lower-upper factorization and a symmetric Gauss-Seidel relaxation scheme)。

式 :eq:`implicit-dual-step-eqn` 和 :eq:`implicit-steady`  在全场联立后，
三维结构网格 (网格量 :math:`N \times N \times N`) 会得到一个大小为 :math:`(5N)^3` 
的对角块线性方程组 (block-banded matrix)。
每一行中非零块的宽度 (bandwidth) 大致为 :math:`B=(5N)^2`, 
那么，求解线性方程组的计算量大致为 :math:`(5N)^3 B^2`, 计算代价难以接受。

Jameson 提出的 LU-SGS 方法采用了简化的正、负特征矩阵分裂，使得构造的 :math:`L, U` 算子不包含块矩阵求逆。
算子 :math:`D` 为简单的标量矩阵求逆，因此求逆过程只是一个全场逐点扫描的过程。
只需要进行 :math:`L, U` 两次扫描：一次从左上到右下的 GS 迭代，一次相反的迭代，大大提高了计算效率。
由于迭代是两个方向对称进行的，所以称为对称 Gauss-Seidel 迭代。

LU-SGS 方法把求解对角快线性方程组的过程，简化为 **两次显式扫描过程** 。
这种方法编程比较简单，每步的计算量也较小。在计算中，
**物理时间步长** 可根据对非定常数值解时间方向精度的要求选取；
数值计算表明，物理时间步长的选取对计算过程的稳定性影响不大。
**虚拟时间步长** 理论上可以选任意值，但是数值实验表明，
在流场的初始值变化较为剧烈或光滑性不好时，选用较小的虚拟时间步长有利于计算的稳定。
在经过一定步数的计算后，虚拟时间步长可以选取较大的值，一般虚拟时间步长对应的 CFL
数为数十至数百时，计算可以收敛。非定常计算内迭代的次数，可以根据数值解是否满足条件
:math:`||\mathbf{U}^{(m+1)} - \mathbf{U}^{(m)}|| \le \Delta \tau \cdot \epsilon` 
自动确定。其中 :math:`\epsilon` 为指定的小正数。

.. note::
    求解 Euler 和 Navier-Stoke 方程的隐式方法，除了 LU-SGS 方法外, 
    还有近似隐式分解方法、点隐式方法、ADI 方法、线松弛方法 LU-SSOR 等等多种方案。
    某些显式格式，也可以通过隐式残差光滑等方法，达到隐式格式的效果。 

    大部分显式格式和隐式格式在求解定常问题（或者用双时间步方法求解非定常问题）
    时，均可采用一些加速收敛的措施。这些措施包括：局部时间步长、预处理(preconditioning)
    和多重网格 (multigrid) 方法。根据需要，这些措施可以分别或者同时采用。 


(2) 空间差分算子的处理
---------------------------------

双时间步隐式时间推进格式 (:eq:`implicit-dual-step-eqn`) 中的 :math:`\delta_\xi, \delta_\eta, \delta_\zeta` 
空间差分算子, 首先按照有限体积格式 (式 :eq:`spatial-derivative-xi`) 进行近似:

.. math::
    [\delta_\xi A] \Delta \mathbf{U} &= [A \Delta \mathbf{U}]_{i+1/2} - [A \Delta \mathbf{U}]_{i-1/2} \\
    [\delta_\xi B] \Delta \mathbf{U} &= [B \Delta \mathbf{U}]_{j+1/2} - [B \Delta \mathbf{U}]_{j-1/2} \\
    [\delta_\xi C] \Delta \mathbf{U} &= [C \Delta \mathbf{U}]_{k+1/2} - [C \Delta \mathbf{U}]_{k-1/2}
    :label: implicit-difference-operator

将粘性净通量显式处理，即式 :eq:`implicit-dual-step-matrix` 忽略粘性通量: 
:math:`A = \partial \hat{\mathbf{F}} / \partial \mathbf{U}`。
其中, :math:`\Delta \mathbf{U}` 代表 :math:`\Delta \mathbf{U}_{i,j,k}`。

对无粘净通量使用矢通量分裂方法 (:eq:`fvs-split`) 进行拆分,
将界面上的无粘通量 Jocobian 矩阵按正负特征值分裂，采用一阶迎风法则。

.. math::
    [A \Delta \mathbf{U}]_{i+1/2} &= A_{i}^{+} \Delta \mathbf{U}_{i} + A_{i+1}^{-} \Delta \mathbf{U}_{i+1} \\
    [A \Delta \mathbf{U}]_{i-1/2} &= A_{i-1}^{+} \Delta \mathbf{U}_{i-1} + A_{i}^{-} \Delta \mathbf{U}_{i}
    :label: implicit-operator-split

那么，原隐式时间推进格式 :eq:`implicit-dual-step-eqn` 变为：

.. math::
    \left[
    \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) I + \left(
      A_{i}^{+} - A_{i}^{-}
    + B_{j}^{+} - B_{j}^{-}
    + C_{k}^{+} - C_{k}^{-} \right)^{(m)} \right] \Delta \mathbf{U}^{(m)}  \\
    - \left[
        A_{i-1}^{+} \Delta \mathbf{U}^{(m)}_{i-1} + 
        B_{j-1}^{+} \Delta \mathbf{U}^{(m)}_{j-1} + 
        C_{k-1}^{+} \Delta \mathbf{U}^{(m)}_{k-1}
    \right] \\
    + \left[
        A_{i+1}^{+} \Delta \mathbf{U}^{(m)}_{i+1} + 
        B_{j+1}^{+} \Delta \mathbf{U}^{(m)}_{j+1} + 
        C_{k+1}^{+} \Delta \mathbf{U}^{(m)}_{k+1}
    \right] \\
    =
    \frac{\phi \Delta \mathbf{U}^{n-1}}{J \Delta t} -
    \frac{ (1+\phi)( \mathbf{U}^{(m)}-\mathbf{U}^{n} ) }{J \Delta t} +
    \mathbf{R}(\mathbf{U}^{(m)})
    :label: implicit-eqn-split

其中, :math:`J` (坐标转换雅可比矩阵 :eq:`jacobian-coordinates` 的模) 代表 :math:`J_{i,j,k}` 。
残差项 :math:`\mathbf{R}(\mathbf{U}^{(m)})` 见式 :eq:`residual-3d-general`,
其计算方法与显式时间推进中的处理方法相同 (式 :eq:`euler-1d-c-discrete`)。 

为了保证下面 LU 分解的 :math:`L, U` 算子在最大程度上对角占优，
应使得 :math:`+` 特征矩阵的特征值非负，:math:`-` 特征矩阵的特征值非正。
因此，采用式 :eq:`fvs-split` 中的矢通量分裂方法。

Yoon 和 Jameson 利用上述无粘通量 Jacobian 矩阵的近似分裂形式，使构造的 :math:`L, U`
算子具有最大程度的对角占优，从而得到如下形式的一种快速有效的隐式 LU-SGS 形式:

.. math::
    (L+D)D^{-1}(D+U) \Delta \mathbf{U}^{(m)} = \text{RHS}^{(m)}
    :label: lu-sgs-eqn

其中, :math:`\text{RHS}^{(m)}` 是 :eq:`implicit-eqn-split` 的右端项，为已知量。

.. math::
    L = - \left[ A_{i-1}^{+} + B_{j-1}^{+} + C_{k-1}^{+} \right]^{(m)} \\
    U = + \left[ A_{i+1}^{-} + B_{j+1}^{-} + C_{k+1}^{-} \right]^{(m)} \\
    D = \left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right) I 
    + \left( \sigma_A + \sigma_B + \sigma_C \right)
    :label: lu-sgs-matrix

其中, :math:`\sigma_A = (1+\varepsilon)|\lambda|_{\text{max}, A_i} + 2\nu_a`, 
:math:`\varepsilon \in [0,0.01]`, 稳定因子 :math:`\nu_a` (:eq:`fvs-stable-factor`) 根据具体情况添加。


(3) 时间推进步骤
---------------------------------

**L 块向前扫描运算:**

首先使用已知时间步的数据计算式 :eq:`implicit-eqn-split` 右端项 :math:`\text{RHS}`。
执行 :math:`L` 块算子运算, 进行全场逐点向前扫描得到中间预测值 :math:`\Delta \mathbf{U}^*`。

.. math::
    (L+D) \Delta \mathbf{U}^* = \text{RHS}^{(m)}
    :label: lu-sgs-eqn-l

即：

.. math::
    \Delta \mathbf{U}^* = \frac{ \text{RHS}^{(m)} + 
          (A^{+} \Delta \mathbf{U})_{i-1}^{(m)} 
        + (B^{+} \Delta \mathbf{U})_{j-1}^{(m)}
        + (C^{+} \Delta \mathbf{U})_{k-1}^{(m)} }
    {\left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right)
    + \sigma_A + \sigma_B + \sigma_C }
    :label: lu-sgs-sweep-l

**U 块向后扫描运算:**

之后，进行全场逐点向后扫描得到式 :eq:`implicit-eqn-split` 的解 :math:`\Delta \mathbf{U}^{(m)}`:

.. math::
    (D+U) \Delta \mathbf{U}^{(m)} = D \Delta \mathbf{U}^*
    :label: lu-sgs-eqn-u

即：

.. math::
    \Delta \mathbf{U}^{(m)} = \Delta \mathbf{U}^* - \frac{
          (A^{-} \Delta \mathbf{U})_{i+1}^{(m)} 
        + (B^{-} \Delta \mathbf{U})_{j+1}^{(m)}
        + (C^{-} \Delta \mathbf{U})_{k+1}^{(m)} }
    {\left( \frac{1}{J \Delta \tau} + \frac{1+\phi}{J \Delta t} \right)
    + \sigma_A + \sigma_B + \sigma_C }
    :label: lu-sgs-sweep-r

为了提高格式的鲁棒性，加快收敛速度，可对 :math:`\Delta \mathbf{U}^{(m)}` 进行一次光顺处理。



