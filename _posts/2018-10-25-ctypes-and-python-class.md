---
layout: single
title:  "笔记: 用 cytpes 联系 Python 和 C 的一些经验"
date:   2018-10-25
categories:
- Computer Tech
tags: [Python]
comments: true
---
## Intro ##
最近在为重写组里一个老软件做准备, 写了一些解一维量子问题的代码 ([Github:1DQuantum](https://github.com/CareF/1DQuantum)). 代码的主要结构是用 C 写计算量大的部分, 然后包一个 Python 的接口. 这个过程中学习了 ctypes 包以及怎么整合 C 中的面向对象意味的代码和 Python class. 
另外这段代码里还用了 OpenMP, 有功夫可以再写一篇 Blog. 

## ctypes ##
ctypes 是 Python 中用来调用 C 编写的动态链接库的包. 
ctypes 最简陋的用法是 `clib = ctypes.CDLL('xxxx.so/dll')` 不过出于科学计算的目的, 反正我们也要大量用 numpy, 所以不如就用 `clib = numpy.ctypeslib.load_library('xxx', '.')`. 至少这么做不用自己操心 OS 相关的后缀名问题. 
(说起来, numpy 还真是喜欢自己重新造个轮子.. 这种方便的改造难道不应该提交给 ctypes 吗.)

加载了动态链接库之后, 就可以直接用 `clib.MyFunc()` 调用其中的函数了.

### 类型 ###
如果函数有参数则往往需要做类型转换. 自动类型转换似乎只有 int 类型. 另外, 在编写 C 函数的时候, Python 的 int 对应 C int 长度是平台相关的. 所以在 C 的部分: 

	#ifdef _WINDLL
	typedef int32_t numpyint;
	#else
	typedef int64_t numpyint;
	#endif

其他的类型转换包括 `ctypes.c_double(x)`, `ctypes.POINTER(<sometype>)` 等.
值得注意的是 numpy 数组转化成 C 指针最简单的方法是
`numpy_array.ctypes.data_as(c_double)`.

C 库被调用的时候是不进行类型检查的. 这样进行调用的时候往往很不安全,
所以还会在 Python 中显式的定义参数和返回值的类型: 

	clib.Numerov.argtypes = [c_double, c_int, c_double, c_double, c_double, _doubleArray, _doubleArray, _doubleArray]
	clib.Numerov.restype = c_double

比如上面这个例子当中, 我定义了 `Numerov` 函数的类型. 其中 `_doubleArray`
是利用 numpy 的轮子.

	_doubleArray = np.ctypeslib.ndpointer(dtype=np.float64,
	                   ndim=1, flags="C_CONTIGUOUS")

这么做的好处是, 调用 `clib.Numerov` 时不再需要对 numpy 数组进行显式的类型转换,
并且 Python 会对类型进行检查. 其中 flags 参数是个很 tricky 的问题: numpy
的数组未必是在连续的内存上顺序存储的, 反例比如通过切片生成的数组 `a[3:5]`,
`a[::-1]` 等, 而这个 `C_CONTIGUOUS` 指示了 Python 拒绝这样的调用. 

### 结构体 ###
在 Python 中处理 C 调用的结构体, 首先需要通过继承 `ctypes.Structure` 定义和 C
代码中对齐的类:

	class cBand(Structure):
	    _fields_ = [("update", c_void_p),
	                ("N", c_int),
	                ("Eg", POINTER(c_double))]

对应 C 代码

	struct BAND{
	    numpyint *update (BAND *, double, double *, double *);
	    numpyint N;
	    double *Eg;
	}; 

而后才能才能正确的处理以结构体为参数或者返回值的 C 函数. 

## 面向对象 ##
C 天生不是面向对象的语言. 虽然可以在 C 上进行面向对象思路的编程,
但需要手工进行构造和析构的调用来完成内存管理,
还需要频繁地进行强制类型转换来模拟继承和重载.

继承和重载的部分可以在 C 代码部分解决, 而通过合理的设计来避免暴露给 Python, 
但构造和析构, 因为和函数的生存期有关, 而 Python 又自带垃圾回收, 应当在 Python
中通过包一层中间代码来完成.

比如上面定义的这个 `cBand` 类型, 在我的代码中通过
`band_new` 构造, `band_free` 析构, 并且存储了一些指针作为必要的成员变量.
我需要保证: 
- 在 Python 中能正确的构造和析构 C 生成的类型
- 保证 C 中引用自 Python 的数据在类型被析构前存活

解决方案是这样设计一个类: 

	class Band(object):
	    """Python interface for a cBand"""
	    def __init__(self, *args, **kwargs):
	        super(Band, self).__init__()
	        # Make refs of parameters of band so it's not garbage collected 
	        self.args = args
	        self.kwargs = kwargs 
	        self.c = cband_new(*args, **kwargs)
	    def __del__(self): 
	        cZBband_free(self.c)

然后通过 `Band.c` 调用 `cBand`. 实际操作中还可以通过修改上述代码来实现 C 中的
"重载" 的 Python 接口. 
