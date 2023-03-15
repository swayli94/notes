# 高等计算流体力学第四章作业

## Problem 1

首先写出一维N-S方程的形式：
$$
\frac{\partial \mathbf{Q}}{\partial t}+\frac{\partial \mathbf{F}}{\partial x}=0, ~\mathbf{Q}=
\begin{pmatrix}
\rho\\
\rho u\\
\rho E
\end{pmatrix}, ~
\mathbf{F}=
\begin{pmatrix}
\rho u\\
\rho u^2 + p\\
(\rho E + p)u
\end{pmatrix}
$$
注意其中$E$和其他变量的关系：
$$
E=\frac{1}{2}u^2+\frac{1}{\gamma-1}\frac{p}{\rho}
$$
令$\mathbf{Q}$为：
$$
\mathbf{Q}=
\begin{pmatrix}
\rho\\
\rho u\\
\rho E
\end{pmatrix}=
\begin{pmatrix}
Q_1\\Q_2\\Q_3
\end{pmatrix}
$$
那么$p$就可以写成：
$$
p=(\rho E - \frac{1}{2}\rho u^2)(\gamma-1)=(Q_3-\frac{1}{2}\frac{Q_2^2}{Q_1})(\gamma-1)
$$
于是$\mathbf{F}$可以写为：
$$
\mathbf{F}=\begin{pmatrix}
Q_2\\
(\gamma-1)Q_3+\frac{3-\gamma}{2}\frac{Q_2^2}{Q_1}\\
(\gamma Q_3-\frac{\gamma-1}{2}\frac{Q_2^2}{Q_1})\frac{Q_2}{Q_1}
\end{pmatrix}
$$
于是可以写出雅可比矩阵$\frac{\partial \mathbf{F}}{\partial \mathbf{Q}}$:
$$
\frac{\partial \mathbf{F}}{\partial \mathbf{Q}}=\begin{pmatrix}
0&1&0\\
-\frac{3-\gamma}{2}(\frac{Q_2}{Q_1})^2& (3-\gamma)\frac{Q_2}{Q_1}&\gamma-1\\
-\frac{\gamma Q_3Q_2}{Q_1^2}+(\gamma-1)\frac{Q_2^3}{Q_1^3} &
-\frac{3(\gamma-1)}{2}\frac{Q_2^2}{Q_1^2}+\gamma\frac{Q_3}{Q_1}&
\gamma\frac{Q_2}{Q_1}
\end{pmatrix}
$$
写成$(\rho, u, E)$的表达式：
$$
\frac{\partial \mathbf{F}}{\partial \mathbf{Q}}=\begin{pmatrix}
0&1&0\\
-\frac{3-\gamma}{2}u^2& (3-\gamma)u& \gamma-1\\
-\gamma uE+(\gamma-1)u^3&
-\frac{3(\gamma-1)}{2}u^2+\gamma E&
\gamma u
\end{pmatrix}
$$
利用$E$和$p, u$的关系进一步化简：
$$
E=\frac{1}{2}u^2+\frac{1}{\gamma-1}\frac{p}{\rho}
$$

$$
\frac{\partial \mathbf{F}}{\partial \mathbf{Q}}=\begin{pmatrix}
0&1&0\\
-\frac{3-\gamma}{2}u^2& (3-\gamma)u& \gamma-1\\
(\frac{\gamma}{2}-1)u^3-\frac{\gamma u}{\gamma -1}\frac{p}{\rho}&
(-\gamma +\frac{3}{2})u^2+\frac{\gamma}{\gamma - 1}\frac{p}{\rho}&
\gamma u
\end{pmatrix}
$$

 如果我们令$H=E+\frac{p}{\rho}$，则雅可比矩阵可以写为：
$$
\frac{\partial \mathbf{F}}{\partial \mathbf{Q}}=\begin{pmatrix}
0&1&0\\
-\frac{3-\gamma}{2}u^2& (3-\gamma)u& \gamma-1\\
-uH+\frac{\gamma - 1}{2}u^3&
H - (\gamma -1)u^2&
\gamma u
\end{pmatrix}
$$
事实上，可以验证，$\mathbf{F}$是$\mathbf{Q}$的一次齐次函数，因而下述关系成立：
$$
\mathbf{F}=\mathbf{A}\cdot\mathbf{Q}=\frac{\partial\mathbf{F}}{\partial \mathbf{Q}}\cdot\mathbf{Q}
$$

## Problem 2

