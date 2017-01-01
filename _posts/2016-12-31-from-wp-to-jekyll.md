---
layout: post
title:  "从 WordPress 搬到 Jekyll 了"
date:   2016-12-31 15:41:00 -0500
categories: 记录
comments: true
---
之前一直觉得 WordPress 太庞大, 自己只用了很小一部分功能. 恰逢
DigitalOcean 的赠送余额到期, 想着把博客搬迁一下. 然后被人安利了 GitHub
Page 和 Jekyll, 于是学习一下如何使用 Jekyll 顺便把博客搬迁过来. 

## 安装和配置 ##
我参照了[这里](http://cenalulu.github.io/jekyll/how-to-build-a-blog-using-jekyll-markdown/).
除了默认安装的依赖项之外, 还需要手动安装 bundler: 

	gem install bundler
	bundler update      # necessary in some case

其他照做就能搭起来一个简单的框架, push 到 GitHub 上的
[用户名].github.io 的 repo 上就能在相应域名看到页面. 

## 从 WordPress 迁移数据 ##
参照 Jekyll 的官网相关[页面](http://import.jekyllrb.com/docs/wordpress/)
有迁移的教程. 

遇到的困难是 DigitalOcean 上我之前用的系统是 CentOS, 软件库里的 Ruby
太老了, 不支持其中的一些工具... 网上查了一下解决办法是自己编译新的 Ruby. 
过程中还遇到了一些权限管理的问题不提.. 反正这个 VPS 很快就打算弃用了,
权限乱了就乱了. 

用这个工具迁移 WordPress 的一个问题是导入的日志都是 html 格式的, 会出
现一些奇怪的转义符解释错误.. 手动把 html 转成 markdown, 顺便复习一下
markdown 的用法..

## 套用模板 ##
TBD

## 撰写文章 ##
基本上就是 markdown, 除了开头要有一个 ["YAML 头信息"](http://jekyllcn.com/docs/posts/). 

TBD: 从 WordPress 转入的文章, 头信息内容很丰富, 包含了评论信息, 另外作
者一栏内容更是繁多, 而且默认情况下似乎识别错误. 我猜测是要搭配某些模板
使用的. 

## DisQus 评论系统 ##
TBD
