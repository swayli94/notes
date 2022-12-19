高分辨率格式
=================================


(1) 抑制间断附近的数值振荡
---------------------------------

二阶以上的 FDM 或 FVM 在间断附近的解可能会出现数值振荡，
而一阶精度的格式通常会把激波、接触间断等 "抹平"。
数值振荡是由于单调性的丧失， **保单调性** 可以抑制间断附近的振荡。

一阶迎风格式和 Lax 格式是线性单调格式，因此不会出现数值振荡。
根据 **Godunov定理** : 线性单调格式最多能达到一阶精度。
因此，保单调性的二阶或二阶以上精度的高分辨率格式必定是 **非线性格式** ,
即使求解的方程是线性的。其中的一种典型 **高分辨率格式** 是 TVD 格式。

TVD (Total Variation Diminishing) 格式：
如果差分格式满足 **时间推进** 时总变差不增加，则称为 TVD 格式。
谓总变差，是衡量函数的波动状况的一种指标，在离散点上，定义为:
:math:`TV(u)=\sum_{j=-\infty}^{\infty} |u_{j+1}-u_j|`

可以证明，非线性双曲型守恒方程组（系统）的解析解本身不具备 TVD 的特点。
所以要求求解守恒方程的格式具有 TVD 的性质是不需要的，甚至是有害的。
实际上，有人已经证明，不存在求解非线性守恒系统的 TVD 格式。
所以所谓非线性守恒系统的 TVD 格式只是对标量方程TVD格式的形式上的推广。

TVD 条件是比较严的保单调条件, 不能直接用于多维问题。
可以证明，对二维、三维情况，不存在二阶及以上精度的 TVD 格式
（即使对于线性标量方程）。因此，将二阶 TVD 格式推广到多维问题，
也只是形式上的推广。

极值原理 (Maximum Principal) 是可以直接应用于多维问题抑制振荡的准则。

.. seealso::
    T.J. Barth, D. Jespersen, The design and application of upwind schemes 
    on unstructured meshes, in: Proceedings of the 27th AIAA Aerospace Sciences 
    Meeting, Reno, NV, Paper AIAA 89-0366, 1989.

TVD 格式在工程问题的计算中取得了很好的效果。但是，无论其基准格式是几阶精度，
在解的极值点处都会退化为一阶精度。因此, TVD 格式在计算多尺度流体力学问题
(如 DNS, LES, CAA等) 时耗散过大，分辨率不够。为了解决这些问题，
还须发展新的高精度、高分辨率方法。


(2) 一维 Euler 方程的 TVD 格式
---------------------------------

Euler 方程的 TVD 格式，在形式上和有限体积框架下的 Roe 格式是类似的。
主要区别在于重构界面左右端守恒变量 
:math:`\mathbf{U}_{j+1/2}^L, \mathbf{U}_{j+1/2}^R` 的算法。

(2.a) 简化算法
+++++++++++++++++++++++++++++++++

.. math:: 
   \mathbf{D}_j &= \text{min mod}
   (\mathbf{U}_{j+1}-\mathbf{U}_{j}, &\mathbf{U}_{j}-\mathbf{U}_{j-1})/\Delta x \\
   \mathbf{D}_{j+1} &= \text{min mod}
   (\mathbf{U}_{j+2}-\mathbf{U}_{j+1}, &\mathbf{U}_{j+1}-\mathbf{U}_{j})/\Delta x
   :label: tvd-roe-slope-simple

.. math:: 
   \mathbf{U}_{j+1/2}^L &= \mathbf{U}_{j} + 0.5 \mathbf{D}_j \Delta x \\
   \mathbf{U}_{j+1/2}^R &= \mathbf{U}_{j+1} - 0.5 \mathbf{D}_{j+1} \Delta x \\
   :label: tvd-roe-u-simple

其中, :math:`\text{min mod}` 算子为:

