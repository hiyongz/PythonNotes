# -*-coding:utf-8-*-
# @Time:    2023/3/8 16:21
# @Author:  haiyong
# @File:    osPopen.py
import os
import subprocess
import sys
import logging


class testPopen():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

    def test_Popen(self):
        command = "netsh interface ip show address "
        filename = input("Please input name of network adapter:\n")
        p = subprocess.Popen(command+filename, stdout=subprocess.PIPE).stdout
        # p = Popen(command+filename, shell=True, stdin=PIPE).stdin
        print('Return Value:', p.read().decode('gbk'))
    
    def test_Popen2(self):
        command = "netsh interface ip show address WAN | findstr IP"
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
        
        print(p.read().decode('gbk'))
        # logging.info(p.read().decode('gbk'))

    def test_Popen3(self):
        command = "netsh interface ip show address WAN | findstr IP"
        p = subprocess.Popen(command, shell=True).wait()
        print(p)
        # logging.info(p.read().decode('gbk'))

    def test_Popen4(self):
        p1 = subprocess.Popen('netsh interface ip show address WAN', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen('findstr IP', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE).stdout
        print(p2.read().decode('gbk'))

    def test_Popen5(self):
        p1 = subprocess.Popen('netsh interface ip show address WAN', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen('findstr IP', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        out, err = p2.communicate()
        print(out.decode('gbk'))

    def test_Popen6(self):
        output = subprocess.check_output("netsh interface ip show address WAN | findstr IP", shell=True)
        print(output.decode('gbk'))

    def popenWithMultiCmd(self):
        commands = ['mkdir log', 'cd log','echo "test" > test.txt','dir']
        p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for cmd in commands:
            p.stdin.write((cmd + "\n").encode('utf-8'))
        p.stdin.close()
        logging.info(p.stdout.read().decode('gbk'))


if __name__ == '__main__':
    dir = testPopen()
    # dir.test_Popen6()
    dir.popenWithMultiCmd2()
