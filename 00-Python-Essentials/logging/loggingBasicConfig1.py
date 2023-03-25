import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息', stack_info=True)
logging.critical('Critical 级别日志信息')

# logging.log(logging.INFO, 'Info 级别日志信息')


def mylog(message, level='INFO'):
    level = {'NOTSET': logging.NOTSET,
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL}[level]
    logging.log(level, message)

mylog('Info 级别日志信息', 'INFO')