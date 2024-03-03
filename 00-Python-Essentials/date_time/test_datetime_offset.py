#!/usr/bin/python2
#-*-coding:utf-8-*-
# @Time:    2020/5/14 13:56
# @Author:  haiyong
# @File:    test_date.py
import datetime
from dateutil import parser
from dateutil import rrule
import os

class testDateTime():
    def init_arg_s(self,init_kargs,kargs):
        for k,v in kargs.items():
            if k in init_kargs:
                init_kargs[k] = v
        return init_kargs


    def adb_get_time(self):
        time_local = os.popen('adb shell date "+%Y-%m-%d %H:%M:%S"')
        time_local = time_local.read()
        time_local = time_local.strip()
        print("nowdate: ",time_local)
        dates = time_local.split(' ')[0]
        times = time_local.split(' ')[1]
        # time_y = os.popen('adb shell date "+%Y').read().strip()
        # time_m = os.popen('adb shell date "+%m').read().strip()
        # time_d = os.popen('adb shell date "+%d').read().strip()

    def add_datetime(self, kargs='{}'):
        kargs = eval(kargs)
        init_dict = {"addtime_y": "0", "addtime_m": "0", "addtime_d": "0"}
        kargs = self.init_arg_s(init_dict, kargs)
        def addtime_init(tim):
            if tim == '':
                tim = 0
            else:
                tim = int(tim)
            return tim

        addt_m = addtime_init(kargs['addtime_m'])
        addt_y = addtime_init(kargs['addtime_y'])
        addt_d = addtime_init(kargs['addtime_d'])
        ##### 获取手机时间 #####
        # now_time_new = datetime.datetime.now().strftime('%H:%M')
        # print "now_time_new",self.now_time_new
        time_local = "2024-01-15 20:29:00"

        ##### 天数增加减少 #####
        # time_local = strTime
        startTime = datetime.datetime.strptime(time_local, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式
        # startTime时间增加减少
        startTime1 = (startTime + datetime.timedelta(days=addt_d)).strftime("%Y-%m-%d %H:%M")

       ##### 月数增加减少 #####
        startTime2 = startTime
        for _ in range(abs(addt_m)):
            if addt_m < 0:
                startTime2 = startTime2.replace(day=1) - datetime.timedelta(days=1)
            elif addt_m > 0:
                startTime2 = startTime2.replace(day=28) + datetime.timedelta(days=4)
        startTime2 = startTime2.strftime("%Y-%m-%d %H:%M")
        ##### 年份增加减少 #####
        startTime3 = startTime
        for _ in range(abs(addt_y)):
            if addt_y < 0:
                startTime3 = startTime3.replace(month=1,day=1) - datetime.timedelta(days=1)
            elif addt_y > 0:
                startTime3 = startTime3.replace(month=12,day=31) + datetime.timedelta(days=1)
        startTime3 = startTime3.strftime("%Y-%m-%d %H:%M")

        if abs(addt_y) > 0:
            resulttime = startTime3[0:5] + time_local[5:10]
            return resulttime
        elif abs(addt_m) > 0:
            resulttime = startTime2[0:8] + time_local[8:10]
            return resulttime
        elif abs(addt_d) > 0:
            resulttime = startTime1[0:10]
            return resulttime
        else:
            resulttime = time_local[0:10]
            return resulttime

    def time_offset(self):
        d1 = '2024-01-01 20:29:00'
        d2 = '2024-02-15 20:29:02'
        # 将字符串转化为datetime格式
        # date1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()  ##datetime.date(2018, 1, 6)
        date1 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")  ##datetime.date(2018, 1, 6)
        # date2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()  ##datetime.date(2018, 1, 9)
        date2 = datetime.datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")  ##datetime.date(2018, 1, 9)
        # 天数差
        Days = (date2 - date1).days        
        print(Days)
        Days = (parser.parse(d2) - parser.parse(d1)).days
        print(Days)
        Days = rrule.rrule(rrule.DAILY, dtstart = date1, until = date2).count()
        print(Days)
        # 秒数差 
        Seconds = (date2 - date1).total_seconds()
        print(Seconds)
        # 毫秒数
        Microseconds = (date2 - date1).microseconds  
        print(Microseconds)
        # 周数差（rrule）
        Weeks = rrule.rrule(rrule.WEEKLY, dtstart = date1, until = date2).count() 
        print(Weeks)
        # 月数差（rrule）        
        Months = rrule.rrule(rrule.MONTHLY, dtstart = date1, until = date2).count()  
        print(Months)        
        # 年数差
        Years = rrule.rrule(rrule.YEARLY, dtstart = date1, until = date2).count()  
        print(Years)

    



Date = testDateTime()
nowdate = Date.add_datetime(str({"addtime_d": "6"}))
print(nowdate)
Date.time_offset()