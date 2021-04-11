---
layout: single
title:  "Python setuptools 在安装前执行指定脚本并生成数据文件"
date:   2021-04-10
categories:
  - Computer Tech
tags: [Python]
comments: true
---

我希望实现的效果是在安装前执行特定的脚本来生成一些文件, 并把这些文件作为数据文件用于这个
Python 包. [这里](https://cuyu.github.io/python/2017/08/07/%E4%BD%BF%E7%94%A8setuptools%E5%AE%9E%E7%8E%B0pip-install%E6%97%B6%E6%89%A7%E8%A1%8C%E6%8C%87%E5%AE%9A%E8%84%9A%E6%9C%AC)以及一系列英文网站上都有类似的方案, 
但全部都不 work. `setuptools` 的相关文档也同样语焉不详. 此处将我的 hack 记录如下. 

首先大的思路和上面链接中的是一致的, 即重写一个 `installCommand` 作为 `setup` 的 `cmdclass` 参数

```python
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        YOUR_FUNCTION()  # Replace with your code
        super().run()
```

这样做可以使 `python setup.py install` 运行时能够完成需求. 
然而这样做是不足以覆盖所有的按照情况的, 还需要重写 `develop`, 即

```python
from setuptools.command.develop import develop

class CustomDevelopCommand(develop):
    def run(self):
        YOUR_FUNCTION()  # Replace with your code
        super().run()
```

实际测试下来以上在 `python setup.py` 下的行为符合要求, 但在 `pip install` 的行为则不符合. 
`YOUR_FUNCTION()` 的脚本执行了, 但生产的文件没有被拷贝到包中. 
经过一些试验, 需要重写 `bdist_wheel` 即

```python
from wheel.bdist_wheel import bdist_wheel

class CustomBdistWheelCommand(bdist_wheel):
    def run(self):
        YOUR_FUNCTION()  # Replace with your code
        super().run()
```

此时 `setup` 应形如

```python
setuptools.setup(
    ...
    ,
    cmdclass={
        'bdist_wheel': CustomBdistWheelCommand,
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand
    },
    package_data={
        'YOUR_PACKAGE': ['GENERATED_DATAS', ...]
    }
)
```

更进一步可以使用一个全局变量来避免重复执行

```python
_built = False

def YOUR_FUNCTION():
    global _built
    if _built:
        return
    _built = True
    ...
```

当然, 打包时要使用源码格式

```bash
python setup.py sdist
```

而不是

```bash
python setup.py sdist bdist_wheel
```

------------

`pip` 和 `setup.py` 的行为不完全一致的原因我没能查清楚. 以下是一些尝试.. 

首先是检查 `pip install` 和 `setup.py install` 分别运行了哪些指令


```bash
python setup.py install -v 2>&1 | grep running
```

的输出是

```
running install
running build
running build_py
running install_lib
running install_egg_info
running egg_info
running install_scripts
```

而

```bash
python -m pip install . -v 2>&1 | grep running
```

的输出是

```
  running egg_info
    running dist_info
  running bdist_wheel
  running build
  running build_py
  running install
  running install_lib
  running install_egg_info
  running egg_info
  running install_scripts
```


实测把上述 `install` 的重载改写改成 `build`, `build_py` 等有同样的效果: 
能在 `setup.py install` 中生效但不能在 `pip install` 中生效. 
疑似 `pip` 在 `bdist_wheel` 完成之后固定化了一些文件列表. 但 `-vvv` 的输出中, 
`running bdist_wheel` 和 `running build` 中间又没有别的内容了.

如果读者有什么更好的建议, 非常感谢!


