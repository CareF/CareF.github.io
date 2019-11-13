---
layout: single
title: "X1 Carbon gen4 & Arch, 系统重装整理"
date:  2019-11-12 22:20:25
categories:
  - Computer Tech
tags:
  - [Linux]
comments: true
---

从双系统到完全在 Linux 下工作快三年了, 眼看着各种小毛病渐渐解决. 
之前以为这个系统会是临时用用的, 现在看起啦会用的越来越长久. 
刚开始的时候做的分区太局促, 于是为了调整分区, 顺便重做了一下系统. 
写个记录留作未来的参考. 

### 硬件 ###

这台小黑随我三年了: `20FBCTO1WW ThinkPad X1 Carbon 4th`. 
买的时候以为可以自己加内存而选了默认 8G, 有点后悔. 另外为了性能选配的 NVMe SSD 
的散热似乎略超出了设计散热能力, 硬盘 IO 强度大的时候风扇就呼呼呼. 
在 Win10 下, 因为后台更新会是个很大的问题, 每次开机都要响几分钟才能消停. 
Linux 下相对可控一点. 

![重做之后的分区]({{ site.url }}/figure/2019-11/arch/filesys.png) 

有使用经验之后重做的分区应该就不那么局促了. 占空间的电影之类移动到了 SD 卡上. 
root 本来想做 128G 的, 调整了几次都没成功, `parted`逼死强迫症... 
还是 Windows 的分区工具指哪儿打哪儿利索. 

说到 SD 卡, 之前 Kernel 有个老 Bug, 容量大于一定值的卡就无法加载, 
`dmesg` 会显示 `mmc0: error -110 whilst initialising SD card`. 
这个问题值到前不久 Linux 5.2.14 才解决. 

同样被近期 Kernel 解决的问题还有之前一直以来会在启动时的警告 (在 `linux-lts` 中任存在): 
```
Warning: Possibly missing firmware wd719x
Warning: Possibly missing firmware aic94xx
```

