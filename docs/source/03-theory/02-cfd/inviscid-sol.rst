无粘通量与流场间断
===========================

(1) 双曲型守恒方程中的间断
---------------------------

(1.a) 广义解
+++++++++++++++++++++++++++

通常，我们认为偏微分方程的解是连续可微的。
但是，一般的非线性双曲型守恒方程组 (:eq:`ns-eqn-c`) 的解中都有可能存在间断，
因此，必须拓展双曲型守恒律解的概念。

以一维双曲型守恒方程组为例，
引入广义解 (generalized solution) 或弱解 (weak solution) 概念来表示包含间断的解：

 设分片连续可微的函数 :math:`\mathbf{U}(x,t)`, 若任意与 :math:`\mathbf{U}` 只有有限个交点的
 光滑封闭曲线 :math:`\Gamma` 都满足 :math:`\oint (\mathbf{F} dt - \mathbf{U} dx) = 0`, 
 则称 :math:`\mathbf{U}` 是偏微分方程组在初值 
 :math:`\mathbf{U}(x,0)=\mathbf{U}_0(x)` 下的广义解。
 可以看出，在光滑区弱解就是通常的连续可微解。而在间断处，需要额外的条件来确定间断两侧的关系。

广义解推广了偏微分方程初值问题连续可微解的概念，但其后果是导致了广义解不唯一。
但是对于有明确物理意义的守恒律，其中只有一个解是有物理意义的，我们称之为 **物理解** 。
因此需要添加额外的条件来收敛到物理解，由于这个条件的作用与热力学第二定律相同，
因此被称为 "熵条件" (entropy condition)。

对于 CFD 而言，激波的两侧通过 R-H 关系相联系。


(1.b) 守恒格式和相容性
+++++++++++++++++++++++++++

守恒格式 (conservative numerical scheme) 指格式有统一且守恒形式的通量
(with consistent and conservative numerical fluxes)。
即，在相邻单元 L 和 R 的界面上，从 L 指向 R 的通量等于从 R 指向 L 通量的相反数。
注意，前者使用 L 的模板点计算，后者使用 R 的模板点计算。

**Lax-Wendroff theorem** : a conservative numerical scheme for a hyperbolic system 
of conservation laws converges, then it converges towards a weak solution.

数值通量的相容条件：假设数值通量的计算函数为 
:math:`\hat{\mathbf{F}}(\mathbf{U}_k | k= \cdots)`
(即该单元某个面的通量由若干个相应模板点计算得到), 那么, 如果满足
:math:`\hat{\mathbf{F}}(\mathbf{U}, \cdots, \mathbf{U}) = \mathbf{F}(\mathbf{U})`, 则称该数值通量有相容性。

结论: **相容的守恒格式** 具有自动捕捉激波和接触间断的能力。

Euler方程 (和其它基于物理定律的守恒方程一样) 具有旋转不变性。
因此，可以将基于一维 Riemann 问题的通量计算格式推广到高维问题中。


(2) 一维迎风型有限差分格式
----------------------------------

双曲型方程的差分格式收敛 (在Lax等价性定理满足时亦即稳定) 的必要条件
是差分格式的依赖域包含微分方程的依赖域, 即满足 CFL (Courant-Friedrichs-Lewy) 条件。

非线性双曲型方程组的的迎风格式本质上是线性格式形式上的推广。
最为常用的是 ROE 方法。

(2.a) 一维 Euler 方程
+++++++++++++++++++++++++++

一维 Euler 方程 (理想气体) 的守恒形式为：

.. math:: 
   \frac{\partial \mathbf{U}}{\partial t} + 
   \frac{\partial \mathbf{F}}{\partial x} = 0
   :label: euler-1d-c

.. math::
   U= \left[ 
      \begin{array}{c}
         \rho \\ 
         \rho u \\ 
         \rho E
      \end{array}
   \right], 
   \;\;\;\;
   F= \left[ 
      \begin{array}{c}
         \rho u \\ 
         \rho u^2 + p \\ 
         u(\rho E+p)
      \end{array}
   \right]
   :label: euler-1d-c-vec

写为拟线性形式:

.. math:: 
   \frac{\partial \mathbf{U}}{\partial t} + 
   A \frac{\partial \mathbf{U}}{\partial x} = 0
   :label: euler-1d-linear

