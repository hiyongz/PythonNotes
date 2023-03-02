import logging
import os

# Create a custom logger
logger  = logging.getLogger(__name__)

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
logname = os.path.join(abspath, 'file.log')

# Create handlers
console_handler = logging.StreamHandler() # 输出到控制台
file_handler    = logging.FileHandler(logname) # 输出到文件
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format    = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
logger.warning('Warning 级别日志信息')
logger.error('Error 级别日志信息')
logger.critical('Critical 级别日志信息')