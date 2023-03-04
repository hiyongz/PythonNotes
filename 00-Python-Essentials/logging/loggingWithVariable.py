import logging

FORMAT = '%(asctime)s - %(clientip)s - %(message)s'
logging.basicConfig(format=FORMAT)
clientip = '192.168.0.1'
d = {'clientip':clientip}

logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息', extra=d)

