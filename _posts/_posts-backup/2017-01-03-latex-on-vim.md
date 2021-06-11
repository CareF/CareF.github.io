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

首先[这里](http://coolshell.cn/articles/5426.html)习惯一下基本用法, 然后
感谢大鹰的[博文](https://bigeagle.me/2015/05/vim-config/)给了我一个出发点. 
在熟悉了 Vim 中控制光标移动的基本操作之后, 跟着大鹰的脚步很快就有应该大体上能
用的编辑器环境了. 熟悉之后就要着手搭建自己的使用环境, 我这里就从 LaTeX 着手. 

## 不要用vim-latex... ## 
我一开始使用的插件是 `vim-latex/vim-latex`, 它有很详细的[官方手册](http://vim-latex.sourceforge.net/documentation/latex-suite/). 

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
~~并没有~~ 我改用[vimtex](https://github.com/lervag/vimtex).. 

## vimtex ##
首先在 `~/.latexmkrc` 下写好自己的配置, 选择编译引擎. [作者
](https://github.com/lervag/vimtex/issues/254) 的偏好显示他并不愿意把这部分设
置集成到 vimtex 中: 
```
$pdflatex = 'xelatex %O %S';
```

然后根据需要还要求启用 Vim 的 clientserver 功能. gvim 自动启用了但如果要在终
端下启用, 需要在启动 Vim 时添加选项 `--servername VIM`. 为了偷懒, 我直接在
`~/.bashrc` 里设置了 alias: 

    alias svim='vim --servername VIM' # for vimtex plugin


当然我还要另做一些设置来满足我的需求, 具体可以看[我的 Vim 设置](https://github.com/CareF/vim-config)

作者似乎并[不打算](https://github.com/lervag/vimtex/issues/179)支持Gnome 的默认浏览器 evince, 
我试了一下推荐的 MuPDF, 这软件设计得到时极简到家, 料想配合 tiling wm 会很惊艳, 
奈何定位太差.. KDE 的 okular 的依赖又实在太多 (KDE 家的东西简直依赖灾难啊..) 
于是决定使用 qpdfview. 在 vimtex 的手册中并没有提到在 qpdfview 中调用反向搜索
的方法, 经探索应该是在 `Edit-Settings...-Source editor:` 选项中填入. 
    
    gvim --remote-silent +%2<Enter>zz "%1"

或者如前述设置了 servername 之后

    vim --servername=VIM --remote-silent +%2<Enter>zz "%1"

从而实现了反向搜索的设置. 这么做有应该小问题: Vim 多开时, 响应可能和预期不一
样. 

其他理论上说是开箱即用的. 从文档中摘录几个常用命令: 

快捷键       | 指令                            | 模式 |
-------------|---------------------------------|------|
\<leader\>ly | \<plug\>(vimtex-labels-open)    | n    |
\<leader\>lv | \<plug\>(vimtex-view)           | n    |
\<leader\>ll | \<plug\>(vimtex-compile-toggle) | n    |
\<leader\>lc | \<plug\>(vimtex-clean)          | n    |






