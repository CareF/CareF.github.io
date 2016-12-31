---
layout: post
status: publish
published: true
title: UEFI\GPT 结构的 Win+Linux 双系统
author:
  display_name: CareF
  login: caref
  email: lm0329@126.com
  url: ''
author_login: caref
author_email: lm0329@126.com
wordpress_id: 142
wordpress_url: http://www.lyuming94.com/?p=142
date: '2015-08-30 06:42:22 -0400'
date_gmt: '2015-08-29 22:42:22 -0400'
categories:
- Computer Tech
tags: []
comments: []
---
为了能安装这样的双系统之前折腾过 N+1 次, 从 Ubuntu 到 Debian 到 Fedora 通通失败了... 这次在 Arch 上竟然成功... 记录一笔.

过程基本上是按照 Arch WiKi 上 [Beginners' Guide](https://wiki.archlinux.org/index.php/Beginners'_guide) 进行. 曾经按照这个过程试过后来失败了.. 说明其中有坑, 这一次参照其他若干文档反复对照某些过程, 整理 (还记得的) 坑如下: 

* 关于分区那个部分它给的例子没考虑双系统的问题, 要自己灵活处理. ESP 区就不用做了, 直接用 Windows 分好的那大概 400M 的就好, 也不用设置什么 `set 1 boot on` 之类
* 分区最后挂载的时候倒是提到了 boot 的问题, 千万要记得! 
* fstab 默认产生的会把 Win 的 EFI 分区识别为 vfat 格式, 不要自作聪明改成 fat32. 否则会导致完成所有安装之后只能重启无法顺利挂载 boot, 只能进入 emergency mode
* 最大的坑在于 Bootloader 部分, Beginners' Guide 上以 GRUB 作为 Bootloader 却没有设置 EFI 的结构. 设置方法在[这里](https://wiki.archlinux.org/index.php/GRUB#Windows_installed_in_UEFI-GPT_Mode_menu_entry) 然而只看这一部分是不够的, 要看这个页面前面告诉你在哪里改设置. 然而又一处坑在于 GRUB 词条中给的对于 UEFI-GPT 的  `# grub-mkconfig -o /boot/efi/EFI/GRUB/grub.cfg` 并不正确, 会报错说找不到文件/路径, 要用上面那条, 也即 Beginners' Guide 中一样的 `# grub-mkconfig -o /boot/grub/grub.cfg` 来更新设置

最后 Arch 安装时是能够插拔 U 盘的, 所以我先把 EFI 分区的东西备份了一个. 虽然最后没用上....
