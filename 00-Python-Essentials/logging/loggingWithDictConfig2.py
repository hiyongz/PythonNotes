import logging
import logging.config
import os
import json

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
confpath = os.path.join(abspath, 'logging.json')

if os.path.exists(confpath):
    with open(confpath, 'r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger("mylogger")

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
logger.warning('Warning 级别日志信息')
logger.error('Error 级别日志信息')
logger.critical('Critical 级别日志信息')