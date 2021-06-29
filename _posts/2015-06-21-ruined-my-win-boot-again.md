---
title: 我又一次在尝试装Linux的时候把Windows的启动项搞坏了...
date: '2015-06-21 16:04:28 -0400'
categories:
- Computer Tech
tags: [Linux]
---
我彻底放弃试 Arch 了, 这次试的是 Debian.. 然后结果还不如最早之前用 Ubuntu, 至少那时候 Ubuntu 成功建好了自家的启动项, 并且替换 EFI 文件之后还能切回到 Windows...

而这次安装之后启动就仍然是 Win8 的然而没法正常启动.. 在若干次折腾\重建分区表\更改分区表类型等操作之后...

用的[这里](http:\\superuser.com\questions\460762\how-can-i-repair-the-windows-8-efi-bootloader)的方法暴力解决的..

然而现在磁盘在 恢复+EFI 和主分区 直接留下了一个 128M 的未分配区域... 不知道是干什么用的...

为什么我这儿双系统就那么蛋疼.... VirtualBox 上同一台虚拟机里装双系统都没有遇到任何器官的地方...

P.S. 被 Win8 的 "安装windows的驱动器已经被锁定。请解锁该驱动器，然后再试一次" 折腾过若干次了...

P.P.S. 不要寄希望于 Win8 的系统映像, 那货硬盘结构稍有变化就跪了啊跪了!

-----
2016-11 更新: 
为了某数值模拟的软件不得不又装了一次 Linux, 结果意料之外地顺利.. 现在已经拿 Arch 做主力系统了... 果然 flag 不要乱立
