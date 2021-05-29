---
title: 报文构造、解析脚本说明
date: 2021-01-07
update: 2021-05-12
author: zhanghaiyong
version:  v1.1
tags:
	- scapy
	- 报文构造
	- 报文解析
    - tshark
categories: 
---
# 报文构造、解析脚本说明

本文档介绍报文构造（buildpkt.py）和解包（parserPacket.py）脚本的使用方法，DHCPv6报文构造（Linux）、报文解析（windows和Linux）相关关键字已经集成到ATTrobot平台，相关文件已上传到ATTrobot平台项目的demo目录中，大家可以对脚本进行改进上传。

## 目录

- [背景](#背景)
- [环境](#环境)
- [使用说明](#使用说明)
	- [报文构造发送](#报文构造发送)
	- [报文解析](#报文解析)
- [示例](#示例)
	- [报文构造发送](#报文构造发送)
	- [报文解析](#报文解析)
- [ATTrobot平台使用](#ATTrobot平台使用)
	- [断言](#断言)
- [其它说明](#其它说明)


## 背景
1. IPv6相关协议测试需要构造特定选项字段的报文，测试DUT设备的协议一致性。
2. 大量测试用例需要对报文进行解析，检查目标字段或者协议。

## 环境
脚本主要使用Python语言进行开发，主要环境如下：
```text
1. 支持Python 2.7 和 Python 3 (3.4 to 3.8)
2. scapy==2.4.4
3. Windows or Linux
4. wireshark（需要wireshark的命令行工具tshark）
```
### scapy
报文构造主要使用python scapy库。
- 官网：[https://scapy.net/](https://scapy.net/)
- github地址：[https://github.com/secdev/scapy](https://github.com/secdev/scapy)
- 官方文档：[https://scapy.readthedocs.io/en/latest/](https://scapy.readthedocs.io/en/latest/)

安装：
```python
pip install scapy
```
### tshark
解包需要使用wireshark提供的命令行工具tshark，在windows系统中也可以使用tshark进行抓包，windows中安装完成wireshark后，将安装目录添加到环境变量。

wireshark下载安装
wireshark官网：[https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)

centos安装：
```bash
yum -y install wireshark
```
tshark参考文档：[https://www.wireshark.org/docs/man-pages/tshark.html](https://www.wireshark.org/docs/man-pages/tshark.html)

## 使用说明
查看帮助文档

```sh
$ python buildpkt.py -h
$ python parserpacket.py -h
```
### 报文构造发送
```sh
$ python buildpkt.py [OPTION...]
```

|  参数  |   说明   |   示例   |
| ---- | ---- | ---- |
| -P, --Protocol  |  协议名称，不区分大小写  |   dhcpv6, icmpv6   |
| -p, --package  |   报文文件，默认/tmp/packet.pcap   |      |
| -m, --message  |  报文类型，不区分大小写  |  Solicit, Request等    |
| -l, --layer  |  报文层名称，不区分大小写  |  ether, ip, ipv6    |
| -I, --iface  |  报文发送接口    |  eth1  |
| -c, --count  |  发送报文次数，默认发送一个报文  |      |
| -h, --help  |  帮助信息   |      |


### 报文解析
```sh
$ python parserpacket.py [OPTION...]
```
提供两种方法：tshark解析和scapy解析，建议使用tshark方法。

|  参数  |   说明   |   示例   |
| ---- | ---- | ---- |
| -P, --Protocol  |  协议名称，不区分大小写（**用于scapy解包方法**）  |   dhcpv6, icmpv6   |
| -p, --package  |   报文文件，默认/tmp/packet.pcap（**用于scapy解包方法**）   |      |
| -m, --message  |  报文类型，不区分大小写（**用于scapy解包方法**）  |  Solicit, Request等    |
| -F, --field |  报文字段，多个条件使用","分隔（**用于scapy解包方法**）  | -F dst='ff02::1:2' |
| -f, --filter | 过滤条件，多个条件使用","分隔 | -f dhcpv6.msgtype=1 |
| -Y, --display-filter | 报文过滤条件，只处理符合条件的报文，多个条件使用","分隔 | -Y dhcpv6.msgtype==1 |
| -r, --return_flag | 是否返回字段值，默认不返回，仅查找 | -r 1 |
| -c, --count  |  预期匹配数，默认1次  |      |
| -h, --help  |  帮助信息   |      |


## 示例
### 报文构造发送
#### 构造并发送DHCPv6 Solicit报文
设置ether层、ipv6层源地址、目的地址。

```sh
$ python buildpkt.py -P dhcpv6 -m solicit -I eth1 -l ether,dst=ff:ff:ff:ff:ff:ff,src=00:0c:29:d9:98:c7 -l ipv6,dst=ff02::1:2,src=fe80::20c:29ff:fed9:98c7
```
默认添加Client Identifier Option、IA_NA Option。如果要修改或者添加option，使用 `-o` 参数，多个字段仍然用逗号隔开。

#### 构造并发送DHCPv6 Request报文
注意：Request报文需要服务器发送的Advertise报文相关Option，所以构造发送Request报文前，首先发送一个Solicit报文，抓取并保存服务器返回的报文。
```sh
$ python buildpkt.py -P dhcpv6 -m request -I eth1 -l ether,dst=33:33:00:01:00:02,src=00:0c:29:d9:98:c7 -l ipv6,dst=ff02::1:2,src=fe80::20c:29ff:fed9:98c7 -p /tmp/packet.pcap -o iaaddress,addr=ffff::
```
`-p` 指定需要读取的报文文件


### 报文解析
#### 方法1：tshark方法解包
过滤条件可以在wireshark中获取，默认解析/tmp/packet.pcap
```sh
# 查找DHCPv6_Solicit报文
$ python parserpacket.py -f dhcpv6.msgtype=1
# 查找目的MAC地址为ff02::1:2的DHCPv6_Solicit报文
$ python parserpacket.py -f ipv6.dst=ff02::1:2 -Y dhcpv6.msgtype==1 
$ python parserpacket.py -f ipv6.dst=ff02::1:2 -Y dhcpv6.msgtype==1,ipv6.dst=ff02::1:2 
```
`-f` 参数对应tshark工具中的`-e`参数，`-Y` 参数对应tshark工具中的`-Y`参数，tshark参考文档：[https://www.wireshark.org/docs/man-pages/tshark.html](https://www.wireshark.org/docs/man-pages/tshark.html)

> **注意**：
>
> 1. `-f` 参数字段值可以使用“=”或者`==`连接value值，多个条件用`,`隔开，不要使用多个`-f`参数。也可以不指定value值，仅用于检查是否存在这个字段，不判断值是否正确。
> 2. `-Y` 参数只能使用`==`连接，同wireshark中获取到的相同，多个条件用`,`隔开，不要使用多个`-Y`参数。
> 3. 过滤条件不要有空格，即使加上引号也不行，因为代码在数据预处理时去掉了引号。

#### 方法2：scapy解包
脚本也提供了scapy解包方法，建议使用tshark方法。

检查目的MAC为00:0c:29:d9:98:c7的DHCPv6 Solicit报文

```sh
$ python parserpacket.py -P dhcpv6 -m solicit -F dst=00:0c:29:d9:98:c7 -p /tmp/packet.pcap
```


## ATTrobot平台使用
抓包和解包已经在Attrobot平台测试，抓包和解包都在虚拟机中完成，使用RF的SSHLibrary库实现脚本执行。虚拟机中建议将脚本存放在 `/var/tendatest/TDT/script/` 目录下

centos中解包使用**PktParser**关键字。

windows系统中解包使用**PktParser windows**关键字。

### 断言

构造发送报文通过检查是否出现 `Sent 1 packets.`判断是否发送成功

对于解包，匹配成功会打印 `PASS` ，否则打印 `FAIL`

只有一个过滤条件的情况下，如果匹配条件大于等于预期匹配数，打印`PASS`

如果有多个条件，需要都满足才会打印`PASS` ，示例：
```sh
字段 dhcpv6.msgtype=3 匹配成功1次
字段 ipv6.dst=ff02::1:2 匹配成功1次
所有字段匹配成功1次
PASS
```
通过断言打印的是PASS或者FAIL来判断是否通过测试。

## 其它说明
1. 目前报文构造脚本只添加了部分option，需要添加其它option需新增相关函数。
2. 除了DHCPv6报文，其它类型协议报文可以通过在**PktBuild**和**LayerOptionBuild**类中添加相关协议函数。目前包括了Ethernet II、IPv6、UDP、DHCPv6、DHCP6OptClientId、DHCP6OptServerId、DHCP6OptIA_NA、DHCP6OptIAAddress、DHCP6OptDNSServers等报文层和关键字。

ls()：查看支持的协议:
截取部分：
```sh
>>> ls()
DHCP       : DHCP options
DHCP6      : DHCPv6 Generic Message
DHCP6OptAuth : DHCP6 Option - Authentication
DHCP6OptBCMCSDomains : DHCP6 Option - BCMCS Domain Name List
DHCP6OptBCMCSServers : DHCP6 Option - BCMCS Addresses List
DHCP6OptBootFileUrl : DHCP6 Boot File URL Option
DHCP6OptClientArchType : DHCP6 Client System Architecture Type Option
DHCP6OptClientFQDN : DHCP6 Option - Client FQDN
DHCP6OptClientId : DHCP6 Client Identifier Option
DHCP6OptClientLinkLayerAddr : DHCP6 Option - Client Link Layer address
DHCP6OptClientNetworkInterId : DHCP6 Client Network Interface Identifier Option
DHCP6OptDNSDomains : DHCP6 Option - Domain Search List option
DHCP6OptDNSServers : DHCP6 Option - DNS Recursive Name Server
DHCP6OptERPDomain : DHCP6 Option - ERP Domain Name List
```

查看某个报文层、Option字段
```sh
>>> ls()
>>> ls(IPv6)
version    : BitField  (4 bits)                  = (6)
tc         : BitField  (8 bits)                  = (0)
fl         : BitField  (20 bits)                 = (0)
plen       : ShortField                          = (None)
nh         : ByteEnumField                       = (59)
hlim       : ByteField                           = (64)
src        : SourceIP6Field                      = (None)
dst        : DestIP6Field                        = (None)

>>> ls(DHCP6OptClientId)
optcode    : ShortEnumField                      = (1)
optlen     : FieldLenField                       = (None)
duid       : _DUIDField                          = ('')
```


<center><b>--THE END--<b></center>

