#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/10/5 17:19
# @Author:  hiyongz
# @File:    test_regex.py

# 正则表达式
import re

data = "1\nstart\ntest1\ntest2\nend\n2"

class TestRegex():
    def test1(self):
        # 删除多行
        reg0 = r'(?<=start).*?(?=end)'
        res = re.findall(reg0, data)
        print(res)

        reg1 = r"start.*end"
        # m = re.search(reg1, data, flags=re.S)
        # print(m.group(1))
        print("\nreg1: ")
        res = re.findall(reg1, data, flags=re.S)
        print(res)
        res = re.findall(reg1, data, flags=re.DOTALL)
        print(res)

        print("\nreg2: ")
        reg2 = r"start(.*)end"
        res = re.findall(reg2, data, flags=re.S)
        print(res)
        res = re.findall(reg2, data, flags=re.DOTALL)
        print(res)

        print("\nreg3: ")
        reg3 = r"start((.|\n|\r)*)end"
        res = re.findall(reg3, data)
        print(res)

        print("\nreg4: ")
        reg4 = r"start([\s\S]*)end"
        res = re.findall(reg4, data)
        print(res)

        # reg5 = r"start((?s).*)end"
        print("\nreg5: ")
        reg5 = r"(?s)start(.*)end"
        res = re.findall(reg5, data)
        print(res)

        print("\nreg6: ")
        reg6 = r"(?s)start.*end"
        res = re.findall(reg6, data)
        print(res)



reg = TestRegex()
reg.test1()