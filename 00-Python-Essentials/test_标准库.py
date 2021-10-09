#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2020/8/22 19:03
# @Author:  haiyong
# @File:    test_标准库.py

import os
# os.mkdir("testdir")
print(os.listdir("./")) # 打印当前目录文件名
# os.removedirs("testdir") #删除testdir
print(os.getcwd()) # 返回当前路径

if not os.path.exists("testdir"):
        os.mkdir("testdir")
if not os.path.exists("testdir/test.txt"):
        # f = open('testdir/test.txt','w')
        with open('testdir/test.txt','w') as f:
            f.write("hello world !!!")
import time

print(time.asctime())
print(time.time())
print(time.localtime())
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# 获取两天前的时间
now_timestamp = time.time()
two_day_before = now_timestamp - 60*60*24*2
time_tuple = time.localtime(two_day_before)
print(time.strftime("%Y-%m-%d %H:%M:%S", time_tuple))


import urllib.request
response=urllib.request.urlopen('http://www.baidu.com')
print(response.status)
print(response.read())

import math

print(math.ceil(5.2))
print(math.floor(5.2))