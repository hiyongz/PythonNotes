import datetime
import os
import logging
 
class Loggers(object):
    """
    日志记录
    """ 
    def __init__(self, log_level = logging.INFO, log_dir = 'log', fmt = '%(asctime)s - %(levelname)s: %(message)s'):
        filename = 'log_' + datetime.datetime.now().strftime('%Y%m%d-%H-%M') + '.log'
        abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
        logpath = os.path.join(abspath, log_dir) # 日志保存路径
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        logname = os.path.join(logpath, filename)

        self.logger = logging.getLogger("fatherModule")
        format_str  = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(log_level)  # 设置日志级别

        stream_handler = logging.StreamHandler()  # 输出到控制台
        stream_handler.setFormatter(format_str)

        file_handler = logging.FileHandler(logname, mode='a') # 输出到文件
        file_handler.setFormatter(format_str)
        
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
 
if __name__ == "__main__":
    txt = "demo"
    log = Loggers()
    log.logger.info(4)
    log.logger.info(5)
    log.logger.info(123,txt)