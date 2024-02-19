#!/usr/bin/python2
#-*-coding:utf-8-*-
# @Time:    2020/5/14 13:56
# @Author:  haiyong
# @File:    test_date.py
import datetime
from dateutil import parser
from dateutil import rrule
import os

class datetimeDemo():

    def Demo1(self):
        d1 = '2024-02-25 20:29:00'
        # 将字符串转化为datetime格式
        # date1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()  ##datetime.date(2018, 1, 6)
        date1 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")  ##datetime.date(2018, 1, 6)
        now_time = datetime.datetime.now()
        print(now_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(now_time.strftime("%A"))
        print(now_time.strftime("%w"))

        weekday = now_time.weekday()
        print(weekday)
        print(date1.weekday())
        print(date1.strftime("%w"))


Date = datetimeDemo()
Date.Demo1()