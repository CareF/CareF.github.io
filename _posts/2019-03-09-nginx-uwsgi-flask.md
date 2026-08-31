---
layout: single
title:  "笔记: 搭建基于 Nginx-uWSGI-flask 的 web app 并应用于 GitHub webhook"
date:   2019-03-09
categories:
- Computer Tech
tags: [web]
comments: true
---
## Intro ##
未来的 App 将会是 web 的天下. 当初小学期蹭贵系的课, 学了点 Django, 
然后再也没用过.. 这些天学术不顺, 于是只好学了一点点 Flask 搞 Web 应用. 
整个服务的结构是 Nginx 作为 http 服务器, uWSGI 作为中间层, 
用 socket 文件通信, Flask 实现应用. 

这篇博文不谈任何一个层面的具体用法, 只以最简单的范例为例描述一下搭建这个环境的过程. 

## Flask 的简单范例 ##
最简单的一个范例: 
```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a test for flask. '
```

Flask 接受了 http 的请求. 在这个例子中只关系请求的域名. 其中 `'/'` 是 app 的根目录, 
但合理的设置 uWSGI 的情况下, 不必须是整个页面的根目录. 

其他后文用到的 Flask 功能主要是 `flask.request` 的 `header`, `method`, `data` 
等 http 请求的具体内容. Flask 还有 `flask_restful` 包直接实现 RESTful 风格的 API, 


## uWSGI 的配置 ###
这部分在网上能找到许多不同的具体配置方案, 我参考后采取的是使用 `.ini` 文件定义配置, 
用 `mount` 连接 app, socket 进行通信, `systemd` 进行管理的模式. 

以 Arch 为例, 需要安装的软件包除了 `uwsgi` 之外, 还有 `uwsgi-plugin-python`. 
当然对于 docker 来说有现成配置好的环境可以用. 

一个 `example.ini` 的例子; 
```
[uwsgi]
mount = /<app_path>=<script>:app
manage-script-name = true
plugin = python
master = true
processes = 3

chdir = /srv/http/test
uid = http
gid = http
socket = /srv/http/test.sock
logto = /srv/http/test/log
chmod-socket = 660
vacuum = true
```

其中使用 mount 而不是像许多 "教程" 那样使用 module 的原因是, mount + `manage-scipt-name` 
可以正确的处理相对路径. 比如在上面的例子中, 如果 `<app>` 填写的是根目录的话, web app 
就会在网址根目录下, 否则就会在子目录下. 而这并不要求更改 `@app.route('/')` 中定义的 URL: 
uWSGI 会自动进行 URL 地址的转换. 其他 `mount = /<app_path>=<script>:app` 中 `<script>` 
是 Python Flask 脚本的文件名 (不含 `.py` 后缀), 而 `app` 则是脚本中 `app = Flask(__name__)`
定义的变量名. 

`.ini` 文件中定义的三个路径 `chdir`, `socket` 和 `logto` 分别是 app 运行环境的路径, 
用于和 http 服务器通信的 socket 文件的路径以及 log, 三者都可以根据需要填写. 需要注意的是, 
相关路径的读写权限要和 `uid` 以及 `gid` 定义的用户一致. `chmod-socket` 则是 `socket` 
文件的权限表示. `vacuum=true` 表示在关闭 uWSGI 时删除 socket 文件. 

把编辑完成的 `a.ini` 文件链接或复制到 `/etc/uwsgi/` 路径下, 就可以使用
`systemctl status/start/enable/... uwsgi@a.service` 来进行启用等管理了. 

## Nginx 配置 ##
在 Nginx 的一个 Server 中定义: 
```
location = /<app_path>/ {
	include uwsgi_params;
	uwsgi_pass unix:/srv/http/test.sock;
}
```
即可在 `domain/<app_path>/` 下启用 app. 其中 `<app_path>` 与 uwsgi 的配置应该是一致的, 
同时 Nginx 的用户 (Arch 下默认是 http) 要有 socket 文件的读写权限. 

这个简单的配置有一个问题是只能匹配 `domain/<app_path>/` 而无法处理 `domain/<app_path>`. 
Flask 文档推荐的写法是: 
```
location = /test {
	rewrite ^ /test/;
}
location /test {
	try_files $uri @test;
}
location @test {
	include uwsgi_params;
	uwsgi_pass unix:/srv/http/flasktest.sock;
}
```

## 一个简单的应用: GitHub Webhook 的应答器 ##
在 Flask 上我写了一个简单的响应 GitHub Webhook 的 [app](https://github.com/CareF/GitHub-WebHook-AURUpdator). 
主要功能是接收 [create event](https://developer.github.com/v3/activity/events/types/#createevent) 
并且在发现这是个新的 tag 时, 更新 AUR 上的信息. 

功能上检验了 GitHub 提供的 HMAC ([密钥散列消息认证码](https://en.wikipedia.org/wiki/HMAC)) 签名验证, 
验证通过后, 对于新增的 tag, 调用外部 bash 脚本更新 AUR 上的信息. 
目前我发布在 AUR 上的 指示 Arch 更新信息的 deepin-dock [插件](https://aur.archlinux.org/packages/deepin-dock-plugin-arch-update/)
已经使用这套方法自动更新了. 