首先写出Roe格式在均匀网格下的形式：
$$
\hat{\mathbf{F}}_{i+\frac{1}{2}}=\frac{1}{2}(\mathbf{F}_R+\mathbf{F}_L)-\frac{1}{2}\mathbf{R}\left |\mathbf{\Lambda}\right |\mathbf{R}^{-1}(\mathbf{Q}_R-\mathbf{Q}_L)
$$
根据第一题的推导，我们可以求出雅可比矩阵$\mathbf{A}=\partial \mathbf{F}/\partial \mathbf{Q}$的特征值分解：
$$
\mathbf{A}=\mathbf{R}\mathbf{\Lambda}\mathbf{R}^{-1}
$$
其中：
$$
\mathbf{\Lambda} = \begin{pmatrix}
u-c &0 &0\\
0 & u & 0\\
0 & 0 & u+c
\end{pmatrix}, ~\mathbf{R}=\begin{pmatrix}
1&1&1\\
u-c&u&u+c\\
H-uc& u^2/2&H+uc
\end{pmatrix}
$$

$$
\mathbf{R}^{-1}=\begin{pmatrix}
\frac{u}{4c}(2+(\gamma - 1)\frac{u}{c})&-\frac{1}{2c}(1+(\gamma-1)\frac{u}{c})&\frac{\gamma - 1}{2}\frac{1}{c^2}\\
1-\frac{\gamma - 1}{2}(\frac{u}{c})^2& (\gamma-1)\frac{u}{c^2}&-(\gamma-1)\frac{1}{c^2}\\
-\frac{u}{4c}(2-(\gamma-1)\frac{u}{c})& -\frac{1}{2c}(1-(\gamma-1)\frac{u}{c})&\frac{\gamma-1}{2}\frac{1}{c^2}
\end{pmatrix}
$$

于是，如果令$\delta_\rho = \rho_R-\rho_L, \delta_u = u_R-u_L, \delta_p = p_R- p_L$，那么$\mathbf{R}^{-1}(\mathbf{Q}_R-\mathbf{Q}_L)$可以写为：
$$
\mathbf{R}^{-1}(\mathbf{Q}_R-\mathbf{Q}_L)=\begin{pmatrix}
\frac{1}{2c^2}(\delta_p-c\rho \delta_u)\\
\delta_{\rho}-\frac{1}{c^2}\delta_p\\
\frac{1}{2c^2}(\delta_p+c\rho \delta_u)
\end{pmatrix}
$$
我们用$\hat{\cdot}$代表Roe平均的量，那么有(马赫数大于1，且不妨假设$\hat{u}>0$)：
$$
\begin{align}
\mathbf{D}&=\frac{1}{2}\begin{pmatrix}
1&1&1\\
\hat{u}-\hat{c}&\hat{u}&\hat{u}+\hat{c}\\
\hat{H}-\hat{u}\hat{c}& \hat{u}^2/2&\hat{H}+\hat{u}\hat{c}
\end{pmatrix}
\begin{pmatrix}
\hat{u}-\hat{c} &0 &0\\
0 & \hat{u} & 0\\
0 & 0 & \hat{u}+\hat{c}
\end{pmatrix}
\begin{pmatrix}
\frac{1}{2c^2}(\delta_p-c\rho \delta_u)\\
\delta_{\rho}-\frac{1}{c^2}\delta_p\\
\frac{1}{2c^2}(\delta_p+c\rho \delta_u)
\end{pmatrix}\\
&=\frac{1}{2}\begin{pmatrix}
1&1&1\\
\hat{u}-\hat{c}&\hat{u}&\hat{u}+\hat{c}\\
\hat{H}-\hat{u}\hat{c}& \hat{u}^2/2&\hat{H}+\hat{u}\hat{c}
\end{pmatrix}
\begin{pmatrix}
\frac{1}{2c^2}(\delta_p-c\rho \delta_u)(\hat{u}-\hat{c})\\
(\delta_{\rho}-\frac{1}{c^2}\delta_p)\hat{u}\\
\frac{1}{2c^2}(\delta_p+c\rho \delta_u)(\hat{u}+\hat{c})
\end{pmatrix}\\
&=\frac{1}{2}\begin{pmatrix}

\hat{\rho}\delta_u+\hat{u}\delta_{\rho}\\
2\hat{\rho}\hat{u}\delta_u +\delta_\rho \hat{u}^2+\delta_p\\
\frac{\gamma u}{\gamma -1}\delta_p+(\hat{\rho}\hat{u}^2+\hat{\rho}\hat{H})\delta_u
+\frac{\hat{u}^3}{2}\delta_{\rho}\end{pmatrix}

\end{align}
$$
代入Roe平均的表达式：
$$
\hat{\rho}=\sqrt{\rho_L\rho_R},~\hat{u}=\frac{\sqrt{\rho_L}u_L+\sqrt{\rho_R}u_R}{\sqrt{\rho_L}+\sqrt{\rho_R}},~\hat{H}=\frac{\sqrt{\rho_L}H_L+\sqrt{\rho_R}H_R}{\sqrt{\rho_L}+\sqrt{\rho_R}}
$$
(19)可以进一步化简为：
$$
\mathbf{D}=\frac{1}{2}(\mathbf{F}_R-\mathbf{F}_L)
$$
因此，(12)可以进一步化简为：
$$
\hat{\mathbf{F}}_{i+\frac{1}{2}}=\frac{1}{2}(\mathbf{F}_R+\mathbf{F}_L)-\frac{1}{2}(\mathbf{F}_R-\mathbf{F}_L)=\mathbf{F}_L
$$
因此，在超声速情况下，$i+1/2$面的数值通量完全由左侧值确定，这和超声速流动“下游只受上游影响，不受更下游影响”的物理特性相符。事实上，上述性质可以直接从Roe构造Roe平均时服从的规则得到。Roe构造Roe平均的雅可比矩阵时，要求：

