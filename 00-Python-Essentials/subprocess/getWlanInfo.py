#-*-coding:utf-8-*-
# @Time:    2023/03/04 21:12
# @Author:  hiyongz
# @File:    getWlanInfo.py
# @description: 读取无线网卡信息
# 执行方式：python getWlanInfo.py -d 30 -n 6

import datetime
import logging
import os
import argparse
from time import sleep

class ArgParser():
    """读取输入参数

    """
    def __init__(self):
        self.usage = "读取无线网卡信息"

    def arg_parser(self):
        self.parser = argparse.ArgumentParser(description = self.usage)
        # 添加参数
        self.parser.add_argument("-i", "--iface", help = "网卡名称")
        self.parser.add_argument("-d", "--duration", help = "读取时间，单位秒", default=30)
        self.parser.add_argument("-n", "--number", help = "读取次数", default=6)
        self.parser.add_argument("-p", "--path", help = "日志保存路径")
        args          = self.parser.parse_args()
        self.iface    = args.iface
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

class wlanInfo(Loggers):
    def __init__(self):
        super().__init__()
        self.logger = Loggers().myLogger()
        
        self.get_intf       = 'netsh wlan show interface | findstr /I "名称 name"'
        self.show_chkrate_r = 'netsh wlan show interface | findstr /I "接收速率(Mbps) Receive"'
        self.show_chkrate_s = 'netsh wlan show interface | findstr /I "传输速率 (Mbps) Transmit"'
        self.show_signal    = 'netsh wlan show interface | findstr /I "信号 Signal"'
        self.iface = self.__hardware_info(self.get_intf)

    def __hardware_info(self, command):
        """获取windows无线相关的信息，此方式仅用于获取netsh wlan show interface回显的相关值。

        :param command:获取命令
        :return:命令回显值
        """
        hardwareinfo = self.__sendcommand_with_windows(command)
        if len(hardwareinfo) > 2:
            result_info = hardwareinfo.split()[-1]
        else:
            result_info = None
        return result_info

    def __sendcommand_with_windows(self, command):
        """向PC发送命令并返回回显信息。

        :command: 将要发送的命令
        :return info: 回显消息
        """
        info = os.popen(command).read()
        return info

    def __chcek_wireless(self):
        """检查无线网卡 物理连接状态，既：是否准备就绪。

        """
        init_statue = self.__hardware_info(self.get_intf)
        if init_statue is None:
            return False
        return True

    def __get_median(self, data):
        if data[0]:
            data.sort()
            half = len(data) // 2
            return (data[half] + data[~half]) / 2
        return 0

    def wifi6_getrate_r(self):
        """返回无线的接收速率

        :return chkrate_recv: 接收速率
        """
        if self.__chcek_wireless():
            chkrate_recv = self.__hardware_info(self.show_chkrate_r)
            self.logger.info("Receive rate (Mbps): %s"%chkrate_recv)
            if chkrate_recv:
                return float(chkrate_recv)
        return False

    def wifi6_getrate_s(self):
        """返回无线的传输速率

        :return chkrate_send: 传输速率
        """
        if self.__chcek_wireless():
            chkrate_send = self.__hardware_info(self.show_chkrate_s)
            self.logger.info("Transmit rate (Mbps): %s"%chkrate_send)
            if chkrate_send:
                return float(chkrate_send)
        return False

    def wifi6_getsignal(self):
        """返回无线的信号强度

        :return wireless_signal: 信号强度
        """
        self.__chcek_wireless()
        wireless_signal = self.__hardware_info(self.show_signal)
        self.logger.info("Signal: %s"%wireless_signal)
        if wireless_signal:
            signal = wireless_signal.replace('%', '')
            return float(signal)

    def getInfo(self):
        """在指定时间内多次读取信号无线网卡信息
        
        :param duration: 读取时间，单位秒，正整数
        :param num: 读取次数

        :return wireless_signal: 信号强度
        """
        num       = self.num
        duration  = self.duration
        time_step = int(duration)/int(num)

        rate_recv_list = []
        rate_send_list = []
        signal_list    = []
        # rate_recv_sum  = 0
        # rate_send_sum  = 0
        # signal_sum  = 0
        self.logger.info("\n")
        self.logger.info("开始读取无线网卡数据")
        for i in range(int(num)):
            if i == int(num)-1:
                break
            else:
                sleep(time_step)
                i1 = i+1
                self.logger.info("第%s次读取无线网卡数据"%i1)
                rate_recv = self.wifi6_getrate_r()
                rate_send = self.wifi6_getrate_s()
                signal    = self.wifi6_getsignal()
                rate_recv_list.append(rate_recv)
                rate_send_list.append(rate_send)
                signal_list.append(signal)
                # rate_recv_sum += rate_recv
                # rate_send_sum += rate_send
                # signal_sum += signal
                # now = now + time_step
        # rate_recv_avg = rate_recv_sum/(int(num)-1)
        # rate_send_avg = rate_send_sum/(int(num)-1)
        # signal_avg = signal_sum/(int(num)-1)
        # print("%s,%s,%s"%(rate_recv_avg,rate_send_avg,signal_avg))
        rate_recv_med = self.__get_median(rate_recv_list)
        rate_send_med = self.__get_median(rate_send_list)
        signal_med = self.__get_median(signal_list)
        print("%s,%s,%s"%(rate_recv_med,rate_send_med,signal_med))


if __name__ == "__main__":
    wlan = wlanInfo()
    wlan.getInfo()




