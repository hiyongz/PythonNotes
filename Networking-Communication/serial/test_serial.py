#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/5/25 9:42
# @Author:  haiyong
# @File:    test_serial.py

import serial
from serial import *
import serial.tools.list_ports

plist = list(serial.tools.list_ports.comports())

# python -m serial.tools.list_ports

if len(plist) <= 0:
    print("没有发现端口!")
else:
    plist_0 = list(plist[0])
    serialName = plist_0[0]
    serialFd = serial.Serial(serialName, 9600, timeout=60)

print("可用端口名>>>", serialFd.name)

if serialFd.isOpen():
    print("open success")
else:
    print("open failed")

