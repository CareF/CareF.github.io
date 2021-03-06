---
title: Python 的 map 并行计算
date: '2016-02-26 11:38:10 -0500'
categories:
- Computer Tech
tags: [Python, parallel]
---
年前玩数模美赛的时候做的模型挖了一个大坑: 多结点非线性非马尔科夫的传播模型... 到最后一天发现考察参数依赖关系的时候运算能力跟不上了. 想起科协新的服务器有24核, 拿来做并行计算想必是极好的, 学习了一下Python有很好上手的并行化包 (简直庆幸上手时候用的Python...), 在这里做个记录:

	from multiprocessing import Pool # 多进程
	# from multiprocessing.dummy import Pool as ThreadPool # 多线程
	pool = Pool()
	listofresult = pool.map(func, listofdata)
	pool.close()
	pool.join()

其中 multiporcessing 用于 CPU 密集型的任务, 而 multiprocessing.dummy 用于 IO 密集型的任务. map 简单粗暴地把 listofdata (每个 list 的元素都是可以是个 tuple) 都作为 func 的输入, 分别计算. multiporcessing 里还有更加高级的并行功能, 不过鉴于糙快猛的模型模拟并用不着什么高级的功能, 于是就这样简单快上了.

扔服务器上 (setsid python3 xx.py) 之后把 24 核 CPU 跑满, 看 top 里面满排的 Python 有种莫名其妙的壮观感. 话说回来.. 那么糙快猛的程序遇到问题要强行终止好像变得不那么容易了...

从想到要做并行, 搜索, 试用到直接扔服务器上开始跑模拟, 整个学习到应用时间不超过半小时, Python大法果然好! (虽然去年计算物理用 MATLAB 的 parfor 好像也不难的样子...)

P.S. 昨天遇到一位五字班 (大神) 学弟, 感觉口味和爱好和我当年真是相似, 但能力和眼界比起那时候的我不知道高到哪里去了. 而他竟然关注了我这小破博客和那小小破 GitHub 主页, 好开心 :) 回来赶紧补一点东西上去.
