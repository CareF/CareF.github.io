---
layout: single
title:  "尝试: Cython 和 inline 优化"
date:   2018-12-14
categories:
- Computer Tech
tags: [Python]
comments: true
---

学习 Cython 的时候, 出于好奇对比了一下 Cython 和 ctypes 调用 C 编写动态链接库的效率, 有一些发现. 运行的 C 代码是: 

```
/* int1.c */
double f(double x){
	return x * ( x - 1.0);
}

double integrate(double a, double b, int N){
	int i;
	double tot = 0;
	double step = (b - a)/N;
	for(i=0; i<N; i++){
		tot += f(a + i*step);
	}
	return tot;
}

double integrateRep(double a, double b, int N, int rep) {
	double tot=0;
	int i;
	for(i=0; i<rep; i++) {
		/* tot += integrate(a, b, N); */
		double step = (b - a)/N;
		int j;
		for(j=0; j<N; j++){
			tot += f(a + i*step);
		}
	}
	return tot/rep;
}
```

Cython 则是: 

```
# intpy.pyx
cdef double f(double x):
    return x * (x - 1.0)

def integrate(double a, double b, int N):
    cdef int i
    cdef double tot, dx
    tot = 0.0
    dx = (b - a) / N
    for i in range(N):
        tot += f(a + i*dx)
    return tot

def integrateRep(double a, double b, int N, int rep):
    cdef int i
    cdef double tot
    tot = 0.0
    for i in range(rep):
        tot += integrate(a, b, N)
    return tot/rep
```

为了避免载入时间上的影响, 把循环写在 C 里面了. 计时: 

```
# timeit testing
import timeit
setup = """
import intpy
from ctypes import CDLL, c_double
clib1 = CDLL("./int1.so")
"""
parm = (0, 5, 1000, 5000000)

if __name__ == "__main__":
    print("test cython")
    print("  Result = ", timeit.timeit(
        "intpy.integrateRep(%f, %f, %d, %d)"%parm,
        setup = setup, number = 1))
    print("test C Lib V1")
    print("  Result = ", timeit.timeit(
        "clib1.integrateRep(c_double(%f), c_double(%f), %d, %d)"%parm,
        setup = setup, number = 1))
```

如上的结果竟然是 Cython 快了近一倍...! 为了弄明白是什么情况, 手工编译 Cython 使用相同的优化策略: 

```
# Makefile
CFLAGS += -shared -fPIC -Ofast

all : int1.so intpy.so

intpy.c : intpy.pyx
	cython -3 $^

intpy.so : intpy.c
	$(CC) $(CFLAGS) -pthread -I/usr/include/python3.7m -o $@ $^

%.so : %.c
	$(CC) $(CFLAGS) -o $@ $^
```

经过一些尝试, 发现如果把 `f` 函数在 C 里面定义为内联函数, 或者宏, C 库立马就和 Cython 速度快了 (快得不多). 纯 C 当然还是最快的, 即便不使用内联定义. 

记得曾经看到别人说, 不需要自己声明内联, 因为编译器几乎总是能做出最好的判断来进行内联化的优化. 不过显然在 Linux 下, 编译为动态链接库时, 内联优化并没有启动, 即便 `-O3` 和 `-Ofast` 都包含了内联的 flag. 

比较让人讨厌的是, 手工加入 `inline` 关键词会让编译出来的 .so 文件失去相应的接口... 




