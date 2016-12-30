---
layout: post
status: publish
published: true
title: 搭建工作完成, 也算是有真正的个人网站了
author:
  display_name: CareF
  login: caref
  email: lm0329@126.com
  url: ''
author_login: caref
author_email: lm0329@126.com
wordpress_id: 10
wordpress_url: http://www.lyuming94.com/?p=10
date: '2015-05-23 00:07:39 -0400'
date_gmt: '2015-05-22 16:07:39 -0400'
categories:
- Computer Tech
tags: []
comments:
- id: 2
  author: Liang Yan
  author_email: phycept@gmail.com
  author_url: ''
  date: '2015-05-23 01:29:27 -0400'
  date_gmt: '2015-05-22 17:29:27 -0400'
  content: 一个月前还在想怎么拿到那笔钱，已经放弃了，成功了教我
- id: 3
  author: CareF
  author_email: lm0329@126.com
  author_url: ''
  date: '2015-05-23 10:11:01 -0400'
  date_gmt: '2015-05-23 02:11:01 -0400'
  content: 我只是上传了学生卡照片... 据说是能通过的还在等
- id: 5
  author: CareF
  author_email: lm0329@126.com
  author_url: ''
  date: '2015-05-26 22:11:44 -0400'
  date_gmt: '2015-05-26 14:11:44 -0400'
  content: 已经成功, 见http:&#47;&#47;107.170.205.7&#47;index.php&#47;2015&#47;05&#47;26&#47;apply-for-github-student-developer-pack&#47;
---
服务器搭建在 DigitalOcean 上. 选择 DO 的主要原因是 GitHub 有 DO 的 100 刀学生优惠.. 虽然现在还没拿到这笔钱: 开始得晚了不能靠学校邮箱完成学生身份认定真是遗憾... 看网上的说法是上传学生证照片验证虽然慢一点但其实还是可以拿到的?

DO 的手册赞一个, 简直新手友好! (相比之下某些 Linux 发行版的手册... 不忍吐槽) 从创建 VPS 到搭建 LAMP (Linux, Apache, MySQL, PHP) 栈到安装 WordPress 都有手把手教程. 在教程之外自己做的更改主要包括:
* 设置了一下系统 swap. 穷啊只能用最低配 512 MB 内存的VPS, 动不动数据库就崩, 一看默认没有 swap 简直了...
* PHP 的多字节支持, 具体来说是安装 php-mbstring, 然后重启 Apache
* WordPress 的配置真是新手友好, 唯一值得一提的是学了一下 WP 的 Child Theme 概念, 微调了一下主题

VPS 的另外一个作用是搭了一个 IPv6 的 Shadowsocks 解决科学上网的问题和学校的流量问题 (好吧其实这才是最初的目的, 搭博客反而是第二步), 决定花点时间做这件事的原因之一是这个月初电脑硬盘坏了换硬盘重装系统, 系统更新和各种软件把流量跑完了, 原因之二是又恰好看到知乎上这则回答: [清北校园网如何配置免流量ipv6环境?](http://zhi.hu/iCoH)  于是乎很开心的照做了.
关于这个博客要写点什么东西, 我目前 的想法是:
* 学习生活中遇到的小 trick 的记录
* 之前在人人上放的学习整理要转移到这里
* 今后学术上如果有值得记录的想法
* 吐槽...

夜已深, 还有这里以后还有很多要微调的地方, VPS 的配置也是 (当务之急大约是配置和学习 Git?). 写完这篇之后大概就能把这里公开出去了? 先睡下了.
