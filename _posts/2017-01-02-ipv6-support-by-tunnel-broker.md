---
layout: single
title:  "用 IPv6 Tunnel Broker 让 AWS 支持非原生 IPv6"
date:   2017-01-02
categories:
- Computer Tech
tags: [VPS, IPv6]
comments: true
---
### 动机 ###
DigitalOcean 的教育账号优惠用完了... (我为什么没想着用普林的邮箱再申请
一个呢.. 怎么就那么老实地把普林的邮箱也绑到原来的 GitHub 账号上去了呢.
于是打算把这台 VPS 停用. 又恰好 Amazon 家又有免费的服务器用了. 然而,
Amazon 并不提供 IPv6 地址.. 我现在还得依靠 IPv6 连接回清华啊.. 

### 找隧道 ###
[tunnelbroker.net](http://tunnelbroker.net/) 提供免费的 IPv6 Tunnel
Broker. 注册完成之后添加 Tunnel (`Create Regular Tunnel`), 需要输入
VPS 的 IP 地址, 并且选择合适的隧道位置. 创建完成之后就能看到分配的
IPv6 地址, 而且是很奢华的 /64 即 $2^{64}$ 个地址. 此外, 在 `Example
Configuration` 中 tunnelbroker.net 还很贴心地给了设置方法样例. 

值得一提的是, AWS 的默认安全策略非常保守.. 需要在安全组中允许相应流量
入站才能成功创建 tunnel. 

### 设置 AWS ###
*但是* tunnelbroker.net 的设置方法在 AWS 上是不行的... 原因似乎是因为内部地址分配 
(好吧我承认我计算机网络课程水过去了... 啥都不知道..). 解决办法我参照了
[这个](https://samsclass.info/ipv6/proj/pHE1A-Tunnel.htm). 
具体来说先创建一个执行文件用于获取内部 IP: 

    #!/bin/bash
    ip addr show dev eth0|grep "inet "|awk '{print $2}'|awk -F/ '{print $1}'

保存到 `/usr/local/bin/checkipeth0` 并更改权限 

    $ sudo chmod +x /usr/local/bin/checkipeth0

而后在 `/etc/network/interfaces` 中添加以下内容: 

    auto he-ipv6
    iface he-ipv6 inet6 v4tunnel
      address $CLIENT_IPV6
      netmask 64
      endpoint $SERVER_IPV4
      local `/usr/local/bin/checkipeth0`
      up ip -6 route add default dev he-ipv6
      down ip -6 route del default dev he-ipv6

其中两个 IP 地址根据隧道给出配置的填写即可. 然后执行

    $ sudo ifup he-ipv6
    $ ifconfig he-ipv6
    $ ping6 -c 4 google.com

最后一行是用于检验能否 ping 通 IPv6 的. 如果之前有错误的配置, 需要执行

    $ sudo ip tun del he-ipv6

删除旧的设置. 

至此, 我的目的已经达成了. 但如果要建 IPv6 的站点, 还有更多的技巧来做地
址绑定和发送心跳保持隧道开启. 这些事情都等今后有需要的时候再说就是. 
