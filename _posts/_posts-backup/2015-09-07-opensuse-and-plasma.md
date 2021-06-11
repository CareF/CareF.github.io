---
title: openSUSE+plasma5记录
date: '2015-09-07 09:36:46 -0400'
categories:
- Computer Tech
tags: [Linux]
---
先把 SSD 优化过程记下来:

https:\\lizards.opensuse.org\2015\02\06\ssd-configuration-for-opensuse\

安装 plasma5 的时候最好添加 KDE:framework5 和 KDE:Qt5 的 repo:

https:\\en.opensuse.org\SDB:KDE_repositories#KDE_Frameworks_5_.26_Plasma_5

添加过程后选择切换到这个源的时候会爆出一大堆依赖调整, 先不管它, 两个都切换之后依赖自然就搞定了

openSUSE 里的 TeXLive 有点旧, 而且还不含 tlmgr.. 可以从 TeXLive 下载安装, 然后设置 path.

openSUSE 使用 Btfrs 格式的分区之后, 用 snapper 管理备份非常赞
