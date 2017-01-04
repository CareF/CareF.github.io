---
layout: single
title: "Vim 学习之 LaTeX 环境搭建" 
date:   2017-01-03
categories:
- Computer Tech
tags: [Vim, LaTeX]
comments: true
---
在我 Sublime Text 用得正爽的时候, 大概从来没想过会有一天开始学习 Vim.. 
然而生活就像是人生就像一盒巧克力, 对吧. 我把我的 Vim 配置放在
[这里](https://github.com/CareF/vim-config). 

首先[this](http://coolshell.cn/articles/5426.html) 
感谢大鹰的[博文](https://bigeagle.me/2015/05/vim-config/)给了我一个出发点. 
在熟悉了 Vim 中控制光标移动的基本操作之后, 跟着大鹰的脚步很快就有应该大体上能
用的编辑器环境了. 熟悉之后就要着手搭建自己的使用环境, 我这里就从 LaTeX 着手. 

## 教程 ## 
我这里使用的插件是 `vim-latex/vim-latex`, 它有很详细的[官方手册](http://vim-latex.sourceforge.net/documentation/latex-suite/). 

安装方法非常简单, 跟着大鹰的文章, 装上 vim-plug 之后, 插入
```vimrc
Plug 'vim-latex/vim-latex' 
```
然后运行 `:PlugInstall` 即可.

我从 [Beginner's
tutorial](http://vim-latex.sourceforge.net/documentation/latex-suite-quickstart/)
开始读起 (然而这份 tutorial 使用的是 GUI 版本..). 
当然这些都在本地有 help 文档. 这里我

有一个问题是如何选择编译器. 看起来 vim-latex 并不支持. 搜索之下找到了这篇
[文章](http://www.jianshu.com/p/6ecb64bd4436). 
经过几番努力和尝试, 我还是没能在 Vim 内成功解决以下目标: 
- 调用 latexmk 进行编译
- 产生 PDF 文件并显示
- 正向/反向搜索

咨询一些朋友之后意识到... 貌似并没有什么简单的办法... 所以我经过一番挣扎之后
~~并没有~~ 我决定回头考完试转投 Emacs.. 

完...

