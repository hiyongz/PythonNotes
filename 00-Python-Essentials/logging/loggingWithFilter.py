import logging
import sys
import os


class failureFilter(logging.Filter):
    def filter(self, record):
        # for attr in [a for a in dir(record) if not a.startswith('__')]:
        #     print(f'{attr}: {getattr(record, attr)}')

        if 'Failure' in record.msg:
            return True
        return False
        # return not record.getMessage().startswith('parsing')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
logname = os.path.join(abspath, 'file.log')

# 创建处理器 handlers
console_handler = logging.StreamHandler(stream=sys.stdout) # 输出到控制台
file_handler    = logging.FileHandler(logname) # 输出到文件
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)

# 添加filter
loggingFiletr = failureFilter()
console_handler.addFilter(loggingFiletr)
file_handler.addFilter(loggingFiletr)

# 创建格式器
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')
file_format    = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y%m%d-%H:%M:%S')

# 将格式器添加到处理器中
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# 将处理器添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info('Info 级别日志信息')
logger.error('Failure')

