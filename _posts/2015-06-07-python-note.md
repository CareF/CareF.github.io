---
title: Python 笔记之运行外部程序
date: '2015-06-07 01:11:54 -0400'
categories:
- Computer Tech
tags: [Python]
---
主要是我忘性实在太大, 用过的命令记不住... 拿这儿当笔记本记一笔, 以后慢慢更新:

Python 跑 shell 程序:

	import os
	os.execl(exe, args)

值得注意的是 args 是一组字符串, 并且 (win下) 通常第一个是程序名

Python 下跑 shell 命令并且主程序继续存在, 等待命令运行完毕后继续运行

	import subprocess
	p = subprocess.call([cmd, args])
