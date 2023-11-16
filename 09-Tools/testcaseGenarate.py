#!/usr/bin/python3

# --------------------------------------------------------------------#
# Copyright (C), 1998-2022, Tenda Tech. Co., Ltd.
# FileName: testcaseGenarate.py
# Author:   zhanghaiyong
# Email: zhanghaiyong@tenda.cn
# Version:  V0.1
# FirstBuild: 2022-11-16
# LastChange: 2022-11-17
# Description:   生成待测自动化用例
#
# History:
#   <author> <time> <version > <desc>
#   zhanghaiyong  2022-11-16 V0.1
# --------------------------------------------------------------------#

import os
import re
import argparse
import shutil

# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 

class ArgParser():
    """
    读取输入参数
    """
    def __init__(self):
        self.usage = "基于源自动化脚本，根据测试用例ID整理要执行的自动化用例"

    def arg_parser(self):

        parser = argparse.ArgumentParser(description = self.usage)
        # 添加参数
        parser.add_argument("-p", "--path", help = "自动化脚本路径，eg: D:/testcase/EW3000G/01_测试套件")
        parser.add_argument("-i", "--id", help = "要执行的测试用例ID", action='append')
        args          = parser.parse_args()
        self.codepath = args.path
        self.ids      = args.id
        # print('code path:' + self.codepath)
        # print('testcase ids:' + self.ids)

