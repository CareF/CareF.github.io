---
layout: single
title:  "笔记: 通过 Let's Encrypt 添加个人服务器的 HTTPS 支持[更新]Unicode bug"
date:   2019-02-05
categories:
- Computer Tech
tags: [web]
comments: true
---
## Intro ##
HTTPS 的年代要来了. 我现在主要通过 GitHub Pages 写博客, 另外租一台 VPS 处理各类日常, 必要的时候也用 Nginx 提供简单的 web 服务. 
GitHub 给的建议点击[这里](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/),
在服务器端则参考[这里](https://letsencrypt.org/getting-started/). 

## GitHub Pages ##
GitHub 已经集成了 Let's Encrypt, 使用 CNAME 的 GitHub Pages 直接就可以用 HTTPS 浏览, 同时可以在设置里选择强制跳转到 HTTPS.

## 服务器端 ##
服务器端的系统是 Debian 9. 首先需要[添加 bakcports](https://backports.debian.org/Instructions/).

```
# add to /etc/apt/sources.list
deb http://ftp.debian.org/debian stretch-backports main
```

`sudo apt-get update` 之后, 安装 `sudo apt-get install python-certbot-nginx -t stretch-backports`, 安装完成后, 运行命令 `sudo certbot --nginx certonly` 而后按照提示输入相关信息即可. 

使用 certbot 会自动进行证书的更新, 可谓省心了. 


### 配置 Nginx ###
在 Nginx 相关配置文件中添加一下内容: 

```
listen 443 ssl;
listen [::]:443 ssl;
ssl_certificate /etc/letsencrypt/live/[domain]/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/[domain]/privkey.pem;
```

而后 `sudo nginx -s reload` 就可以用 HTTPS 了. 


### 2019-02-05 更新: 注释中有非 ACSII 字符的 bug ###

如果 nginx 的设置文件中有非 ACSII 字符, 即便字符在注释中, 仍然会导致 `certbot` 崩溃. 
以及有 [issue](https://github.com/certbot/certbot/issues/5592) 提及这件事, 
但尚未来得及修复 (有些年头了这个bug...). 目前的 work-around 是避免使用 Unicode 字符. 
