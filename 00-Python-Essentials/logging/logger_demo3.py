import logging
import logging.config
import os

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
confname = os.path.join(abspath, 'config.conf')

logging.config.fileConfig(fname=confname, disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.debug('This is a debug message')