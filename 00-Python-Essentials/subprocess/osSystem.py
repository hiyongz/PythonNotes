# -*-coding:utf-8-*-
# @Time:    2023/3/8 16:21
# @Author:  haiyong
# @File:    osPopen.py

import os
import logging

class testSystem():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

    def test_system(self):
        command = "date /T"
        command = "netsh interface ip show address WAN | findstr IP"
        p = os.system(command)
        print(p)   

    def test_ossystem(self):
        command = "netsh interface ip show address "
        filename = input("Please input name of network adapter:\n")
        return_value = os.system(command+filename)
        print('Return Value:', return_value)

if __name__ == '__main__':
    dir = testSystem()
    # dir.test_system()
    dir.test_ossystem()

