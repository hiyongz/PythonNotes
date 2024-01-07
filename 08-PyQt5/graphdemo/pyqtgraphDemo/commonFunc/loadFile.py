

import logging
import os
import yaml


class LoadFile:
    def __init__(self):
        self.logger = logging.getLogger("fatherModule.son.module")

    def loadConfig(self):
        abspath = os.getcwd() # 项目路径
        logpath = os.path.join(abspath, "config/config.yaml") # 日志保存路径
        self.logger.info("加载配置文件")
        with open(logpath, encoding="utf-8") as f:
        # steps = yaml.safe_load(f)
            config = yaml.safe_load(f)
        return config