.. math::
   A = \frac{\partial \mathbf{F}}{\partial \mathbf{U}}= \begin{bmatrix}
         0 & 1 & 0 \\ 
         (\gamma-3)\frac{u^2}{2} & (3-\gamma)u & (\gamma-1) \\ 
         (\gamma-1)u^3-\gamma u E &  -\frac{3}{2}(\gamma-1)u^2+\gamma E & \gamma u
   \end{bmatrix}
   :label: euler-1d-matrix-a

注意到 Euler 方程的通量 :math:`\mathbf{F}` 是守恒变量 :math:`\mathbf{U}` 的一次齐次函数:

.. math::
   \mathbf{F}(\alpha \mathbf{U}) = \alpha \mathbf{F}(\mathbf{U})
   :label: homogeneous-function-euler-flux

那么，有

.. math::
   \mathbf{F} = A \mathbf{U}
   :label: inviscid-flux-au

系数矩阵 :math:`A` 的特征值和特征向量是:

.. math::
   A = R \Lambda L
   :label: euler-1d-eigenstructure

.. math::
   \Lambda = \begin{bmatrix}
         u-a & 0 & 0 \\ 
         0   & u & 0 \\ 
         0   & 0 & u+a
   \end{bmatrix}
   :label: euler-1d-eigenvalue

.. math::
   R = \begin{bmatrix}
         1    & 1       & 1   \\ 
         u-a  & u       & u+a \\ 
         H-ua & 0.5 u^2 & H+ua
   \end{bmatrix}
   :label: euler-1d-eigen-r

.. math::
   L = \begin{bmatrix}
         \frac{1}{2}(\frac{\gamma-1}{2 a^2} u^2+\frac{u}{a}) & 
         -\frac{1}{2}\left(\frac{\gamma-1}{a^2}u+\frac{1}{a} \right) &
         \frac{\gamma-1}{2 a^2} \\ 
         1-\frac{\gamma-1}{2a^2}u^2 &
         \frac{\gamma-1}{a^2}u &
         -\frac{\gamma-1}{a^2} \\ 
         \frac{1}{2}(\frac{\gamma-1}{2 a^2} u^2-\frac{u}{a}) & 
         -\frac{1}{2}\left(\frac{\gamma-1}{a^2}u-\frac{1}{a} \right) &
         \frac{\gamma-1}{2 a^2}
   \end{bmatrix}
   :label: euler-1d-eigen-l

记, :math:`\Lambda_{ij} = \lambda_i \delta_{ij}`,
:math:`R = [\mathbf{v_1}, \mathbf{v_2}, \mathbf{v_3}]`。 其中, :math:`L = R^{-1}`。

对式 :eq:`euler-1d-c` 左乘 :math:`L`, 记 :math:`\mathbf{W}=L\mathbf{U}` 为特征变量, 得：

.. math:: 
   \frac{\partial \mathbf{W}}{\partial t} + 
   \Lambda \frac{\partial \mathbf{W}}{\partial x} = 0
   :label: euler-1d-feature

形式上类似于线性波动方程组，适用于迎风格式。


(2.b) 通量微分分裂方法: ROE 格式
+++++++++++++++++++++++++++++++++

.. seealso::

   `Prof. Daniel J. Bodony, Roe's Approximate Riemann Solver, 2018
   <http://acoustics.ae.illinois.edu/pdfs/ae410_spring_2018_roe_scheme_notes.pdf>`_

   `Roe P.L., Approximate Riemann solvers, parameter vectors, and difference schemes,
   Journal of Computational Physics, 43(2), 1981,
   <https://www.sciencedirect.com/science/article/pii/0021999181901285>`_

式 :eq:`euler-1d-c` 的守恒型差分格式为：

.. math:: 
   \frac{\partial \mathbf{U}_j}{\partial t} + 
   \frac{\tilde{\mathbf{F}}_{j+1/2} - \tilde{\mathbf{F}}_{j-1/2}}{\Delta x} = 0
   :label: euler-1d-c-discrete

其中, :math:`\tilde{\mathbf{F}}_{j+1/2}` 由 :math:`\mathbf{U}_k (k=\cdots)` 计算得到。

一阶 Roe 格式通量:

