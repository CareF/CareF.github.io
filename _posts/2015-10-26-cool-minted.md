---
title: 酷炫的 minted 宏包
date: '2015-10-26 21:47:37 -0400'
categories:
- Computer Tech
tags: [LaTeX, Python]
---
listings 宏包很好用, 不过 minted 宏包更好用. 毕竟调用了 Python 来做 parser 和上色.

## 安装 ##

根据宏包的文档, 需要 Python 的 Pygments (win 下)

	pip install Pygments

进行安装. 然后就能愉快的开始使用了

## 使用 ##

直接上我调好的 Sublime Text snippet 吧:

    <snippet>
        <content><![CDATA[\begin{listing}[!htp]
      ${5:\begin{minted\}[linenos, gobble=2, tabsize=4, style=xcode]{${3:C++}\}
      ${0:/* A Sample for minted.. A new try*/
        #include <stdio>
        int main(){
          printf("Hello world!..\n");
          return 0;
        \}}
      \end{minted\}}
      ${4:% \inputminted[linenos, tabsize=4, style=xcode]{${3:C++}\}{temp.cpp\}}
      \caption{${1:listing}\label{lst:${2:${1/\\\w+\{(.*?)\}|\\(.)|(\w+)|([^\w\\]+)/(?4:_:\L$1$2$3)/g}}}}
    \end{listing}]]></content>
        <tabTrigger>lst</tabTrigger>
        <scope>text.tex.latex</scope>
        <description>LaTeX minted listing</description>
    </snippet>

选 style 的时候看了若干, 默认的毕竟实在太鲜艳. emacs 和 vim 也类似..
随后还是苹果的配色好啊... 不得不佩服苹果的设计水平

