#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/12/9 17:55
# @Author:  haiyong
# @File:    subprocess_demo.py
import subprocess

p = subprocess.Popen("netstat -nao | findstr 8100", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
p.stdout
p.communicate()