.. math:: 
   \tilde{\mathbf{F}}_{j+1/2} = \frac{1}{2}(\mathbf{F}_j+\mathbf{F}_{j+1}) -
   \frac{1}{2} |\tilde A|_{j+1/2} (\mathbf{F}_{j+1}-\mathbf{F}_j)
   :label: roe-flux-1

其中, :math:`|\tilde A|=\tilde R |\tilde \Lambda| \tilde L`, 
:math:`|\tilde \Lambda| = \text{sign}(\tilde \lambda_i)\delta_{ij}`。

.. math:: 
   \text{sign}(a) = \left\{
      \begin{array}{l}
         -1 &, a<0 \\
         0  &, a=0 \\
         1  &, a>0 \\
      \end{array}
   \right.
   :label: sign

将 :math:`\mathbf{U}` 分解为特征振幅 
:math:`\mathbf{U}_j=\sum_p^3 \beta_p \mathbf{v}_p`。
那么, 界面处的守恒变量变化 (jump)为:

.. math:: 
   \mathbf{U}_{j+1}-\mathbf{U}_j = 
   \sum_p^3 (\beta_{i+1,p}-\beta_{j,p}) \tilde{\mathbf{v}}_p
   \doteq \sum_{p=1}^3 \alpha_{p} \tilde{\mathbf{v}}_p
   :label: roe-jump

其中,

.. math:: 
   \begin{array}{l}
      \alpha_1 = \frac{1}{2 \tilde{a}^2} (\Delta p - \tilde a \tilde \rho \Delta u) \\
      \alpha_2 = \Delta \rho - \frac{1}{\tilde{a}^2} \Delta p \\
      \alpha_3 = \frac{1}{2 \tilde{a}^2} (\Delta p + \tilde a \tilde \rho \Delta u) \\
      \Delta \rho = \rho_R - \rho_L,
      \Delta p = p_R - p_L,
      \Delta u = u_R - u_L
   \end{array}
   :label: euler-alpha

界面处的守恒变量 :math:`\tilde{\mathbf{U}}_{j+1/2}` 由左右状态
:math:`\mathbf{U}_L = \mathbf{U}_{j}, \mathbf{U}_R = \mathbf{U}_{j+1}` 
平均得到 (Roe 平均):

.. math::
   & \left\{
      \begin{array}{l}
         \tilde \rho &= \sqrt{\rho_L \rho_R} \\
         \tilde u &= (\sqrt{\rho_L} u_L+\sqrt{\rho_R} u_R)/
         (\sqrt{\rho_L}+\sqrt{\rho_R}) \\
         \tilde H &= (\sqrt{\rho_L}H_L+\sqrt{\rho_R}H_R)/
         (\sqrt{\rho_L}+\sqrt{\rho_R}) \\
         \tilde a^2 &= (\gamma-1)\left(\tilde H - \tilde u^2/2 \right)
      \end{array}
   \right.
   :label: roe-average


根据线性 Reimann 问题的信息传播方向, 界面处的解为:

.. math:: 
   \mathbf{U}_{j+1/2} &= 
   \frac{1}{2} \left[\mathbf{U}_{j} + \sum_{\lambda_p<0} \alpha_{p} 
   \tilde{\mathbf{v}}_p \right] +
   \frac{1}{2} \left[\mathbf{U}_{j+1} - \sum_{\lambda_p>0} \alpha_{p} 
   \tilde{\mathbf{v}}_p \right] \\
   &= \frac{\mathbf{U}_{j}+\mathbf{U}_{j+1}}{2} + \frac{1}{2}
   \left[\sum_{\lambda_p<0}-\sum_{\lambda_p>0}\right] \alpha_{p} 
   \tilde{\mathbf{v}}_p 
   :label: roe-jump-sol

那么, 根据 :math:`\tilde A \tilde{\mathbf{v}}_p = \tilde{\lambda}_p \tilde{\mathbf{v}}_p`,
式 :eq:`roe-flux-1` 得

.. math:: 
   \tilde{\mathbf{F}}_{j+1/2} = \frac{1}{2}(\mathbf{F}_L+\mathbf{F}_{R}) -
   \frac{1}{2} \sum_{p=1}^3 |\tilde{\lambda}_p| \alpha_p \tilde{\mathbf{v}}_p 
   :label: roe-flux-1-vec

**熵修正** : 经验上, 速度 :math:`u \approx a` 时 Roe solver 会给出错误答案,
这是因为线性化在此时违背了热力学第二定律。因此, 当
:math:`|\tilde{\lambda}_p| < \epsilon \; (p=1,3)` 时，对特征值进行修正:

.. math:: 
   \tilde{\lambda}_p \rightarrow \frac{1}{2}
   \left(\frac{\tilde{\lambda}^2_p}{\epsilon}+\epsilon \right), \epsilon \ll 1
   :label: roe-entropy-fix

以下为 ROE 格式通量在一维 Euler 问题中的实现，为了更清晰，代码的实现不考虑效率。

.. include:: codes/euler1d.py
   :literal:
   :start-line: 93
   :end-line: 178


(2.c) 矢通量分裂方法
+++++++++++++++++++++++++++

矢通量分裂方法 (flux vector splitting, FVS) 最早由 Steger-Warming 提出。
将通量按特征值分解为

.. math::
   \begin{array}{l}
   &\mathbf{F}^{+} = A^{+} \mathbf{U}, 
   &\mathbf{F}^{-} = A^{-} \mathbf{U} \\
   &\mathbf{A}^{+} = 0.5(A+|\lambda|_{\text{max}} I) + \nu_aI, 
   &\mathbf{A}^{-} = 0.5(A-|\lambda|_{\text{max}} I) + \nu_aI
   \end{array}
   :label: fvs-split

其中，:math:`|\lambda|_{\text{max}}` 为特征值绝对值的最大值
(可以在该项前面乘上一个系数如 1.01 来确保分解后的矩阵特征值非负/非正)。
:math:`\nu_a` 是针对物面法向的人工稳定因子，是为了弥补不能对角化的物面法向上粘性项的影响，
以增加数值计算的稳定性，仅在壁面附近的物面法向添加
(:math:`\hat{l}_{\text{cell}}` 是网格空间尺度，如物面法向方向的长度)。

.. math::
   \nu_a = \frac{2 \, \mu \, \hat{l}^2_{\text{cell}}}{\rho \, Re}
   :label: fvs-stable-factor

所以，式 :eq:`euler-1d-c-discrete` 中的数值通量为：

.. math::
   \tilde{\mathbf{F}}_{j+1/2} = \mathbf{F}^{+}_{j} + \mathbf{F}^{-}_{j+1} \\
   \tilde{\mathbf{F}}_{j-1/2} = \mathbf{F}^{+}_{j-1} + \mathbf{F}^{-}_{j} \\
   :label: fvs-flux

也就是说，考虑到波的传播方向，界面 :math:`j+1/2` 左侧的 :math:`\mathbf{F}^{+}_{j}`
和右侧的 :math:`\mathbf{F}^{-}_{j+1}` 对界面的数值通量都有贡献。

与 ROE 格式的区别: ROE 取 :math:`j+1/2` 处的特征结构, FVS 通量分裂逐点进行。

注意到，如果通量 :math:`\mathbf{F}` 不是守恒变量 :math:`\mathbf{U}` 的一次齐次函数，
则不能构造相应的 FVS 方法。另外，通量分裂的方法不是唯一的。


(3) 一维迎风型有限体积格式
----------------------------------

记网格单元的体积平均 
:math:`\bar{\mathbf{U}}_j = \int_{x_{j-1/2}}^{x_{j+1/2}} {\mathbf{U}(x)} dx` 仍为
:math:`\mathbf{U}_j`, 即 :eq:`euler-1d-c-discrete` 形式不变。

首先对 :math:`\mathbf{U}(x)` 进行重构，从而获得界面上的值。
以一阶重构 (空间二阶精度) 为例, 界面 :math:`j+1/2` 的左右端值为:

.. math::
   \mathbf{U}_{j+1/2}^L &= 1.5 \mathbf{U}_{j} - 0.5 \mathbf{U}_{j-1} \\
   \mathbf{U}_{j+1/2}^R &= 1.5 \mathbf{U}_{j+1} - 0.5 \mathbf{U}_{j+2} \\
   :label: reconstruction-linear

那么, :math:`\tilde{\mathbf{F}}_{j+1/2}` 的计算按照式 :eq:`roe-flux-1-vec` 进行。
当然，在存在间断的流场中，直接使用一阶重构经常会出现数值发散 (密度或压力在重构时变为负数) 的情况。
因此，通常需要引入限制器或高分辨率格式。

