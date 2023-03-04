import logging
import logging.config
import os

abspath = os.path.dirname(os.path.abspath(__file__)) 
confpath = os.path.join(abspath, 'logging.conf')

if os.path.exists(confpath):
    logging.config.fileConfig(fname=confpath, disable_existing_loggers=False)

# create logger
logger = logging.getLogger("mylogger")

logger.debug('Debug 级别日志信息')
logger.info('Info 级别日志信息')
logger.warning('Warning 级别日志信息')
logger.error('Error 级别日志信息')
logger.critical('Critical 级别日志信息')