class TestcaseGen(ArgParser):
    def __init__(self):
        super().__init__()

    def parse_caseid(self):
        caseIDList = []
        for ids in self.ids:
            if ',' in ids:
                caseids     = ids.split(",")
                caseIDList += caseids
            else:
                caseIDList.append(ids)
        # caseIDList=list(set(caseIDList)) # 去重
        # caseIDList = ['31915','31916','31918','31945','31991']
        return caseIDList

    def read_robot_file(self, robot_file):
        """
        读取测试平台用例数据
        :param robot_file: 存放的测试平台用例所在的目录文件
        :return: 无
        """
        with open(robot_file,'r',encoding='utf-8') as f:
            line = f.readlines()
            yield line

    def testcase_generate0(self):
        """
        注释不执行的参数化用例（弃用）
        :return:
        """
        caseIDList = self.parse_caseid()
        # self.codepath = 'D:/testcase/EW3000GDemo/01_测试套件'        
        codebasename = os.path.basename(self.codepath)
        newcodepath  = os.path.dirname(self.codepath) + '/' + codebasename + '_temp'
        if os.path.exists(newcodepath):
            shutil.rmtree(newcodepath)
        # print('创建临时自动化用例目录:' + newcodepath)
        os.makedirs(newcodepath)

        for casefile_name in os.listdir(self.codepath):
            print(casefile_name)
            old_file  = self.codepath + '/' + casefile_name
            new_file  = newcodepath   + '/' + casefile_name
            temp_file = newcodepath   + '/temp_' + casefile_name
            print(temp_file)
            shutil.copy(old_file, temp_file)
            r_list = []
            read_f = next(self.read_robot_file(temp_file))
            for line in range(len(read_f)):
                msg = read_f[line].strip()
                if re.search(r"case_", msg):
                    casetitle = msg.split(" ")[0]
                    caseID = re.findall("_(\d+)$",casetitle)
                    if len(caseID) == 0 or caseID not in caseIDList:
                        r_list.append("#" + read_f[line])
                    else:
                        r_list.append(read_f[line])
                    print(caseID)
                    print(casetitle)  
                else:
                    r_list.append(read_f[line])

                with open(new_file,'w',encoding='utf-8') as write_f:
                    write_f.write("\n".join(r_list))
            os.remove(temp_file)

    def testcase_generate(self):
        """
        删除不执行的用例
        :return:
        """
        caseIDList = self.parse_caseid()
        # self.codepath = 'D:/testcase/EW3000GDemo/01_测试套件'
        
        codebasename = os.path.basename(self.codepath)
        newcodepath  = os.path.dirname(self.codepath) + '/' + codebasename + '_temp'
        if os.path.exists(newcodepath):
            shutil.rmtree(newcodepath)
        # print('创建临时自动化用例目录:' + newcodepath)
        os.makedirs(newcodepath)

        for casefile_name in os.listdir(self.codepath):
            # print(casefile_name)
            old_file  = self.codepath + '/' + casefile_name # 源脚本文件名
            new_file  = newcodepath   + '/' + casefile_name # 整理后的新脚本文件名
            temp_file = newcodepath   + '/temp_' + casefile_name # 临时脚本文件名
            # print(temp_file)
            shutil.copy(old_file, temp_file)
            r_list    = []  # 存储新脚本内容
            case_list = []  # 存储单条自动化用例
            case_dict = {'tiName':{'flag':0, 'status':0}, 'test':{'flag':0, 'status':-1}} # 初始标记, flag标记当前行是否属于参数化或者普通用例，status标记当前用例是否需要执行，case_dict['tiName']['status']表示当前参数化用例要执行的用例数，为0表示没有要执行的用例；case_dict['test']['status']为0表示当前用例不执行，为1表示要执行
            read_f    = next(self.read_robot_file(temp_file)) # 读取脚本文件
            for line in range(len(read_f)):
                msg = read_f[line].strip() # 使用空格分割，读取第一个字段，用于判断标题
                if re.search(r"^tiName_", msg): # 参数化用例
                    if case_dict['tiName']['status'] != 0:
                        r_list += case_list # 保存整理好的参数化用例
                    if case_dict['test']['status'] == 1:
                        r_list += case_list # 保存整理好的普通用例
                    case_list = []
                    case_dict['tiName']['flag']   =  1
                    case_dict['tiName']['status'] =  0
                    # 初始化普通用例标记
                    case_dict['test']['status']   = -1
                    case_dict['test']['flag']     =  0
                elif re.search(r"^test_", msg): # 普通用例
                    if case_dict['tiName']['status'] != 0:
                        r_list += case_list
                    if case_dict['test']['status'] == 1:
                        r_list += case_list
                    case_list = []
                    case_dict['test']['status']   = -1
                    case_dict['test']['flag']     = 1
                    # 初始化参数化用例标记
                    case_dict['tiName']['flag']   = 0
                    case_dict['tiName']['status'] = 0

                elif read_f[line].strip() == '*** Keywords ***':
                    if case_dict['tiName']['status'] != 0:
                        r_list += case_list
                    if case_dict['test']['status'] == 1:
                        r_list += case_list
                    case_list = []
                    # 测试用例整理完毕，初始化标记
                    case_dict['tiName']['flag']  = 0
                    case_dict['test']['flag']    = 0

                if (case_dict['tiName']['flag'] == 1):
                    # 整理Test Cases：参数化用例
                    if re.search(r"^case_", msg):
                        casetitleList = list(filter(None, msg.split(" ")))
                        for casetitle in casetitleList:
                            caseID = re.findall("_(\d+)$", casetitle)
                            if (len(caseID) != 0):
                                break
                        # casetitle2 = msg.split(" ")[0]
                        # caseID    = re.findall("_(\d+)$",casetitle2)
                        if (len(caseID) == 0) or (caseID[0] not in caseIDList):
                            # case_list.append("#" + read_f[line])
                            pass
                        else:
                            case_list.append(read_f[line])
                            case_dict['tiName']['status'] += 1
                    else:
                        case_list.append(read_f[line])
                    continue
                elif (case_dict['test']['flag'] == 1):
                    # 整理Test Cases：普通用例
                    if case_dict['test']['status'] == -1:
                        # casetitle = msg.split(" ")[0]
                        casetitle = msg
                        caseID = re.findall("_(\d+)$", casetitle)
                        if (len(caseID) == 0) or (caseID[0] not in caseIDList):
                            case_list = []
                            case_dict['test']['status'] = 0
                        else:
                            case_list.append(read_f[line])
                            case_dict['test']['status'] = 1
                    elif case_dict['test']['status'] == 0:
                        case_list = []
                    elif case_dict['test']['status'] == 1:
                        case_list.append(read_f[line])
                    continue
                else:
                    # 保存Settings和Keywords内容
                    r_list.append(read_f[line])

                # 保存整理好的自动化用例到新文件
                with open(new_file,'w',encoding='utf-8') as write_f:
                    write_f.write("\n".join(r_list))
            os.remove(temp_file) # 删除临时脚本文件

if __name__ == "__main__":
    case = TestcaseGen()
    case.arg_parser()
    case.testcase_generate()