* 矩阵$\mathbf{A}$可对角化
* 满足：$\mathbf{F}(\mathbf{Q}_R)-\mathbf{F}(\mathbf{Q}_L)=\mathbf{A}(\mathbf{Q}_R-\mathbf{Q}_L)$
* 满足当$\mathbf{Q}_R = \mathbf{Q}_L$时，$\mathbf{A}=\partial \mathbf{F}/\partial \mathbf{Q}$

根据第二条性质，且超对声速流动($u>0$)满足：
$$
\mathbf{D}=\frac{1}{2}\mathbf{R}\left|\mathbf{\Lambda}\right|\mathbf{R}^{-1}(\mathbf{Q}_R-\mathbf{Q}_L)=\frac{1}{2}\mathbf{A}(\mathbf{Q}_R-\mathbf{Q}_L)
$$
可以直接得到$\mathbf{D}=\frac{1}{2}(\mathbf{F}_R-\mathbf{F}_L)$

对于$M\rightarrow0, u>0$的情形，同样可以写出$\mathbf{D}$的表达式
$$
\begin{align}
\mathbf{D}&=\frac{\hat{c}}{2}\begin{pmatrix}
1&1&1\\
\hat{u}-\hat{c}&\hat{u}&\hat{u}+\hat{c}\\
\hat{H}-\hat{u}\hat{c}& \hat{u}^2/2&\hat{H}+\hat{u}\hat{c}
\end{pmatrix}
\begin{pmatrix}
1-M &0 &0\\
0 & M & 0\\
0 & 0 & 1+M
\end{pmatrix}
\begin{pmatrix}
\frac{1}{2c^2}(\delta_p-c\rho \delta_u)\\
\delta_{\rho}-\frac{1}{c^2}\delta_p\\
\frac{1}{2c^2}(\delta_p+c\rho \delta_u)
\end{pmatrix}\\
&= \frac{\hat{c}}{2}\begin{pmatrix}
1&1&1\\
\hat{u}-\hat{c}&\hat{u}&\hat{u}+\hat{c}\\
\hat{H}-\hat{u}\hat{c}& \hat{u}^2/2&\hat{H}+\hat{u}\hat{c}
\end{pmatrix}\begin{pmatrix}
\frac{1}{2c^2}(\delta_p-c\rho \delta_u)(1-M)\\
(\delta_{\rho}-\frac{1}{c^2}\delta_p)M\\
\frac{1}{2c^2}(\delta_p+c\rho \delta_u)(1+M)
\end{pmatrix}\\
&=\frac{\hat{c}}{2}
\begin{pmatrix}
\frac{1-M}{\hat{c}^2}\delta_p+\frac{\rho M}{\hat{c}}\delta_u+M\delta_\rho\\
(\frac{2M}{\hat{c}}-\frac{M^2}{\hat{c}})\delta_p+\hat{\rho}(1+M^2)\delta_u+\hat{c}M^2\delta_\rho\\
\frac{H}{\hat{c}^2}\delta_p+(\frac{M\hat{H}\hat{\rho}}{\hat{c}}+M\hat{\rho}\hat{c})\delta_u+M^2\delta_p+\frac{M^3}{2}(\hat{c}^2\delta_{\rho}-\delta_p)
\end{pmatrix}

\end{align}
$$
略去所有$O(M)$及以上量级的项，那么$\mathbf{D}$可以写为：
$$
\mathbf{D}=\frac{1}{2}\begin{pmatrix}
\frac{\delta_p}{\hat{c}}\\
\hat{\rho}\hat{c}\delta_u\\
\frac{\hat{H}}{\hat{c}}\delta_p
\end{pmatrix}=\frac{\hat{c}}{2}\begin{pmatrix}
\frac{\delta_p}{\hat{c}^2}\\
\hat{\rho}\delta_u\\
\frac{1}{\gamma - 1}\delta_p
\end{pmatrix}
$$
因此，(12)的展开式可以写成：
$$
\hat{\mathbf{F}}_{i+\frac{1}{2}}=\frac{1}{2}(\mathbf{F}_R+\mathbf{F}_L)-\frac{\hat{c}}{2}\begin{pmatrix}
\frac{\delta_p}{\hat{c}^2}\\
\hat{\rho}\delta_u\\
\frac{1}{\gamma - 1}\delta_p
\end{pmatrix}
$$