.. math::
    \text{min mod}(a,b) = 
    \left\{
        \begin{array}{l}
            \text{sign}(a) \min(|a|, |b|) &, \text{if } ab > 0 \\
            0 &, \text{otherwise}
        \end{array}
    \right.
    :label: min-mod

在 TVD 格式中, 还可使用以下算子 :math:`B(a,b)` 作为限制器。

.. math::
    B _\text{Van Leer}(a,b) = 
    \frac{ab[\text{sign}(a)+\text{sign}(b)]}{|a|+|b|+\epsilon} \\
    B _\text{Van Albada}(a,b) = 
    \frac{\max(ab,0)(a+b)}{a^2+b^2+\epsilon}
    :label: tvd-limiter

TVD 格式是一类计算激波的数值方法，限制器并不限于 :math:`\text{min mod}` 算子。

(2.b) 基于特征方向的 TVD 格式
+++++++++++++++++++++++++++++++++

完整的 TVD 格式应当根据 Riemann 问题的特征方向对
:math:`\mathbf{U}_{j+1/2}^L, \mathbf{U}_{j+1/2}^R` 进行重构，
而不是简单地施加限制器。


首先，计算 ROE 平均的特征值向量 :math:`[\tilde{\lambda}]=[\tilde{\lambda}_1,\tilde{\lambda}_2,\tilde{\lambda}_3]^T` 
(:eq:`euler-1d-eigenvalue`)
和特征向量矩阵 :math:`\tilde{R}, \tilde{L}` (:eq:`euler-1d-eigen-r`, :eq:`euler-1d-eigen-l`)。

之后，计算特征变量的梯度向量：

.. math:: 
   \mathbf{D}_j &= \text{min mod}
   (\tilde{L}(\mathbf{U}_{j+1}-\mathbf{U}_{j}), 
   &\tilde{L}(\mathbf{U}_{j}-\mathbf{U}_{j-1}))/\Delta x \\
   \mathbf{D}_{j+1} &= \text{min mod}
   (\tilde{L}(\mathbf{U}_{j+2}-\mathbf{U}_{j+1}), 
   &\tilde{L}(\mathbf{U}_{j+1}-\mathbf{U}_{j}))/\Delta x
   :label: tvd-roe-slope

再计算 Riemann 问题的左右状态向量 (:eq:`euler-1d-feature`):

.. math:: 
   \mathbf{W}^L &= 
   \tilde{L}\mathbf{U}_{j}   + \frac{1}{2}(\mathbf{D}_j\Delta x 
   - \mathbf{D}_j \odot [\tilde{\lambda}] \Delta t) \\
   \mathbf{W}^R &=
   \tilde{L}\mathbf{U}_{j+1} - \frac{1}{2}(\mathbf{D}_{j+1}\Delta x 
   + \mathbf{D}_{j+1} \odot [\tilde{\lambda}] \Delta t)
   :label: tvd-roe-lr

其中, :math:`\odot` 是哈达马积 (Hadamard product), 指两个维度相同矩阵对应位置相乘。
是 Kronecker 积 (直积, 张量积) :math:`\otimes` 在两矩阵维度相同时的简化形式。

最后，计算左右守恒向量:

.. math:: 
   \mathbf{U}_{j+1/2}^L &= \tilde{R} \mathbf{W}^L \\
   \mathbf{U}_{j+1/2}^R &= \tilde{R} \mathbf{W}^R \\
   :label: tvd-roe-u

原则上，可用任意时间离散格式，但 Shu-Osher 证明了如果用 TVD Runge-Kutta 
格式 (:eq:`rk-3-tvd`) 进行时间离散，得到的全离散格式也具有 TVD 性质。


以下为 TVD 格式通量在一维 Euler 问题中的实现，为了更清晰，代码的实现不考虑效率。

.. include:: codes/euler1d.py
   :literal:
   :start-line: 213
   :end-line: 275


(3) MUSCL 格式
---------------------------------

`MUSCL 格式 <https://en.wikipedia.org/wiki/MUSCL_scheme>`_
即 Monotonic Upstream-centered Scheme for Conservation Laws, (van Leer, 1979)。

.. seealso::
   GPL Euler equation solver: https://github.com/Azrael3000/gees


