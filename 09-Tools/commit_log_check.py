#!/usr/bin/python3

# --------------------------------------------------------------------#
# Copyright (C), 1998-2023, Tenda Tech. Co., Ltd.
# FileName: testcaseGenarate.py
# Author:   zhanghaiyong
# Email: zhanghaiyong@tenda.cn
# Version:  V0.1
# FirstBuild: 2023-02-15
# LastChange: 2023-02-15
# Description:   log日志检查
#
# History:
#   <author> <time> <version > <desc>
#   zhanghaiyong  2023-02-15 V0.1
# --------------------------------------------------------------------#

import re
import argparse

class ArgParser():
    """
    读取输入参数
    """
    def __init__(self):
        self.usage = "检查提交日志格式是否符合要求"

    def arg_parser(self):
        parser    = argparse.ArgumentParser(description = self.usage)
        # 添加参数
        parser.add_argument("-m", "--message", help = "提交日志")
        args      = parser.parse_args()
        self.log  = args.message

class Log_Check(ArgParser):
    def __init__(self):
        super().__init__()
        self.LogList = []

    # 对log日志中的[]对数进行检查
    def strLensCheck(self):
        if len(self.LogList) == 6:
            return True
        else:
            StrLensError = 'Log日志中的[]数量应为6对，请检查'
            print(StrLensError)
            exit()

    def startLogCheck(self):
        print("##########################")
        print("# 开始日志检查")
        self.LogList = [part.strip() for part in re.split('[\[\]]', self.log) if part.strip()]
        # 检查Log中的'[]'对数是否满足6条
        self.strLensCheck()

        if 'Bugid' in self.LogList[3] or 'bugid' in self.LogList[3]:
            print("# Bugid检查通过")
        else:
            print("当前log Bugid字段错误,请修改")
            print("无Bugid时填写：[Bugid:]")
            print("有Bugid时填写：[Bugid:100]")
            exit()

        print("# 结束日志检查")
        print("##########################")

if __name__ == '__main__':
    lc = Log_Check()
    lc.arg_parser()
    # args = '[方案导入] [系统安全][子节点] [田主:熊相权][bugid：][原厂 patch：][bcm6750_6715_11ax_mesh] [MX15V1.0][钟博]'
    lc.startLogCheck()
