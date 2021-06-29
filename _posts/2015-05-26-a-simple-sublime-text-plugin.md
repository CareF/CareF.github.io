---
title: 如何写一个简单的 Sublime Text 插件
date: '2015-05-26 00:44:10 -0400'
categories:
- Computer Tech
tags: [Sublime Text]
---
Sublime Text 做文本编辑器一直用得很爽, 现在要用到的 C/C++ 代码, Python 和 $$\mathrm{\LaTeX}$$ 文档都在上面写了. $$\mathrm{\LaTeX}$$ 在 Sublime Text 上使用过程中仅剩的一点不爽在于没法简单地打开宏包的文档 (参见 TeXWork 的 帮助-doc 功能). 当然前不久我才知道 shell 命令 "texdoc [packagename]" 可以实现. 但写文档的时候再开 shell 未免不优雅. 于是决定学一学怎么写插件, 顺便熟练一下 Python.

(以上动机都是扯淡)

----

GitHub地址: [https://github.com/CareF/Show-Texdoc](https://github.com/CareF/Show-Texdoc)

----

(以下涉及系统路径均基于 Windows, $$\mathrm{\LaTeX}$$ 发行版用的是 TeXLive, 手头没有别的发行版测试)

首先在 %appdata%\Sublime Text 3(2)\Packages 文件夹下新建放置插件的文件夹, 在 Sublime 中 Tools-New Plugin... 创建一个插件根文件保存到该文件夹. 新的文件如

    #!/usr/bin/python
    import sublime, sublime_plugin

    class ExampleCommand(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.insert(edit, 0, "Hello, World!")

其中 ExampleCommand 会被 Sublime 识别为名为 example 的命令 (如果有多个大写会被自动分词并添加下划线). 这一段代码的执行效果是在文档开头添加 Hello, World. 测试方法是按 C+\` 然后输入命令 "view.run_command('example')"

更具体的可以查询[手册](http://www.sublimetext.com/docs/3/api_reference.html#sublime_plugin.ApplicationCommand). 

------------

更新 2015/5/26 凌晨: 

完成一个刚刚能实现功能的版本, 在上述文件夹中创建两个文件, 其中功能实现代码如下: 

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    # Filename: ShowTexdoc.py
    # Author:   Lyu Ming <CareF.Lm@gmail.com>

    import sublime, sublime_plugin
    import os

    class PromptShowTexdocCommand(sublime_plugin.WindowCommand):
        '''Ask for input from users'''
        def run(self):
            self.window.show_input_panel("Show Texdoc:", "", self.on_done, None, None)
            pass

        def on_done(self, packagename):
            try:
                if self.window.active_view():
                    self.window.active_view().run_command("show_texdoc", {"packagename": packagename} )
            except ValueError:
                pass

    class ShowTexdocCommand(sublime_plugin.TextCommand):
        '''Call for the package docs'''
        def run(self, edit, packagename = 'texlive'):
            os.system('texdoc '+packagename)

另一个文件把它添加到 Sublime Text 的命令中, 文件名"Default.sublime-commands", 代码

    [
        {
            "caption": "Show TeXdoc",
            "command": "prompt_show_texdoc"
        }
    ]

于是现在可以 Ctrl+Shift+P, "Show TeXdoc", 然后键入宏包名打开宏包文档了.

-------

回头再添加功能, 预计要包括从自动识别 tex 后缀, 分析文中包含的宏包类型, 选中宏包名用快捷键查询, 如何发布到插件库中等. 代码部分都有实现思路但 API 需要查. 先就这样. 

------

补充一句, ST2 和 ST3 对于 import 的路径有所不同, ST2 在直接按照相对路
径 import 就好, ST3 需要加相对路径:

    #!/usr/bin/python
    if sublime.version() < ‘3000’:
        # we are on ST2 and Python 2.X
        # _ST3 = False
        from tex_package_recognizer import GetPackagenameInline
    else:
        # _ST3 = True
        from .tex_package_recognizer import GetPackagenameInline

------
2015-07-05

[给 Sublime 的 Package Control 贡献自己写的插件]({{ site.url }}/computer%20tech/upload-my-sublime-package/)

