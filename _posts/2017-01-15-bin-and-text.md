---
layout: single
title: "从好好的文件到十六进制数, 与其逆变换"
date:  2017-01-15 00:57:22
categories:
  - Computer Tech
tags:
  - Python
  - encoding
  - vim
comments: true
---
事情的起因是[这样](https://www.zhihu.com/question/54702949) 一则知乎提问, 
看了之后我心血来潮想模仿高赞回答膜一发.. (P.S. 大家还是不要尝试看原回答发的
是什么了.. 太辣眼睛了..) 于是我的回答在[这里](https://www.zhihu.com/question/54702949/answer/141044656)

首先, 要把视频剪出来.. 不过这不是主题. 先看如何从视频得到二进制文件. 最近在
学习 vim, 当然要用一用. 
```bash
vim -b nuchi.mp4
```
而后 vim 指令
```vim
:%!xxd
:%s/\d\{8}: //g
:%s/.\{16}$//g
9999J
:%s/\s\s/ /g
"+9999yy
```
分别把文件变成 16进制表示, 去掉地址头和文件内容尾, 然后合并到一行并删掉多余
的空行, 最后把内容复制到系统剪贴板. 

反之要把 16进制数的字符串变回二进制文件, 手里没有趁手的工具, 于是随手用的
Python: 
```Python
fin = open('a.text', 'r') #事先删掉了空格和换行
s = f.read()
n = int(s, 16)
fout = open('nuchi.mp4', 'wb')
fout.write(n.to_bytes((len(s)-1)//2, 'big'))
```
注意的是, 2 个十六进制数是一个字节 (byte), 上述 s 字符串会有一个 \n 
