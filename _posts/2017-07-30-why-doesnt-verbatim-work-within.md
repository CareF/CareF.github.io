---
layout: single
title: "翻译：为什么 verbatim 环境在...下不正常？"
date:  2017-07-30 14:01:18
categories:
  - Computer Tech
tags:
  - LaTeX
comments: true
---

本文是 [Why doesn’t verbatim work
within …?](http://www.tex.ac.uk/FAQ-verbwithin.html)
的翻译。这篇文章在某次 debug
的时候翻到，在收藏夹里存了很久，难得有心情，给自己留个档案。

------
LaTeX 的 verbatim 命令更改了 TeX 内部的类别码（[category codes](https://tex.stackexchange.com/questions/16410/what-are-category-codes)）。
Knuth 说这类东西如何适时使用需要特别小心，因为类别码一旦被设定就不再改变。
所以`\verb` 和 `\begin{verbatim}` 需要假定它们是最早看到作为参数的文本的；
否则 TeX 就已经设定了类别码，从而 verbatim 命令就没有这个机会了。例如：

	\verb+\error+

编译正常，但如果我们定义一个宏再把 `\verb` 作为参数

	\bewcommand{\unbrace}[1]{#1}
	\unbrace{\verb+\error+}

则不能输出希望的结果（会试图运行命令 `\error`）。
其他的报错可能有 '\verb ended by end of line'，
或者更有帮助一些的 '\verb illegal in command argument'。
在 `\begin{verbatim}...\end{verbatim}` 中也有类似的问题：

    \ifthenelse{\boolean{foo}}{% raw %}{%{% endraw %}
    \begin{verbatim}
    foobar
    \end{verbatim}
    }{% raw %}{%{% endraw %}
    \begin{verbatim}
    barfoo
    \end{verbatim}
    }

报错如 'File ended while scanning use of \@xverbatim'，
因为 `\begin{verbatim}` 找不到匹配的 `\end{verbatim}`。

这就是为什么 LaTeX 书籍坚持 verbatim 命令不能出现在其他命令的参数中；
它们不仅仅是脆弱的，在“通常”的命令参数中还非常不可用，即使使用了
`\protection` 命令。

应该问自己的第一个问题是：“`\verb` 命令真的是必要的吗？”

- 如果 `\textt{your text}` 和 `\verb+ your text+` 产生一样的结果，那一开始就不应使用 `\verb`
- 如果你在用 `\verb` 输入网址，邮箱地址或其他类似的东西，用 url 宏包中的 `\url` 命令：它没有 `\verb` 中的那些问题，虽然它还是不很可靠。[这篇文章](http://www.tex.ac.uk/FAQ-setURL.html) 给了一些相关的建议
- 如果你要把 `\verb` 放到一个盒子命令 （如 `\fbox`）里，考虑用 `lrbox` 环境：


	\newsavebox{\mybox}
	...
	\begin{lrbox}{\mybox}
	    \verb!BerbatimStuff!
	\end{lrbox}
	\fbox{\usebox{\mybox}}

如果你无法避免使用 verbatim，那 `\cprotect` 命令（cprotect 宏包）也许有帮助。
这个宏包通过在宏前面加 `\cprotect` 前缀，让它读取的 verbatim 参数“消毒”：

	\cprotect\section{Using \verb|verbatim|}

这个宏包在如上的简单例子里能正常运作，在很多其他的情况下也值得考虑；宏包的文档给出了更多细节。

另一个方法是用测试版 LaTeX3 的宏包 xparse 中的 `\NewDocumentComman` 命令的一个 “参数类型”

	\NewDocumentComman\cmd{ m v m }{#1 `#2' #3}
	\cmd{Command }|\furble|{ isn't defined}

给出结果

	Command \furble isn't defined

这里的 `m` 标签标示一个普通的强制参数，`v` 标示一个 verbatim 参数。
可以看出，它在”普通”的参数串中”插入“了一个 `\verb` 风格的命令；其中 `|` 可要用任何其他不冲突的字符代替。

这个方案很优雅，但缺点是 xparse 宏包引入了庞大的实验性的 LaTeX3 编程环境 (l3kernel)。

除了 cprotect 宏包，还有其他四中部分解决方案：

- 一些宏的设计会负责处理参数中的 verbatim 文本。例如 fancyvrb 宏包定义了一个命令 `\VerbatimFootnotes`，这个命令重定义了 `\footnotetext` 命令，从而改变了 `\footnote` 的行为，于是你可以在 `\footnote` 的参数中使用 `\verb`。这个方法原则上可以拓展到其他命令上，但可能会和其他宏包发生冲突：如 `\VerbatimFootnotes` 和 footmisc 宏包的 para 选项交互很差。
	memoir 类型定有了它自己的 `\footnote` 命令，从而使得它能接受参数中的 verbatim 而不需要其他支持宏包。
- fancyvrb 宏包定义了一个命令 `\SaveVerb` 和它对应的 `\UseVerb` 命令，允许你保存和再次调用它参数中的内容；这个宏包的文档中有关于这个特别强大的功能的细节。
	更简单的是 verbdef 宏包，它的 `\verbdef` 命令定义了一个可靠的命令拓展给出的 verbatim 参数；newverbs 宏包以及其他相关的宏包也提供了类似的功能。
- 类似的，verbatimbox 宏包允许把 verbatim 内容放在盒子里：


	\begin{verbbox}
	some exotic _&$ stuff
	\end{verbbox}
	\theverbbox

- tcolorbox 宏包提供了类似的功能
- 如果你只有一个有问题的字符（不包含这个字符的话就可以直接用 `\texttt`），考虑使用 `\string`。`\texttt{my\string_name}` 的效果和 `\verb+my\_name+` 是一样的，并且可以在一个命令的参数中使用。但是在[运动参数](http://www.dickimaw-books.com/latex/novices/html/fragile.html)中不能政策工作，`\protection` 无助于解决这个问题。
	一个可靠的替代品是：


	\chardef\us=`\_
	...
	\section{... \texttt{my\us name}}

- 还可以考虑把 verbatim 的内容放在外部文件中。。

-------
P.S. Jekyll 在输出上面代码段中的 `{% raw %}{%{% endraw %}` 时报错。。因为错把它当成 Jekyll 的转义字符了。。解决方法是用 `{% raw %}{%{% endraw %} raw {% raw %}%}{% endraw %}{% raw %}{%{%{% endraw %} endraw {% raw %}%}{% endraw %}` 来对它做转义。。 太愚蠢了。。


