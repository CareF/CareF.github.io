---
title: 使用 pickle 保存 Python 的对象
date: '2015-05-31 16:03:06 -0400'
categories:
- Computer Tech
tags: [Python]
---
用 pickle 保存 Python 中的类, 尤其是自己写的类. 代码其实很简单: 

    #输出
    import pickle
    output = file('myclass.pkl','wb')
    pickle.dump(myclass, output, pickle.HIGHEST_PROTOCOL)

    #输入
    inputf = file('muclass.pkl','rb')
    myclass = pickle.load(inputf)

其中 pickle.HIGHEST_PROTOCOL 是可选参数, 忽略表示不压缩, pickle.HIGHEST_PROTOCOL 与任意负数等价, 表示按照最高压缩率来进行. 考虑性能瓶颈往往在 IO 上, 实际使用时压缩率高的往往速度也快. 

注意的是, 不压缩的时候输入输出不必使用二进制 ('b'), 但压缩时必须用二进制, 否则读取出错.

网上说 cPickle 由于用 C 实现效率更高, 在 Python3 中改为 \_pickle, 并且在 pickle 中直接掉用 \_pickle (就该这样嘛!)

-----
2015-07-04

P.S. file 在 Python3 中被废弃, 今后都用 open. 就喜欢 Python 这种不该有的就扔掉的逻辑!
