---
layout: post
status: publish
published: true
title: Python 笔记之运行外部程序
author:
  display_name: CareF
  login: caref
  email: lm0329@126.com
  url: ''
author_login: caref
author_email: lm0329@126.com
wordpress_id: 96
wordpress_url: http://www.lyuming94.com/?p=96
date: '2015-06-07 01:11:54 -0400'
date_gmt: '2015-06-06 17:11:54 -0400'
categories:
- Computer Tech
tags: []
comments: []
---
主要是我忘性实在太大, 用过的命令记不住... 拿这儿当笔记本记一笔, 以后慢慢更新:

Python 跑 shell 程序:

	import os
	os.execl(exe, args)

值得注意的是 args 是一组字符串, 并且 (win下) 通常第一个是程序名

Python 下跑 shell 命令并且主程序继续存在, 等待命令运行完毕后继续运行

	import subprocess
	p = subprocess.call([cmd, args])
