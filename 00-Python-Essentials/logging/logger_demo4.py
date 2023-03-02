import logging
import logging.config
import os
import yaml

abspath = os.path.dirname(os.path.abspath(__file__)) # 脚本绝对路径
confname = os.path.join(abspath, 'config.yaml')

with open(confname, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')