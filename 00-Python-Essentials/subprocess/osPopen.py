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
        # Define command and options wanted
        command = "netsh interface ip show address "
        # Ask user for file name(s) - SECURITY RISK: susceptible to shell injection
        filename = input("Please input name of network adapter:\n")
        # Run os.system and save return_value
        p = os.popen(command+filename, 'r')
        # print('###############')
        # print('Return Value:', p.read())

    def test_ospopen2(self):
        # Define command and options wanted
        command = "netsh interface ip show address "
        # Ask user for file name(s) - SECURITY RISK: susceptible to shell injection
        filename = input("Please input name of network adapter:\n")
        # Run os.system and save return_value
        p = os.popen3(command+filename, 'r')
        # print('###############')
        # print('Return Value:', p.read())

    def test_popen(self):
        # Define command and options wanted
        command = "netsh interface ip show address "
        # Ask user for file name(s) - SECURITY RISK: susceptible to shell injection
        filename = input("Please input name of network adapter:\n")
        # Run os.system and save return_value
        # p = Popen(command+filename, stdout=PIPE).stdout
        p = Popen(command+filename, shell=True, stdin=PIPE).stdin
        print('###############')
        print('Return Value:', p.read())

    def test_ossystem(self):
        # Define command and options wanted
        command = "netsh interface ip show address "
        # Ask user for file name(s) - SECURITY RISK: susceptible to shell injection
        filename = input("Please input name of network adapter:\n")
        # Run os.system and save return_value
        return_value = os.system(command+filename, 'w')
        print('###############')
        print('Return Value:', return_value)


if __name__ == '__main__':
    dir = testPopen()
    # dir.test_path()
    # dir.test_ospopen()
    dir.test_popen()
