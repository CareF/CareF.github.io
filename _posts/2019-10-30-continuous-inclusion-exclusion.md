---
layout: single
title:  "连续版本的概率论容斥原理"
date:   2019-10-30
categories:
- Math
tags: [math]
comments: true
---
一道来自绿皮书的概率题: 
在圆周上随机放 $N$ 个点, 求它们在同一个半圆上的概率. 

这题当然有简单的方法: 记上述事件 $A$, 记每个点的极坐标角度 $\theta_i$, 
记 $A_n $ 是所有点在同一个半圆里且半圆中按顺时针的第一个点为 $n$, 
同时可以记为:
$A_n = \\{\theta_i | \theta_n < \theta_{i\neq n} < \theta_n + \pi\\}$
(其中的不等式表示模 $2\pi$ 上的不等式. 

$$
P(A_n) = \prod_{i\neq n}P(\theta_n < \theta_i <\theta_n+\pi) 
= \frac{1}{2^{N-1}}
$$

而 $A_n$ 是互斥事件并且覆盖全部$A$: $\lor_n A_n = A$, 所以

$$
P(A) = \sum_n P(A_n) = \frac{N}{2^{N-1}}
$$

然而我在做题时, 没有想到 $A_n$ 这样的划分, 而是设想在半圆 
$\alpha \le \theta \le \alpha + \pi$ 上计算概率, 然后用容斥原理计算结果. 
然而, 传统的容斥原理并不处理连续变量... 
试图克服/推广的过程中, 出现了产生无穷大, 再消除无穷大这样物理学生喜闻乐见的过程, 
感觉还是挺有意思的. 

以下计算为了方便, 把 $0\sim 2\pi$ 角度映射到 $0\sim 1$, 
并且所有角度位置相关的量都是模 $1$ 的. 

为了把问题变回 (准) 离散问题, 假定把圆周分成 $\delta \to 0$ 的小扇,
$P(\alpha')$ 表示 $\alpha' \le \alpha < \alpha+\delta$ 的范围内, 
一共有 $1/\delta$ 个扇形. 当 $\delta \ll 1$ 时, 
在 $O(\delta^2)$ 的余项下有近似

$$
\sum_\alpha P(\alpha) = \frac 1\delta \int_0^1\mathrm d \alpha
$$

于是统计容斥原理的结果是 (为方便计算概率, 定义容斥原理中涉及的角度为 
$\alpha, \alpha+\tau_1, \alpha+\tau_1+\tau_2, \cdots$): 

$$
\begin{align*}
P(A) &= \frac 1\delta \int_0^1\mathrm d \alpha \frac 1{2^N}
- \frac 1{\delta^2}
\int_0^1\mathrm d\alpha\int_0^{1/2}\mathrm d\tau_1 \,\tau_1^N \\
&\qquad + \frac 1{\delta^3}
\int_0^1\mathrm d\alpha\int_0^{1/2}\mathrm d\tau_1 
\int_0^{\tau_1}\mathrm d \tau_2 \,\tau_2^N - \cdots \\
&= \sum_{n=0}^\infty 
(-)^n \frac 1{\delta^{n+1}} \frac{N!}{(N+n)!} \frac 1{2^{N+n}} \\
&= N!(-\delta)^{N-1} \left(\sum_{n=0}^\infty - \sum_{n=0}^{N-1}
\right) \frac{(-1/2\delta)^n}{n!} \\
&= N!(-\delta)^{N-1} \left(\mathrm e^{-1/2\delta} - 
\sum_{n=0}^{N-1} \frac{(-1/2\delta)^n}{n!}\right) \\
&= \frac{N}{2^{N-1}} + N!(-\delta)^{N-1} \mathrm e^{-1/2\delta}
- N!\sum_{n=0}^{N-2} \frac{\delta^{N-1-n}}{n!(-2)^n} 
\end{align*}
$$

注意到 $\delta\to 0^+$ 时后两项都是 $0$, 于是得到和前面一样的结果 $P(A) = N/2^{N-1}$. 

这个过程中出现了 $1/\delta \to \infty$ 的无穷大, 但最终会被消除. 
其原因应该是连续变量实际上会在算 "交集" 的时候提高一个维度, 
而这个维度本身意义是不明确的, 需要用 $1/\delta$ 来消除. 
这个思维似乎和重整化有异曲同工. 
