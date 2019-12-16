---
layout: single
title:  "使用 iptables mangle 表连接两个 tinc IPv6 私网"
date:   2019-12-15
categories:
- Computer Science
tags: [network]
comments: true
---
一直蹭着 X 老师组织的 entropy 私网来解决 IPv6 的需要和借用清华的图书馆文献权限资源. 
entropy 基于 tinc 和 babel, 在 Linux 下运行得很好. tinc 有跨平台支持 (虽然 iOS 下要越狱.. 而 Cydia 已死)
但 babel 则要麻烦得多. 

最近换了电脑. 在 Mac 上配置 tinc 是靠谱的, babel 不太方便. 
同时还想试验一下怎么用 iptables 的策略把两个私网连接起来, 为以后更灵活地引入 tinc 之外的方案
 (比如 zerotier? ) 做准备. 

 整理需求如下: 
 1. 可以在私网内解决代理和 IPv6 访问的需要
 2. 通过接入 entropy 的节点, 以该节点的身份访问其他 entropy 节点
 3. 兼容 entropy 的其他服务 (如 IVI 等)
 4. 对于私网本身运行依赖的组件, 尽量安排在服务器端

 手里拥有的资源是一台接入 entropy 的节点 V, 节点上拥有 `/64` 的 IPv6 地址空间. 

 下以 `T:babe::/80` 代 entropy 的地址, 节点 V 在 entropy 的地址空间为 `T:babe:3330::/92`, 
 V 的公网 IP6 地址为 `V::/64`, 需要连接 entropy 的私网称为 tcouple

## 划分地址段 ##
出于方便, tcouple 直接使用 V 的公网 IP 的一个子段, 子段的选择按照下面的要求进行. 

为了能使用 entropy 内部的资源, 需要把 tcouple 的节点翻译到 `T:babe:3330::/92`, 
考虑到 92-96 地址段被用于标识服务, tcouple 只能拥有最多 `96` 的地址空间. 

同时按照 [RFC 6296](https://tools.ietf.org/html/rfc6296#section-3.5) 规则, 
将最长 `/64` 的前缀做地址转换时, 会对 64 往后的 4 段 16 位地址中第一个非 `0xFFFF` 
的地址段进行改写. 在构建 V 上 entropy 的 NPT 服务时, 实际上就以及把 entropy 的地址 
`T:babe::/80` 映到了 V 的公网地址 `V:xxxx::/80` 上, 其中 `xxxx` 根据 
[RFC 6296](https://tools.ietf.org/html/rfc6296#section-3.6) 计算. 

为了保持改写后的地址在 entropy 中会被正确地路由到 V, tcouple 在 `V::/64` 选取的的地址有限制. 
约定 V 在 entropy 中的地址空间中, 
以 `333a` 作为连接到该子网的地址, 于是要求 `V:xxxx::/80` 地址空间里, tcouple 使用地址 
`V:xxxx:333a::/96`. 

参照 [tinc 官方样例](https://www.tinc-vpn.org/examples/ipv6-network/)令 tcouple 
占用 `V:xxxx:333a::/96`, 节点使用 8 位 `nn` 标记, 即使用 `V:xxxx:333a:nn00::/104` 
作为 `nn` 节点的子网地址, 并且以 `V:xxxx:333a::nn` 作为 `nn` 节点在 tcouple 中监听的地址. 

## iptables 设置 ##
需要用 iptables 将 `V:xxxx:333a::/96` 发往 entropy 的地址, 在 V 上转化为 V 在 entropy 中子网 
`T:babe:3330::/92` 的地址. 在保证 `xxxx` 的选择满足 TFC 6296 的情况下, 使用以下命令即可: 

```
ip6tables -tmangle -A POSTROUTING -s V:xxxx:333a::/96 -d T:babe::/80 -j SNPT \
    --src-pfx V::/64 --dst-pfx T::/64
ip6tables -tmangle -A PREROUTING -d T:babe:333a::/96 -s T:babe::/80 -j DNPT \ 
    --src-pfx T::/64 --dst-pfx V::/64 
```

其中第一条将 tcouple 中发往 entropy 的包, 把前缀从 `V` 改成 `T` 从而表现为 entropy 中的 V 节点发出的包; 
第二条将 entropy 中标记为 `333a` 也即 V 节点被划分给 tcouple 的自网段的包, 把前缀从 `T` 改回 `V` 从而回到 
tcouple 网中. 

对于 V 之外 tcouple 的节点, 额外写入路由表, 将访问 `T::/64` 的数据发送到 V, 以满足按照 entropy 的路由访问的目的: 

```
ip -6 route add T:babe::/80 via V:xxxx:333a::[label of V]
```

或者对于 Mac 以及没有 `ip` 命令支持的老旧系统, 
```
route add -inet6 -prefixlen 80 T:babe:: V:xxxx:333a::[label of V]
```