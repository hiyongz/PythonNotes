#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import time
from concurrent.futures import ThreadPoolExecutor
import paramiko
 
 
def get_device_list(filename):
    """从文本文件读取设备列表，返回由字典组成的列表。
    文本内容格式为：ip，用户名，密码，别名，例如：
    1.1.1.1 admin admin sw1
    1.1.1.2 admin admin sw2
    ......
    
    Args:
        filename ([str]): 文件名称
    """
    with open(filename, 'r') as f:
        device_list = []
        for line in f.readlines():
            ip, username, password, name = line.strip().split()
            device_list.append(
                {
                    "ip": ip,
                    "username": username,
                    "password": password,
                    "name": name,
                }
            )
    return device_list
 
class NetworkDevice(object):
    def __init__(self, ip="", username="", password="'", name="", port=22,):
        self.conn = None
        if ip:
            self.ip = ip.strip()
        elif name:
            self.name = name.strip()
        else:
            raise ValueError("需要设备连接地址（ip 或 别名）")
        self.port = int(port)
        self.username = username
        self.password = password
        self._open_ssh()
    
    def _open_ssh(self):
        """初始化 SSH 连接，调起一个模拟终端，会话结束前可以一直执行命令。
 
        Raises:
            e: 抛出 paramiko 连接失败的任何异常
 
        """
        ssh_connect_params = {
            "hostname": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "look_for_keys": False,
            "allow_agent": False,
            "timeout": 5,   # TCP 连接超时时间
        }
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            conn.connect(**ssh_connect_params)
        except Exception as e:
            raise e
        self.conn = conn.invoke_shell(term="vt100", width=500, height=1000)
        return ""
 
    def exec_cmd(self, cmd, recv_time=3):
        """登录设备，执行命令
 
        Args:
            cmd ([type]): 命令字符串
            recv_time (int, optional): 读取回显信息的超时时间. Defaults to 3.
 
        Raises:
            EOFError: 没有任何信息输出，说明连接失败。
 
        Returns:
            output:
        """
        cmd = cmd.strip() + "\n"
        self.conn.sendall("screen disable\n")
        self.conn.sendall(cmd)
        time.sleep(int(recv_time))
        output = self.conn.recv(1024*1024)
        if len(output) == 0:
            raise EOFError("连接可能被关闭，没有任何信息输出")
        return output.decode('utf-8', 'ignore')
 
 
dev = {
    "ip":"192.168.56.21",
    "username":"netdevops",
    "password":"Admin@h3c.com",
    "name": "sw1"
}
# sw1 = NetworkDevice(**dev)
# ret = sw1.exec_cmd("dis version")
# print(ret)