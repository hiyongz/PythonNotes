#!/usr/bin/python2
#-*-coding:utf-8-*-
# @Time:    2020/5/14 13:56
# @Author:  haiyong
# @File:    test_date.py
import datetime
import os

class testDateTime():
    def init_arg_s(self,init_kargs,kargs):
        for k,v in kargs.iteritems():
            if init_kargs.has_key(k):
                init_kargs[k] = v
        return init_kargs

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
        time_local = os.popen('adb shell date "+%Y-%m-%d %H:%M:%S"')
        time_local = time_local.read()
        time_local = time_local.strip()
        print "nowdate: ",time_local
        dates = time_local.split(' ')[0]
        times = time_local.split(' ')[1]
        # time_y = os.popen('adb shell date "+%Y').read().strip()
        # time_m = os.popen('adb shell date "+%m').read().strip()
        # time_d = os.popen('adb shell date "+%d').read().strip()

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



Date = testDateTime()
nowdate = Date.add_datetime(str({"addtime_d": "6"}))
print nowdate