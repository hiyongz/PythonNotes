#!/usr/bin/python3

import datetime
import logging
import os
import argparse


class ArgParser():
    """
    读取输入参数
    """
    def __init__(self):
        self.usage = "检查衰减仪串口配置是否成功"

    def arg_parser(self):

        parser = argparse.ArgumentParser(description = self.usage)
        # 添加参数
        parser.add_argument("-p", "--path", help = "串口日志文件")
        parser.add_argument("-t", "--time", help = "串口设置时间")
        parser.add_argument("-e", "--expe", help = "预期参数，eg: C,10", action='append')
        args          = parser.parse_args()
        self.logpath = args.path
        self.dtime    = args.time
        self.expe     = args.expe

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

class logCheck(Loggers):
    def __init__(self):
        super().__init__()
        self.logger = Loggers().myLogger()

    def br121_should_be_success(self,logpath, time, target):
        """br121-C衰减仪串口设置成功

        :logpath: 串口日志文件
        :time: 串口设置时间
        :target: 预期参数，eg: C,10
        """
        logpath = self.logpath
        time    = self.dtime
        target  = self.expe
        if  not os.path.exists(logpath):
            log_data = '文件 ' + logpath + ' 不存在'
            raise RuntimeError(log_data)
        
        tim = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") 
        time_after  = tim + datetime.timedelta(seconds=1)  # 加1s
        time_before = tim + datetime.timedelta(seconds=-1) # 减1s
        tim         = str(tim)
        time_after  = str(time_after)
        time_before = str(time_before)
        read_f  = next(self._read_log_file(logpath)) # 读取脚本文件
        read_f.reverse() # 倒序，从后往前读

        ########## 读取对应时间的串口打印 ############
        msg = self._get_attenuation(read_f, tim, time_before)
        if len(msg) == 0:
            msg = self._get_attenuation(read_f, time_after, time_before) # 读取后1s的串口日志

        ########## 判断是否设置成功 ############
        if len(msg) == 0:
            raise RuntimeError("没有设置成功，请重新发送命令")

        channel_attenuation = target.strip().split(',')
        channel             = channel_attenuation[0]
        attenuation         = channel_attenuation[1]
        expe                = channel + ',attenuation:' + attenuation + 'dB'
        if expe in msg:
            self.logger.info("设置成功! %s"%expe)
        else:
            raise RuntimeError("没有设置成功，请重新发送命令")

    def _read_log_file(self, logpath):
        """读取日志文件
        :param logpath: 串口日志文件
        :return: 无
        """
        with open(logpath,'r',encoding='gbk') as f:
            line = f.readlines()
            yield line
    
    def _get_attenuation(self, lines, datetime, datetime_before):
        """读取时间对应的衰减值
        :param lines: 日志信息
        :param datetime: 时间
        :param datetime_before: datetime前1s
        :return: msg
        """
        for line in lines:
            msg = line.strip()
            timestr        = '[' + datetime + ']'
            timestr_before = '[' + datetime_before + ']'
            if timestr in msg and ',' in msg:
                return msg
            if timestr_before in msg:
                return ''
        return ''

if __name__ == "__main__":
    lc = logCheck()
    lc.testcase_generate()
