import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')


