import logging

logging.basicConfig(level=logging.DEBUG, filename='D:/ProgramWorkspace/PythonNotes/00-Python-Essentials/logging/test.log', filemode='a', format='%(asctime)s - %(created)f - %(relativeCreated)d - %(msecs)d - %(name)s - %(filename)s - %(funcName)s - %(module)s - %(pathname)s - %(levelname)s - %(levelno)s - %(message)s')

logging.debug('Debug 级别日志信息')
logging.info('Info 级别日志信息')
logging.warning('Warning 级别日志信息')
logging.error('Error 级别日志信息')
logging.critical('Critical 级别日志信息')

def demo():
    logging.critical('Critical 级别日志信息')
demo()