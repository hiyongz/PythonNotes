#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import random
import time,io,sys,os,re
from ktclass import ks_SP9
FLAG = 0

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
# sys.stdout = Logger('/usr/lib/zabbix/alertscripts/log')
sys.stdout = Logger()

def now_time():
    now_time = datetime.datetime.now()
    return now_time
    
def ten_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=10ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.01)
        print"    %s 等待10ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=10ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
    
def twenty_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=20ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.02)
        print"    %s 等待20ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=20ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def fifty_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=50ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.05)
        print"    %s 等待50ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=50ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def hundred_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=100ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.1)
        print"    %s 等待100ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=100ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def twohundredfifty_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=250ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.25)
        print"    %s 等待250ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=250ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def fivehundred_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=1,Toff=500ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试30次测试"%(now_time())
    for i in range(30):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(0.5)
        print"    %s 等待500ms"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=1,Toff=500ms,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def random_ms():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=random,Toff=500ms,Tboot+Tcheck=60s,Tgap=1s 测试"%(now_time())
    print "%s 共测试500次测试"%(now_time())
    for i in range(500):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        rd_num=(random.randint(1,10))
        time.sleep(rd_num)
        print"    %s 等待%s s"%(now_time(),rd_num)
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s Ton=random,Toff=1s,Tboot+Tcheck=60s,Tgap=1s 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def random_45():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=random,HT=45℃ 测试"%(now_time())
    print "%s 共测试500次测试"%(now_time())
    for i in range(500):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        rd_num=(random.randint(1,10))
        time.sleep(rd_num)
        print"    %s 等待%s s"%(now_time(),rd_num)
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s  Ton=random,HT=45℃ 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def random_10():
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=random,HT=-10℃ 测试"%(now_time())
    print "%s 共测试500次测试"%(now_time())
    for i in range(500):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        rd_num=(random.randint(1,10))
        time.sleep(rd_num)
        print"    %s 等待%s s"%(now_time(),rd_num)
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        time.sleep(1)
        print"    %s 等待1s"%(now_time())
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        SW.close()
        time.sleep(60)
        print"    %s 等待60s"%(now_time())
        if ping():
            SW.socket_connect()
            print"    %s 断电"%(now_time())
            SW.sendCmd('ATS0')
            time.sleep(1)
            print"    %s 等待1s"%(now_time())
            print"  %s 第%s测试完成"%(now_time(),i+1)
            SW.close()
        else:
            return False
    print "%s  Ton=random,HT=-10℃ 测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def random_random(num):
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "%s 开始Ton=random,测试"%(now_time())
    print "%s 测试 次数%s"%(now_time(),num)
    for i in range(num):
        print "=================================================================="
        print "  %s 开始第%s测试"%(now_time(),i+1)
        SW.socket_connect()
        SW.sendCmd('ATS1')
        print "    %s 上电"%(now_time())
        rd_num=(random.randint(1,60))
        time.sleep(rd_num)
        print"    %s 等待%s s"%(now_time(),rd_num)
        SW.close()
        SW.socket_connect()
        SW.sendCmd('ATS0')
        print"    %s 断电"%(now_time())
        rd_num=(random.randint(1,10))
        time.sleep(rd_num)
        print"    %s 等待 %s"%(now_time(),rd_num)
    
    print "%s  Ton=random测试完成"%(now_time())
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return True
def ping():
    lines = os.popen('ping 192.168.0.1')
    ret=lines.read()
    ret=ret.decode('gbk')
    print "    %s"%(ret)
    if 'TTL=' in ret:
        return True
    else:
        return True
        
if __name__=="__main__":
    SW=ks_SP9()
    # ten_ms()
    # twenty_ms()
    # fifty_ms()
    # hundred_ms()
    # twohundredfifty_ms()
    # fivehundred_ms()
    # random_ms()
    # random_45()
    # random_10()
    # random_45()
    # random_10()
    random_random(5000)