除此之外, 当初指纹识别没有驱动, 在[联想的论坛](https://forums.lenovo.com/t5/Other-Linux-Discussions/Validity-Fingerprint-Reader-Linux/td-p/3352145)
上讨论许久之后, 在一年多前被网友逆向出了[非官方的驱动](https://github.com/nmikhailov/Validity90). 

如果说硬件和驱动还有什么缺憾的话, 就是 4K 60Hz 视频输出在 Linux 下的驱动似乎还做不到, 
以及如果从 Linux 重启到双系统 Windows 的话可能会黑屏, 必须完全关机再启动. 

### 安装 ###

按照[Arch Wiki Installation Guide](https://wiki.archlinux.org/index.php/Installation_guide_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))按部就班安装即可. 
基本上不会遇到什么坑. 我在家搭的 NUC 小服务器上试了 `system-boot` 作为 bootloader, 
但笔记本上双系统还是用 GRUB 功能丰富一些. 

早几年 bootloader 还经常要自己手写条目, 如今 `os-prober` 包能解决几乎所有问题. 
手动加入的修改是在 `/etc/grub.d/40_custom` 中加入条目: 
```
menuentry "System restart" {
	echo "System rebooting..."
	reboot
}
menuentry "System shutdown" {
	echo "System shutting down..."
	halt
}
```
以方便重启. 重新生成 `grub.cfg` (`grub-mkconfig -o /boot/grub/grub.cfg`), 
将默认选项改为 Windows: 修改 `/boot/grub/grub.cfg` 的 `set default` 条目如下: 
```
if [ "${next_entry}" ] ; then
   set default="${next_entry}"
   set next_entry=
   save_env next_entry
   set boot_once=true
else
   set default="Windows Boot Manager (on /dev/nvme0n1p1)"
fi
```
这么做的主要原因是, Windows 的更新会自动重启, 为了无人监管下完成更新, 
需要在重启时自动加载 Windows. 另外我的使用场景中, Linux 的休眠是真-休眠, 
并没有切断电源而不需要重新加载 bootloader. 而 Windows 的休眠则需要. 
从 Windows 休眠唤醒到 Linux 会导致共享的 NTFS 分区被锁住. 


### 性能优化 ###

按照 Arch Wiki 的指南, 除了正常的安装之外, 做了如下优化: 

1. 安装 intel 的微代码: 
```
pacman -S intel-ucode
```
2. 启用 SSD 的 TRIM
```
systemctl enable fstrim.timer
```
3. 内存 tmpfs: 在 `/etc/fstab` 中加入条目 (Arch 的 tmpfs [默认设置](https://wiki.archlinux.org/index.php/Tmpfs)是一半内存, 这台机子上内存吃紧)
```
# override default tmp
tmpfs   /tmp         tmpfs   nodev,nosuid,size=2G          0  0
```
4. `makepkg` 并行: 修改 `/etc/makepkg.conf`
```
[...]
MAKEFLAGS="-j$(nproc)"
[...]
 COMPRESSXZ=(xz -c -z - --threads=0)
[...]
```
5. swapfile: 内存不够啊还是得开 swap: 
```
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile 
echo "/swapfile none swap defaults 0 0" >> /etc/fstab
```
还要调整 swappiness: `/etc/sysctl.d/90-swappiness.conf`
```
vm.swappiness=1
vm.vfs_cache_pressure=50
```

### 桌面系统 ###

一直以来我都觉得 Linux 的许多理念之争导致了它没有好用的桌面系统. 

Arch 最吸引我的地方, 倒不只是许多人喜欢的 KISS 原则, 而是在 KISS 原则上的实用主义. 
体现在桌面系统上, 各类主流的 WM/DE 大多不让人满意, 

- Xfce 甚至更激进的自称极简的系统
([我的一次尝试]({{ site.url }}/computer%20tech/to-xfce4/)) 
原教旨地追求 stupid simple 的结果是丢失了易用和精致
为了美观我可以花一点业余时间去调整, 但连基本的系统提示音都那么简陋甚至没有设置项就有点难看了. 

- KDE, 与之形成鲜明对比的, 完全不知道 simple 是什么意思, 
我每次尝试都会被完全暴露给用户的复杂度劝退. 

- Gnome, 它大概觉得 stupid 是指用户的智商而不是设计逻辑: 砍起功能来从不手软. 

几经折腾之后, 还是国产的 deepin 最得我心: 美观, 
暴露给用户的部分足够简洁的同时并不妨碍高级的功能. 对于用户的需求保持开放心态, 
在 GitHub 和论坛上及时响应需求, 响应 Bug 也非常及时, 可以说是业界良心. 

最近仅有让我不满的是前不久的一次升级把基于 Mutter 的渲染搞坏了, 说是因为在迁移到 Kwin.. 
然后就要引入一大堆 KDE 的依赖. 不过最近的更新已经修复了这个问题. 
Kwin 也许是 deepin 的未来, 但现在暂时不希望跟进. 

除了安装 `deepin` 和 `deepin-extra` 两个包之外, 修改 `caps` 键位
```
gsettings set com.deepin.dde.keyboard layout-options '["caps:ctrl_modifier"]'
```
其他设置项都可以在图形系统上搞定. 

和 deepin 搭配的 DM 是 lightdm, deepin 自家的 lightdm 主题当然很好, 
但我喜欢 `lightdm-webkit2-greeter`+`material2`. 在 `/etc/lightdm/lightdm.conf` 中设置: 
```
[...]
greeter-session=lightdm-webkit2-greeter
[...]
```
在 `/etc/lightdm/lightdm-webkit2-greeter.conf` 中设置: 
```
[...]
webkit_theme        = material2
[...]
```
代价是登陆的头像需要手动设置: `/var/lib/AccountsService/users/[user]` 

顺便安利下我给 dock 写的俩插件: 
[Arch-update](https://github.com/CareF/deepin-dock-plugin-arch-update), 
[NeoWeather](https://github.com/CareF/deepin-dock-plugin-neoweather)

### AUR ###

`yaourt` 已死, 我现在用 [`yay`](https://github.com/Jguer/yay). 
默认的设置项里 `buildDir` 尽然不是 `/tmp` 就很不合理. 在 `~/.config/yay` 里修改. 

### pacman Hook ###

自己折腾的时候总有些 hack, 搭配 hack 时要做一些安装的时候的自动处理. 
`pacma` 的 hook 位于 `/etc/pacman.d/hooks/`. 下面这个例子是自动删除缓存的. 
```
[Trigger]
Operation = Upgrade
Type = Package
Target = *

[Action]
Description = Removing Cache more than 3 versions ago
When = PostTransaction
Exec = /usr/bin/paccache -rv
```

![neofetch 比 screenfetch 好用]({{ site.url }}/figure/2019-11/arch/neofetch.png) 

除此之外, 我在 `.bashrc` 里调用 [`neofetch`](https://github.com/dylanaraps/neofetch) 生成欢迎页, 但希望在 deepin-terminal 的雷神模式下避免
```
# bashrc
if [[ $(tty) == /dev/pts*  && $(whoami) == lm  && -z "$QUAKE" ]]; then
    neofetch
fi
```
需要 hack 一下以使 bash 知道 ([讨论见这里](https://github.com/linuxdeepin/developer-center/issues/929)). 于是引入这样的 hook: 
```
[Trigger]
Type = File
Operation = Install
Operation = Upgrade
Target = usr/bin/deepin-terminal

[Action]
Description = Making Quake Labled deepin-terminal
When = PostTransaction
Exec = /bin/sh -c 'cd /usr/bin/; mv deepin-terminal deepin-terminal-real; cp deepin-terminal-def-quake deepin-terminal'
```

-------------
今后再有什么折腾自己电脑的小更新大概就都会放在这里了. 