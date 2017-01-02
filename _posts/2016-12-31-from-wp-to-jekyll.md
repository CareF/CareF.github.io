---
layout: single
title:  "从 WordPress 搬到 Jekyll 了"
date:   2016-12-31 15:41:00 -0500
categories:
- Computer Tech
tags: [GitHub, Jekyll]
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

## 撰写文章 ##
基本上就是 markdown, 除了开头要有一个 ["YAML 头信息"](http://jekyllcn.com/docs/posts/). 

从 WordPress 转入的文章, 头信息内容很丰富, 包含了评论信息, 另外作
者一栏内容更是繁多, 后面既然确定了模板, 还要根据模板要求更改. 

## 套用模板 ##
经过一番选择和折腾, 最后选择了 [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/Misa)
作为模板. 这个模板看起来还是很成熟的, 如果不是为了 GitHub Page, 甚至已
经进入了 Ruby 的官方仓库而不需要 fork. 

一个教训是应该先看好模板再做迁移工作的.. 为了把模板和之前已经做好的部
分统一, 多非了好多心思. 我现在的使用策略是先把模板添加为远程分支, 然后
merge (参考[这里](http://blog.csdn.net/gouboft/article/details/8450696)). 
注意现在 git 已经禁用无关项目 merge, 需要用 `--allow-unrelated-histories` 
选项强行合并然后再手动调整. 

Minimal Mistakes 的[手册](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)
非常的棒, 按照手册一步步来就能调整得不错. 只有 category 和 tag 的功能
实现没有详细解释. 不过参考一下它的 demo, 也不太难. 

### 添加知乎 ###
默认的 Minimal Mistakes 的作者社交网络链接不含知乎.. 要[手动添加](https://mmistakes.github.io/minimal-mistakes/docs/layouts/#author-profile)
.. 添加时引入了一个新的问题: 模板中使用的[Font Awesome icon](http://fontawesome.io/icons/)
中并没有知乎... 于是只好先去阿里家的[iconfont](http://iconfont.cn/plus)
找到知乎的图标, 然后自己添加 CSS.. 

## [DisQus](https://disqus.com/) 评论系统 ##
加入评论系统比想象的简单多了, 按照 Minimal Mistakes 的 `_config.yml`
文件的设置, 注册 DisQus, 按照[要求](https://help.disqus.com/customer/portal/articles/466208-what-s-a-shortname-)
注册页面并填写 shortname 即可. 

然而之前从 WordPress 转过来的评论就全部丢了... 丢了就丢了吧.. 

## 添加 LaTeX 支持 ## 
TBD
