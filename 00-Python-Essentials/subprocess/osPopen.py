# -*-coding:utf-8-*-
# @Time:    2023/3/8 16:21
# @Author:  haiyong
# @File:    osPopen.py
import os
from subprocess import PIPE, Popen
import sys
import logging


class testPopen():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

    def test_ospopen(self):
        command = "netsh interface ip show address "
        filename = input("Please input name of network adapter:\n")
        p = os.popen(command+filename, 'r')
        # print('Return Value:', p.read())

    def test_ospopen2(self):
        command = "netsh interface ip show address WAN | findstr IP"
        p = os.popen(command, 'r')
        print(p.read())        

    def test_ospopen3(self):
        command = "netsh interface ip show address "
        filename = input("Please input name of network adapter:\n")
        p = os.popen3(command+filename, 'r')
        # print('Return Value:', p.read())

    def test_ospopen4(self):
        command = 'echo "test" > test.txt ; del test.txt'
        # command = 'dir'
        # command = 'netsh interface ip show address WAN | findstr "IP"'
        p = os.popen(command)
        # p = Popen(command+filename, shell=True, stdin=PIPE).stdin
        # logging.info('###############')
        print('Return Value:', p.read())

        # out = os.popen(command)
        # logging.info(out.read())


if __name__ == '__main__':
    dir = testPopen()
    # dir.test_path()
    # dir.test_ospopen()
    dir.test_ospopen2()

