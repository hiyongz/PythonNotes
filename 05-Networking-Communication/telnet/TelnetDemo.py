#-*-coding:utf-8-*-
# @Time:    2023/03/04 21:12
# @Author:  hiyongz
# @File:    getCpuIdle.py
# @description: 读取DUT CPU idle数据
# 执行方式：python getCpuIdle.py -d 30 -n 6

import datetime
import json
import logging
import os
import argparse
import sys
import requests
import telnetlib
from time import sleep

class ArgParser():
    """读取输入参数

    """
    def __init__(self):
        self.usage = "读取无线网卡信息"

    def arg_parser(self):
        self.parser = argparse.ArgumentParser(description = self.usage)
        # 添加参数
        self.parser.add_argument("-d", "--duration", help = "读取时间，单位秒", default=5)
        self.parser.add_argument("-n", "--number", help = "读取次数", default=3)
        self.parser.add_argument("-p", "--path", help = "日志保存路径")
        args          = self.parser.parse_args()
        self.duration = args.duration
        self.num      = args.number
        self.logpath  = args.path
        

class Loggers(ArgParser):
    """日志记录器

    记录日志，支持命令行窗口和保存到文件。
    Attributes:
        console_level: 输出到控制台最低的日志严重级别
        file_level: 保存到文件最低的日志严重级别
        fmt: 日志格式化输出样式
        datefmt: 时间格式化
    """
    def __init__(self, console_level = logging.INFO, file_level = logging.INFO, fmt = '%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y%m%d-%H:%M:%S'):
        super().__init__()
        self.arg_parser()
        self.filename = 'wlan-log_' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        
        self.fmt      = fmt
        self.datefmt  = datefmt
        self.console_level = console_level
        self.file_level    = file_level
    
    def myLogger(self):
        # 创建自定义 logger
        logging.root.setLevel(logging.NOTSET)
        self.logger = logging.getLogger(__name__)

        if self.logpath:
            logpath = self.logpath
        else:
            abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
            logpath = os.path.join(abspath, 'log') # 日志保存路径
            if not os.path.exists(logpath):
                os.mkdir(logpath)
        self.logname  = os.path.join(logpath, self.filename)

        # 创建处理器 handlers
        # console_handler = logging.StreamHandler() # 输出到控制台
        file_handler    = logging.FileHandler(self.logname, mode='a') # 输出到文件
        # console_handler.setLevel(self.console_level)
        file_handler.setLevel(self.file_level)

        # 设置日志格式
        format_str  = logging.Formatter(self.fmt, self.datefmt)  # 设置日志格式
        # 将格式器添加到处理器中
        # console_handler.setFormatter(format_str)
        file_handler.setFormatter(format_str)

        # 将处理器添加到logger
        # self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        return self.logger

class Telnet():
    """Telnet相关操作

    """
    def __init__(self):
        self.host     = '192.168.0.1'
        self.username = 'root'
        self.pwd      = 'ZWN3NGVuU1BfMjM0MGM3'
        self.timeout  = 3

    def connect(self):
        """telnet连接

        :return self: 返回self
        """
        self.tn = telnetlib.Telnet(self.host, port=23, timeout=self.timeout)
        return self

    def login(self):
        """telnet登录

        :return self: 返回self
        """
        self.tn.read_until(b'login: ', timeout=self.timeout)
        self.tn.write(self.username.encode('utf-8') + b'\n')
        self.tn.read_until(b'Password: ', timeout=self.timeout)
        self.tn.write(self.pwd.encode('utf-8') + b'\n')
        self.tn.read_until(b'~ #', timeout=self.timeout)
        return self

    def write(self, cmd):
        """发送命令

        :return self: 返回self
        """
        self.tn.write(cmd.encode('utf-8') + b'\n')
        return self

    def read(self):
        """读取返回值

        :return out: 命令返回信息
        """
        out = self.tn.read_until(b'~ #', timeout=self.timeout).decode('utf-8')
        return out.strip()

    def close(self):
        """终止Telnet连接

        :return : 无
        """
        self.tn.close()

class cpuInfo(Loggers):
    """读取DUT CPU信息

    """
    def __init__(self):
        super().__init__()
        self.logger = Loggers().myLogger()

        self.tn = Telnet()
        self.tn.connect().login()
        self.logger.info("登录DUT telnet成功")

        self.cmd_cpuIdle = "top -bn 1 | grep idle | grep -v grep | awk '{print $10}'"

    def __get_median(self, data):
        if data[0]:
            data.sort()
            half = len(data) // 2
            return (data[half] + data[~half]) / 2
        return 0

    def get_cpuIdle(self):
        """返回DUT CPU Idle值

        :return cpuIdle: CPU Idle值
        """
        cpuIdle = self.tn.write(self.cmd_cpuIdle).read()
        cpuIdle = cpuIdle.replace(self.cmd_cpuIdle, '')
        cpuIdle = cpuIdle.replace('~ #', '').replace('%', '')
        cpuIdle = cpuIdle.strip()
        return float(cpuIdle)

    def getCpuInfo(self):
        """在指定时间内多次读取DUT CPU信息并计算平均值
 
        """
        num       = self.num
        duration  = self.duration
        time_step = int(duration)/int(num)

        # cpuIdle_list = []
        cpuIdle_sum  = 0
        self.logger.info("\n")
        self.logger.info("开始读取CPU数据")
        for i in range(int(num)):
            if i == int(num)-1:
                break
            else:
                sleep(time_step)
                i1 = i+1
                
                cpuIdle = self.get_cpuIdle() 
                self.logger.info("第%s次读取 CPU IDLE 值: %s"%(i1,cpuIdle))
                # cpuIdle_list.append(cpuIdle)
                cpuIdle_sum += cpuIdle
        self.tn.close()
        cpuIdle_avg = cpuIdle_sum/(int(num)-1)
        print("%s"%(cpuIdle_avg))
        # rate_recv_med = self.__get_median(rate_recv_list)
        # rate_send_med = self.__get_median(rate_send_list)
        # signal_med = self.__get_median(signal_list)

if __name__ == "__main__":
    ci = cpuInfo()
    ci.getCpuInfo()




