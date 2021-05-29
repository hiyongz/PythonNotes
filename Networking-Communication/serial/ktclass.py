#!/usr/bin/python
#coding=utf-8
import time,io,sys,os,re
import serial
import socket
import json
from telnetlib import Telnet
from serial import *
import paramiko
import subprocess
from base64 import b64encode
import subprocess
import requests
import eventlet
import ConfigParser
# from Global import ParserCfg
# eventlet.monkey_patch()
# sys.path.append("..")
#为了能在用例中直接调用全局配置参数，单步调试请注释下面这行代码
# from Global import *

def catch_exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.socket_connect()
            self.login()
            self.close()
            # self.waitTime(2)
            self.socket_connect()
            u = func(self, *args, **kwargs)
            self.close()
            return u
        except Exception,e:
            return False
    return wrapper
def catch_exception_1(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.login()
            u = func(self, *args, **kwargs)
            self.close()
            return u
        except Exception,e:
            return False
    return wrapper
    
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 
class ktClass(object):
    def __init__(self,type="ssh",host="192.168.20.20",username="root",password="tendatest",**kargs):
        self.host = host
        self.host = host
        self.username = username
        self.password = password
        self.rootdir = "/var/tendatest/TDT"
        if type == "telnet":
            self.t = self.telnet_init()
            self.type = "telnet"
        elif type == "ssh":
            self.t = self.ssh_init()
            self.type = "ssh"
        elif type == "com" :
            self.t = self.serial_init(**kargs)
            self.type = "com"
        elif  type == "adb":
            self.type = "adb"
        #self.login()
    def telnet_init(self,**kargs):
        t=Telnet()
        t.open(host=self.host, port=23)
        return t
    def serial_init(self,**kargs):
        init_kargs = {}
        init_kargs['brate']= self.parserdict("brate","115200",**kargs)
        init_kargs['port']=self.parserdict('port',"COM1",**kargs)
        self.t = serial.Serial(port=init_kargs['port'], baudrate=init_kargs['brate'], bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=0.5, xonxoff=0, rtscts=0, writeTimeout=None, dsrdtr=None)
        print self.t
        if self.t.isOpen():
            print "com init suc!"
        else :
            print "________"
        return self.t
    def ssh_init(self,**kargs):
        t=paramiko.SSHClient() 
        t.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        t.connect(hostname=self.host,username=self.username,password=self.password,allow_agent=True)
        print "slslll",t
        return t
    
    def adb_init(self,**kargs):
        return 
    def shell(self, args):
        """
        执行adb shell命令
        :param args:参数
        :return:
        """
        cmd = """adb shell  su -c '%s' """ % (str(args))
        print "cmd=",cmd
        return os.popen(cmd)
    def adb_wifi(self, power):
        """
        开启/关闭wifi
        pass: 需要root权限
        :return:
        """
        if not self.root():
            print('The device not root.')
            return
        if power:
            self.shell('su -c svc wifi enable').read().strip()
        else:
            self.shell('su -c svc wifi disable').read().strip()
    def adb_wifi_config(self,kargs='{}'):
        kargs = eval(kargs)
        ssid = kargs['ssid']
        pwd = kargs['pwd']
        print "kargs=",kargs
        if pwd:
            network = u"""network={\nssid="%s" \npsk="%s" \nkey_mgmt=WPA-PSK \npriority=1\n}""" %(ssid,pwd)
        else:
            network = u"""network={\nssid="%s" \nkey_mgmt=NON \nEpriority=1\n}""" %(ssid)
        print network
        #cmdlist ="svc wifi disable"
        #cmdlist = ["adb shell busybox sed -i ':1;N;$ s#network={.*}##;b1' /data/misc/wifi/wpa_supplicant.conf"]
        cmdlist =[]
        cmdlist.append("""busybox echo '%s' >>/data/misc/wifi/wpa_supplicant.conf"""%(network))
        cmdlist.append("busybox killall wpa_supplicant")
        cmdlist.append("svc wifi disable")
        cmdlist.append("svc wifi enable")
        cmdlist.append("adb shell exit")
        try:
            pipe = subprocess.Popen("adb shell ", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            code = pipe.communicate("\n".join(cmdlist) + "\n")
            #for cmd in cmdlist :
            #    os.popen(cmd)
            self.waitTime(8)
            #检查是否连接上ssid
            cmd = "adb shell ifconfig wlan0"
            line=0
            for x in xrange(8):
                lines = os.popen(cmd)
                lines=lines.readlines()
                ret = lines[line].strip()
                print "wlan0 ip = ",ret
                if "inet addr" in ret:
                    self.waitTime(5)
                    return True
                line=line+1
            self.waitTime(1)
            #os.popen("adb shell svc wifi disable")
            return False
        except Exception,e:
            return False
    def adb_wifi_config_xiaomi4(self,kargs='{}'):
        kargs = eval(kargs)
        ssid = kargs['ssid']
        pwd = kargs['pwd']
        print "kargs=",kargs
        print "kargs=",kargs
        print "kargs=",kargs
        if pwd:
            network = u"""network={ssid="%s" psk="%s" key_mgmt=WPA-PSK priority=1}""" %(ssid,pwd)
        else:
            network = u"""network={ssid="%s" key_mgmt=NON Epriority=1}""" %(ssid)
        cmdlist = ["busybox sed -i ':1;N;$ s#network={.*}##;b1' /data/misc/wifi/wpa_supplicant.conf"]
        cmdlist.append("busybox echo '%s' >>/data/misc/wifi/wpa_supplicant.conf" %(network))
        cmdlist.append("busybox killall wpa_supplicant")
        cmdlist.append("svc wifi disable")
        cmdlist.append("svc wifi enable")
        cmdlist.append("exit")
        try:
            pipe = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            code = pipe.communicate("\n".join(cmdlist) + "\n")
            self.waitTime(5)
            #检查是否连接上ssid
            cmd = "adb shell su root netcfg|grep wlan0|awk '{print $3}'"
            #adb shell su -c "input text "12345678""
            for x in xrange(30):
                lines = os.popen(cmd)
                lines=lines.readlines()
                ret = lines[0].strip()
                print "wlan0 ip = ",ret
                if ret != "0.0.0.0/0":
                    self.waitTime(10)
                    return True
                self.waitTime(1)
            return False
        except Exception,e:
            return False
    def nic_connect(self,kargs='{}'):
        kargs = eval(kargs)
        ssid = kargs['ssid']
        pwd = kargs['pwd']
        
    def waitTime(self,num):
        for x in xrange(int(num)):
            print "%d/%d sum=%d" %(x,num,num)
            time.sleep(1)
        return True
    #def waittime(self,kargs='{}'):
    #    kargs = eval(kargs)
    #    ssid = kargs['ssid']
    def setMac(self,kargs='{}'):
        init_default_dict = {"iface":"eth1","mac":""}
        kargs = self.init_args(kargs,**init_default_dict)
        mac = kargs['mac']
        sec_mac = int(mac[1],16)
        if mac == "00:00:00:00:00:00" or mac == "FF:FF:FF:FF:FF:FF" or sec_mac%2 == 1:
            print u"MAC地址有误"
            return False
        self.sendCmd("ifconfig %s down"%(kargs['iface']))
        self.sendCmd("ifconfig %s hw ether %s up"%(kargs['iface'],mac))
        self.sendCmd("ifconfig %s up"%(kargs['iface']))
        result = self.sendCmd("ifconfig %s"%kargs['iface'])
        if mac in result:
            return True
        else:
            return False
        
        
    def setIp(self,kargs='{}'):
        #初始默认字典
        self.sendCmd("killall -9 dhclient")
        init_default_dict = {"iface":"eth1","ip":"","mask":"","gateway":"","dns":"","mac":"","mtu":"","LFile":"/var/db/dhclient.leases","PFile":"/var/run/dhclient.pid","hostname":"","mode":"static"}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == "static":
            #命令行参数字典
            cfg_opt_dict = {"iface":"eth1","ip":"","mask":"netmask ","mac":"hw ether ","mtu":"mtu "}
            opt_dict = {"iface":"eth1","ip":"","mask":"netmask ","mac":"hw ether ","mtu":"mtu "}
            for k,v in cfg_opt_dict.iteritems():
                if v.endswith(" "):
                    cfg_opt_dict[k]=v+kargs[k]
                else:
                    cfg_opt_dict[k]=kargs[k]
            print "cfg_opt_dict=",cfg_opt_dict
            cmd = ["ifconfig %s" %(kargs['iface'])]
            for k,v in cfg_opt_dict.iteritems():
                if v != opt_dict[k]:
                    if k== 'iface':
                        continue
                    cmd.append(v)
            print cmd
            self.sendCmd(" ".join(cmd))
            if kargs['gateway']:
                self.sendCmd("ip route replace default via %s dev %s" %(kargs['gateway'],kargs['iface']))
            if kargs['dns']:
                self.sendCmd("""echo >/etc/resolv.conf""")
                dnslist = kargs['dns'].split(",")
                for dns in dnslist:
                    self.sendCmd("""echo "nameserver %s" >>/etc/resolv.conf """ %(dns))
        elif kargs['mode'] == 'dhcp':
            if kargs['mac']:
                self.sendCmd("ifconfig %s hw ether %s up"%(kargs['iface'],kargs['mac']))
            self.sendCmd("killall -9 dhclient")
            if kargs['hostname'] != "":
                hostname = kargs['hostname']
                hostlen = len(kargs['hostname'])
                host = "-addop 12,%s,%s." %(hostlen,hostname)
            else:
                host = ""
            lf = "-lf %s" %kargs['LFile']
            pf = "-pf %s" %kargs['PFile']
            self.sendCmd("""/var/tendatest/TDT/bin/dhclient %s  %s %s %s""" %(kargs['iface'],lf,pf,host))
            #检查配置结果
            info = self.sendCmd("""ifconfig %s""" %kargs['iface'])
            line = info.find("inet addr:")
            if line != -1:
               pattern = re.compile("inet addr:(\d+.){3}\d+?")
               ip = pattern.search(str(info)).group().split(":")[1]
               if ip != "":
                    return True
            else:
                return False
        elif kargs['mode'] == 'del':
            self.sendCmd("""/var/tendatest/TDT/script/SetIp.sh -D %s""" %kargs['iface'])
            info = self.sendCmd("ifconfig %s" %kargs['iface'])
            line = info.find("inet addr:")
            if line == -1:
                return True
            else:
                return False
        return True
    def getIp(self,kargs='{}'):
        init_default_dict = {"iface":"eth1","ip":"","mask":"","gateway":"","dns":"","mac":"","mtu":"","dmac":""}
        kargs = self.init_args(kargs,**init_default_dict)
        retdict = {"iface":kargs['iface']}
        ret = self.sendCmd("ifconfig %s" %(kargs['iface']))
        macinfo = re.findall("(HWaddr.*)",ret)
        ipinfo = re.findall("(inet addr:[0-9.]+)",ret)
        maskinfo = re.findall("(Mask:[0-9.]+)",ret)
        mtuinfo = re.findall("(MTU:[0-9]+)",ret)
        if macinfo:
            retdict['mac'] = macinfo[0].strip().split(" ")[-1]
        if ipinfo:
            retdict['ip'] = ipinfo[0].strip().split(":")[-1]
        if maskinfo:
            retdict['mask'] = maskinfo[0].strip().split(":")[-1]
        if mtuinfo:
            retdict['mtu'] = mtuinfo[0].strip().split(":")[-1]
        ret = self.sendCmd("route|grep default")
        gwinfo = re.findall(r"default\s+[0-9.]+",ret)
        if gwinfo:
            retdict['gateway']=re.split("\s+",gwinfo[0])[-1]
        if retdict.has_key("gateway"):
            ret = self.sendCmd("cat /proc/net/arp|grep %s" %(retdict['gateway']))
            if ret:
                retdict['gmac'] = re.split("\s+",ret)[3]
        # for k,v in retdict.iteritems():
            # if kargs.has_key(k):
                # kargs[k] = v
        return retdict
    def pppoeSerCfg(self,kargs='{}'):
        u"""
            配置Pppoe服务器函数
            auth:ppp认证方式
            user:拨号时用户名
            pwd:拨号时密码
            MPPE：40,128,both
            mtu num] \t\t\t\t-- 配置MTU值选项\n 
            mru num] \t\t\t\t-- 配置MRU值选项，0为拒绝协商\n 
            echointerval num] \t\t\t-- 配置维链次数选项，默认12\n \
            echofailure num] \t\t\t-- 配置维链失败次数选项，默认8s\n \
        """
        init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"10.10.10.1","rip":"10.10.10.10","num":"1","iface":"eth1","padot":"0","dns":"202.96.134.133,202.96.128.86","mtu":"","mru":"","mppe":"","servername":"","repadr":"","mode":"add","echointerval":"","echofailure":"","repadi":""}
        pppoe_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","echointerval":"--echointerval ","echofailure":"--echofailure "}
        init_pppoe_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","echointerval":"--echointerval ","echofailure":"--echofailure "}
        
        pppoeserver_options_dict = {"lip":"-L ","rip":"-R ","num":"-N ","iface":"-I ","padot":"-T ","servername":"-S ","repadr":"-a"}
        init_pppoeserver_options_dict = {"lip":"-L ","rip":"-R ","num":"-N ","iface":"-I ","padot":"-T ","servername":"-S ","repadr":"-a"}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd("killall -9 pppoe-server")
        self.sendCmd("killall -9 pppoe")
        self.sendCmd("iptables -F")
        net=kargs['lip']
        net=net[:-1]+'0/24'
        self.sendCmd("iptables -t nat -A POSTROUTING -s %s -o %s -j MASQUERADE"%(net,kargs['iface']))
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#'> /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#'> /etc/ppp/pap-secrets""")
        for index,value in enumerate(kargs['user']):
            # if kargs['pwd'][index] == '"' and  value == '"':
                # self.sendCmd("""echo -e ''"' * '"' *'>> /etc/ppp/chap-secrets""")
                # self.sendCmd("""echo -e '%s' * '%s' *>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
            # elif kargs['pwd'][index] == "'" and  value == "'":
                # self.sendCmd("""echo -e "%s" * "%s" *>> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
                # self.sendCmd("""echo -e "%s" * "%s" *>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
            # else:
                # self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
                # self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
            self.sendCmd("""echo -e \'\"%s\" * \"%s\" *\' >> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
            self.sendCmd("""echo -e \'\"%s\" * \"%s\" *\' >> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
            # self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
            
            # self.sendCmd("""echo -e \'\"%s\" * \"%s\" *\'>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
        
        #处理pppoe-config参数
        for k,v in pppoe_options_dict.iteritems():
            pppoe_options_dict[k] = v+kargs[k]
        cmd_pppoeconf = ["%s/script/config_PppoeSerCfg.sh" %(self.rootdir)]
        for k,v in pppoe_options_dict.iteritems():
            if v != init_pppoe_options_dict[k]:
                if k == 'dns':
                    dnslst = v.strip("--dns ").split(",")
                    for dns in dnslst:
                        cmd_pppoeconf.append("--dns "+dns)
                else:
                    cmd_pppoeconf.append(v)
        self.sendCmd(" ".join(cmd_pppoeconf))
        
        #处理pppoe-server参数
        for k,v in pppoeserver_options_dict.iteritems():
            if k == "repadr":
                if kargs[k] != "off":
                    pppoeserver_options_dict[k]=''
            else:
                pppoeserver_options_dict[k]=v+kargs[k]
        cmd_pppoeserver = ["%s/bin/pppoe-server" %(self.rootdir)]
        for k,v in pppoeserver_options_dict.iteritems():
            if k == 'repadr':
                if kargs[k] == "off":
                    cmd_pppoeserver.append(v)
            if v != init_pppoeserver_options_dict[k]:
                cmd_pppoeserver.append(v)
        self.sendCmd(" ".join(cmd_pppoeserver))
        #开启pppoe-server服务器
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep pppoe-server | grep -v grep")
            if re.search("pppoe-server",ret):
                return True
        return False
    def pptpSerCfg(self,kargs='{}',flag='0'):
        flag = str(flag)
        if flag == '1':
            elf.sendCmd('killall -9 named')
        self.sendCmd('killall -9 pptpd pppd')
        #rip 21.1.1.100或者21.1.1.100-200
        init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"21.1.1.1","rip":"21.1.1.100","iface":"eth1","dns":"202.96.134.133,202.96.128.86",'cf':"/etc/pptpd.conf","pptpopt":"/etc/ppp/options.pptpd","mppe":"","mode":"add","mtu":"","mru":""}
        pptp_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","lip":"--localip ","rip":"--remoteip ","cf":"-o ","pptpopt":" --pppopt "}
        init_pptp_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","lip":"--localip ","rip":"--remoteip ","cf":"-o ","pptpopt":" --pppopt "}
        
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#'> /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#'> /etc/ppp/pap-secrets""")
        for index,value in enumerate(kargs['user']):
            self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
            self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
        #配置pptp参数
        for k,v in pptp_options_dict.iteritems():
            pptp_options_dict[k] = v+kargs[k]
        cmd_pptpconf = ["%s/script/config_PptpSerCfg.sh" %(self.rootdir)]
        for k,v in pptp_options_dict.iteritems():
            if v != init_pptp_options_dict[k]:
                if k == 'dns':
                    dnslst = v.strip("--dns ").split(",")
                    for dns in dnslst:
                        cmd_pptpconf.append("--dns "+dns)
                else:
                    cmd_pptpconf.append(v)
        self.sendCmd(" ".join(cmd_pptpconf))
        #开启pptp服务器
        self.sendCmd("%s/bin/pptpd -c %s -l 0.0.0.0" %(self.rootdir,kargs['cf']))
        for x in xrange(5):
            self.waitTime(10)
            ret = self.sendCmd("ps ax|grep pptpd|grep -v grep")
            if re.search(r"pptpd",ret):
                return True
        return False
    def l2tpSerCfg(self,kargs='{}',flag='0'):
        flag = str(flag)
        if flag == '1':
            elf.sendCmd('killall -9 named')
        #rip 21.1.1.100或者21.1.1.100,21.1.1.200
        self.sendCmd('killall -9 xl2tpd')
        init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"22.1.1.1","rip":"22.1.1.100","iface":"eth1","dns":"202.96.134.133,202.96.128.86",'cf':"/etc/xl2tpd/xl2tpd.conf","pptpopt":"/etc/ppp/options.xl2tpd","mode":"add","mtu":"","mru":""}
        l2tp_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","lip":"--localip ","rip":"--remoteip ","cf":"-o ","pptpopt":" --pppopt "}
        init_l2tp_options_dict = {"auth":"--auth ","dns":"--dns ","mtu":"--mtu ","mru":"--mru ","mppe":"--mppe ","lip":"--localip ","rip":"--remoteip ","cf":"-o ","pptpopt":" --pppopt "}
        
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#'> /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#'> /etc/ppp/pap-secrets""")
            self.sendCmd("""killall -9 xl2tpd""")
        for index,value in enumerate(kargs['user']):
            self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/chap-secrets""" %(value,kargs['pwd'][index]))
            self.sendCmd("""echo -e '"%s" * "%s" *'>> /etc/ppp/pap-secrets"""%(value,kargs['pwd'][index]))
        #配置pptp参数
        for k,v in l2tp_options_dict.iteritems():
            l2tp_options_dict[k] = v+kargs[k]
        cmd_l2tpconf = ["%s/script/config_L2tpSerCfg.sh" %(self.rootdir)]
        for k,v in l2tp_options_dict.iteritems():
            if v != init_l2tp_options_dict[k]:
                if k == 'dns':
                    dnslst = v.strip("--dns ").split(",")
                    for dns in dnslst:
                        cmd_l2tpconf.append("--dns "+dns)
                else:
                    cmd_l2tpconf.append(v)
        self.sendCmd(" ".join(cmd_l2tpconf))
        #开启pptp服务器
        self.sendCmd("%s/bin/xl2tpd -c %s -D >/dev/null 2>&1 &" %(self.rootdir,kargs['cf']))
        # self.sendCmd("%s/bin/xl2tpd -c %s -D &" %(self.rootdir,kargs['cf']))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax|grep xl2tpd|grep -v grep")
            if re.search(r"xl2tpd",ret):
                return True
        return False
    def ftpSerCfg(self,kargs='{}'):
        init_default_dict = {"port":"21","rootdir":"/var/ftp","cf":"/etc/vsftpd/vsftpd.conf","file":"testfile","data":"ABCDEFGHIJKLMNTEST"}
        ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o ","file":"--filename ","data":"--data "}
        init_ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o ","file":"--filename ","data":"--data "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in ftp_opt_dict.iteritems():
            ftp_opt_dict[k] = v+kargs[k]
        cmd_ftpopt = ["%s/script/config_FtpSerCfg.sh" %(self.rootdir)]
        for k,v in ftp_opt_dict.iteritems():
            if v != init_ftp_opt_dict[k]:
                cmd_ftpopt.append(v)
        self.sendCmd(" ".join(cmd_ftpopt))
        #开启vsftpd服务器
        self.sendCmd("killall -9 vsftpd")
        self.sendCmd("%s/bin/vsftpd" %(self.rootdir))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep vsftpd|grep -v grep")
            if re.search("vsftpd",ret):
                return True
        return False
    def ftpSerTraCfg(self,kargs='{}'):
        '''
            功能：
                用来配置启动FTP服务期，并设置服务器根目录
            参数： 
                port：FTP协议端口号，默认21
                rootdir：FTP服务器的根目录
                cf：FTP服务器conf文件的路径
        '''
        init_default_dict = {"port":"21","rootdir":"/var/ftp","cf":"/etc/vsftpd/vsftpd.conf"}
        ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o "}
        init_ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in ftp_opt_dict.iteritems():
            ftp_opt_dict[k] = v+kargs[k]
        cmd_ftpopt = ["%s/script/config_FtpSerTraCfg.sh" %(self.rootdir)]
        for k,v in ftp_opt_dict.iteritems():
            if v != init_ftp_opt_dict[k]:
                cmd_ftpopt.append(v)
        self.sendCmd(" ".join(cmd_ftpopt))
        #开启vsftpd服务器
        self.sendCmd("killall -9 vsftpd")
        self.sendCmd("%s/bin/vsftpd" %(self.rootdir))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep vsftpd|grep -v grep")
            if re.search("vsftpd",ret):
                return True
        return False
    def httpSerCfg(self,kargs='{}'):
        init_default_dict = {"port":"80","rootdir":"/var/www","cf":"/etc/httpd/conf/httpd.conf","subdir":"index.htm","data":"ABCDEFGHIJKLMNTEST"}
        ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o ","subdir":"--subdir ","data":"--data "}
        init_ftp_opt_dict =  {"port":"--port ","rootdir":"--rdir ","cf":"-o ","subdir":"--subdir ","data":"--data "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in ftp_opt_dict.iteritems():
            ftp_opt_dict[k] = v+kargs[k]
        cmd_httpopt = ["%s/script/config_HttpSerCfg.sh" %(self.rootdir)]
        for k,v in ftp_opt_dict.iteritems():
            if v != init_ftp_opt_dict[k]:
                cmd_httpopt.append(v)
        self.sendCmd(" ".join(cmd_httpopt))
        #开启vsftpd服务器
        self.sendCmd("killall -9 httpd")
        self.sendCmd("%s/bin/apachectl -k start" %(self.rootdir))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep httpd|grep -v grep")
            if re.search("httpd",ret):
                return True
        return False
    def dhcpSerCfg(self,kargs='{}'):
        #init_default_dict = {"pool":"","lease":"60","gw":"","dns":"8.8.8.8","mask":"","cf":"/tmp/dhcpd.conf","iface":"eth1","lf":"/var/db/dhcpd.leases","adopt":"","delopt":"","chkopt":"","chklen":"","relet":"","noack":"","mac":"","alert":"","of":"/var/tendatest/TDRouter2/tmp/log_dhcpc.txt","dellog":"0"}
        init_default_dict = {"pool":"","lease":"60","gw":"","dns":"","mask":"","cf":"/tmp/dhcpd.conf","iface":"eth1","lf":"/var/db/dhcpd.leases","adopt":"","delopt":"","chkopt":"","chklen":"","relet":"","noack":"","mac":"","alert":"","of":"/var/tendatest/TDRouter2/tmp/log_dhcpc.txt","dellog":"0"}
        cfg_option_dict = {"pool":"--iprange ","lease":"--lease ","gw":"--routers ","dns":"--dns ","mask":"--netmask ","cf":"-o "}
        init_cfg_option_dict = {"pool":"--iprange ","lease":"--lease ","gw":"--routers ","dns":"--dns ","mask":"--netmask ","cf":"-o "}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd('killall -9 dhcpd')
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k]=v+kargs[k]
        cmdcfg = ["%s/script/config_DhcpSerCfg.sh" %(self.rootdir)]
        for k,v in cfg_option_dict.iteritems():
            if v != init_cfg_option_dict[k]:
                cmdcfg.append(v)
        self.sendCmd(" ".join(cmdcfg))
        
        cmd_option_dict = {"adopt":"-addop ","delopt":"-delop ","chkopt":"-checkop ","chklen":"-checklen ","relet":"-relet ","noack":"-noack ","mac":"-mac ","alert":"-alarm "}
        init_cmd_option_dict = {"adopt":"-addop ","delopt":"-delop ","chkopt":"-checkop ","chklen":"-checklen ","relet":"-relet ","noack":"-noack ","mac":"-mac ","alert":"-alarm "}
        cmd = ["%s/bin/dhcpd -cf %s -lf %s %s" %(self.rootdir,kargs['cf'],kargs['lf'],kargs['iface'])]
        for k,v in cmd_option_dict.iteritems():
            cmd_option_dict[k] = v+kargs[k]
            if cmd_option_dict[k] != init_cmd_option_dict[k]:
                cmd.append(cmd_option_dict[k])
        self.sendCmd(" ".join(cmd))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax |grep dhcpd|grep -v grep")
            print ret
            if re.search("dhcpd",ret):
                return True
        return False
    def dnsSerCfg(self,kargs='{}'):
        self.sendCmd('killall -9 named')
        init_default_dict = {"dns":"","urlip":"","cf":"/var/named"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmdopt = ["%s/script/config_DnsSerCfg.sh -d %s" %(self.rootdir,kargs['cf'])]
        dnslst = kargs['dns'].split(",")
        for index,dns in enumerate(dnslst):
            cmdopt.append("--s%s %s" %(index+1,dns))
        for url in kargs['urlip'].split(","):
            cmdopt.append("--url %s" %(url))
        self.sendCmd(" ".join (cmdopt))
        self.sendCmd("%s/bin/named -c %s/named.conf" %(self.rootdir,kargs['cf']))
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep named |grep -v grep")
            if re.search("named",ret):
                return True
        return False
    def tftpSerCfg(self,kargs='{}'):
        init_default_dict = {"rootdir":"/var/lib/tftpboot","downfile":"tftptest","data":"tftptestfile"}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd('echo "%s"> %s/%s' %(kargs['data'],kargs['rootdir'],kargs['downfile']))
        self.sendCmd("service xinetd start")
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("netstat -anlup")
            if re.search("xinetd",ret):
                return True
        return False
    def ntpSerCfg(self,kargs='{}'):
        init_default_dict = {"enable":"1","time":"2014-01-01 00:00:00","cf":"ntp.conf","rf":"/var/run/ntpd.pid"}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd("date -s '%s'" %(kargs['time']))
        if kargs['enable'] == "1":
            cmd = "%s/bin/ntpd -u ntp:ntp -p %s -g -c %s/conf/%s >/dev/null 2>&1 &" %(self.rootdir,kargs['rf'],self.rootdir,kargs['cf'])
            self.sendCmd(cmd)
        else:
            self.sendCmd("killall -9 ntpd")
            return True
        for x in xrange(5):
            self.waitTime(1)
            ret = self.sendCmd("ps ax |grep ntpd|grep -v grep")
            if re.search("ntpd",ret):
                return True
                
        return False 
    def pktSend(self,kargs='{}'):
        #flag = 1按需分片 2不允许分片
        self.sendCmd("killall -9 pksend")
        init_default_dict = {"dip":"","dport":"60000","pro":"tcp","iface":"","sport":"","sip":"","num":"","size":"","flag":"","loss":0.1,"expemss":"","expe":"pass"}
        option_dict = {"dport":"-p ","iface":"-I ","sport":"-P ","sip":"-i ","num":"-c ","size":"-s ","flag":"-F "}
        init_option_dict = {"dport":"-p ","iface":"-I ","sport":"-P ","sip":"-i ","num":"-c ","size":"-s ","flag":"-F "}
        kargs = self.init_args(kargs,**init_default_dict)
        print "**************kargs=",kargs
        for k,v in option_dict.iteritems():
            option_dict[k] = v+kargs[k]
        #处理udp或者tcp
        mapdict = {"tcp":"-t ","udp":"-u "}
        cmd_option = ["%s/bin/pksend %s" %(self.rootdir,kargs['dip'])]
        print "*************brfore cmd_option=",cmd_option
        for k,v in option_dict.iteritems():
            if v != init_option_dict[k]:
                cmd_option.append(v)
        print "*************after cmd_option=",cmd_option
        cmd = "%s %s" %(" ".join(cmd_option),mapdict[kargs['pro']])
        print "*************cmd=",cmd
        self.sendCmd("ip route flush cache")
        self.sendCmd("echo 0 >/proc/sys/net/ipv4/tcp_timestamps")
        print "*************start send cmd************"
        ret = self.sendCmd(cmd)
        tsret = "fail"
        result = False
        print "___________________ret=",ret
        if re.search("ntransmitted",ret):
            retlst =  map(lambda x:float(x),re.findall(r"([0-9]+)",ret))
            print "retlst=",retlst
            if len(retlst) >=6 or len(retlst) == 4:
                result = (retlst[0]-retlst[1])/retlst[0] < kargs['loss']
                # print "result=",result
            if kargs['expemss']:
                result = float(kargs['expemss']) == retlst[4] and float(kargs['expemss']) == retlst[5]
        self.sendCmd("echo 1 >/proc/sys/net/ipv4/tcp_timestamps")
        print "___________________result=",result
        if result:
            tsret = "pass"
        if tsret == kargs['expe']:
            print "***************success*************"
            return True
        else:
            print "***************fail******************"
            return False
    def sshLogin(self,kargs='{}'):
        init_default_dict = {"ip":"","user":"","pwd":"","cmd":"ifconfig","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "%s/script/sshlogin.sh %s %s %s %s" %(self.rootdir,kargs['user'],kargs['pwd'],kargs['cmd'],kargs['ip'])
        ret = self.sendCmd(cmd)
        result = "pass"
        if re.search("inet addr:%s" %(kargs['ip']),ret):
            result = "pass"
        elif re.search("Connection refused" %(kargs['ip']),ret):
            result = "fail"
        else:
            pass
        if kargs['expe'] == result:
            return True
        else:
            return False
    def telnetLogin(self,kargs='{}'):
        init_default_dict = {"ip":"","user":"","pwd":"","cmd":"ifconfig","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "%s/script/telnetlogin.sh %s %s %s %s" %(self.rootdir,kargs['user'],kargs['pwd'],kargs['cmd'],kargs['ip'])
        ret = self.sendCmd(cmd)
        result = "pass"
        if re.search("inet addr:%s" %(kargs['ip']),ret):
            result = "pass"
        elif re.search("Connection refused" %(kargs['ip']),ret):
            result = "fail"
        else:
            pass
        if kargs['expe'] == result:
            return True
        else:
            return False
    #tftp 客户端 http客户端 ftp客服端 dhclient pptp客户端 l2tp客户端 pppoe客户端
    #简单的获取ip地址，而不做任何判断
    def dhcpCli(self,kargs='{}'):
        init_default_dict = {"iface":"eth1","flag":"1"}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd("""dhclient %s -r""" %kargs['iface'])
        self.sendCmd("""dhclient %s""" %kargs['iface'])
        info = self.sendCmd("""ifconfig %s""" %kargs['iface'])
        line = info.find("inet addr:")
        if line != -1 and kargs['flag'] == 1:
            pattern = re.compile("inet addr:(\d+.){3}\d+?")
            ip = pattern.search(str(code)).group().split(":")[1]
            return True
        elif line == -1 and kargs['flag'] == 0:
            return True
        else:
            return False
    def tftpCli(self,kargs='{}'):
        init_default_dict = {"ip":"","port":"69","dfile":"tftptest","lfile":"/tmp/tftptest","data":"tftptestfile","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "%s/bin/tftp %s %s -c get %s %s" %(self.rootdir,kargs['ip'],kargs['port'],kargs['dfile'],kargs['lfile'])
        self.sendCmd("rm -rf %s" %(kargs['lfile']))
        for x in xrange(3):
            self.sendCmd(cmd)
            self.waitTime(2)
            ret = self.sendCmd("cat %s" %(kargs['lfile']))
            if re.search(kargs['data'],ret):
                result = "pass"
            else:
                result = "fail"
            if kargs["expe"] == result:
                return True
        else:
            return False
    def httpCli(self,kargs='{}'):
        init_default_dict = {"url":"","port":"80","dfile":"index.htm","lfile":"/tmp/www","data":"ABCDEFGHIJKLMNTEST","expe":"pass","timeout":"3","reconnum":"3"}
        cft_option_dict = {"url":"--url  ","dfile":"--file ","port":"--port ","timeout":"--timeout ","reconnum":"--reconnum ","lfile":"--outdir "}
        init_cft_option_dict = {"url":"--url  ","dfile":"--file ","port":"--port ","timeout":"--timeout ","reconnum":"--reconnum ","lfile":"--outdir "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in cft_option_dict.iteritems():
            cft_option_dict[k] = v+kargs[k]
        cmd = ["%s/script/http_downfile.sh" %(self.rootdir)]
        for k,v in cft_option_dict.iteritems():
            if v != init_cft_option_dict[k]:
                cmd.append(v)
        for x in xrange(3):
            self.sendCmd("rm -rf %s/%s" %(kargs['lfile'],kargs['dfile']))
            self.sendCmd(" ".join(cmd))
            ret = self.sendCmd("cat %s/%s"%(kargs['lfile'],kargs['dfile']))
            result = "fail"
            if re.search(kargs['data'],ret):
                result = "pass"
            if result == kargs['expe']:
                return True
            self.waitTime(1)
        return False
    def ftpCli(self,kargs='{}'):
        init_default_dict = {"ip":"","port":"21","user":"ftp","pwd":"ftp","dfile":"testfile","lfile":"/tmp/ftp","data":"ABCDEFGHIJKLMNTEST","expe":"pass","mode":"0"}
        cft_option_dict = {"ip":"--ip  ","dfile":"--file ","port":"--port ","user":"--user ","pwd":"--passwd ","lfile":"--outdir ","mode":"--mode "}
        init_cft_option_dict = {"ip":"--ip  ","dfile":"--file ","port":"--port ","user":"--user ","pwd":"--passwd ","lfile":"--outdir ","mode":"--mode "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in cft_option_dict.iteritems():
            cft_option_dict[k] = v+kargs[k]
        cmd = ["%s/script/ftp_downfile.sh" %(self.rootdir)]
        for k,v in cft_option_dict.iteritems():
            if v != init_cft_option_dict[k]:
                cmd.append(v)
        for x in xrange(3):
            self.sendCmd("rm -rf %s/%s" %(kargs['lfile'],kargs['dfile']))
            self.sendCmd(" ".join(cmd))
            ret = self.sendCmd("cat %s/%s"%(kargs['lfile'],kargs['dfile']))
            result = "fail"
            if re.search(kargs['data'],ret):
                result = "pass"
            if result == kargs['expe']:
                return True
            self.waitTime(1)
        return False
    def ftpCliSpeed(self,kargs='{}'):
        '''
            功能:
                用于计算ftp服务器传输速度，需要配合使用ftpSerTraCfg拉起FTP服务器
            参数：
                ip：FTP服务器ip地址
                port：FTP协议走的端口号，默认21
                user：用户名，默认ftp
                pwd ：密  码，默认ftp
                dfile：需要下载的文件名称，默认testfile1G
                lfile：本地存储的地址，默认/tmp/ftp
                speed ：预期的传输速率，默认为空（单位为MB/s）
                        如果为空，则返回计算出的 speed值
                        如不为空，则于计算出的值进行比较，如果大于传入的值则返回 True
                        反之 ，返回 False
                mode :0表示被动模式,若1则为主动模式，默认为0
                size : 客户端接收文件的大小(单位kB)
                       用来查看文件是否传输完成，并计算FTP文件传输速率
                overtime:超时时间，超过这个时间没有传输完成，则返回False，默认60s
        '''
        init_default_dict = {"ip":"","port":"21","user":"ftp","pwd":"ftp","dfile":"testfile1G","lfile":"/tmp/ftp","speed":"","mode":"0","size":"1076399071","overtime":"60"}
        cft_option_dict = {"ip":"--ip  ","dfile":"--file ","port":"--port ","user":"--user ","pwd":"--passwd ","lfile":"--outdir ","mode":"--mode "}
        init_cft_option_dict = {"ip":"--ip  ","dfile":"--file ","port":"--port ","user":"--user ","pwd":"--passwd ","lfile":"--outdir ","mode":"--mode "}
        kargs = self.init_args(kargs,**init_default_dict)
        for k,v in cft_option_dict.iteritems():
            cft_option_dict[k] = v+kargs[k]
        cmd = ["%s/script/ftp_downfile.sh" %(self.rootdir)]
        for k,v in cft_option_dict.iteritems():
            if v != init_cft_option_dict[k]:
                cmd.append(v)
        self.sendCmd("rm -rf %s/%s" %(kargs['lfile'],kargs['dfile']))
        self.sendCmd(" ".join(cmd))
        transfertime=1#初始传输时间为1s,因为上个步骤FTP连接后等待了1s
        overtime = int(kargs["overtime"])
        for i in range(1,overtime):
            ret=self.sendCmd("ls -l /tmp/ftp |grep %s"%kargs["size"])
            if kargs["size"] in ret:
                transfertime = transfertime+i
                break
        else:
            return False
        kargs['size'] = int(kargs['size'])
        sizeMB = (kargs['size']/1024/1024)#将KB换算为MB
        transferspeed = (sizeMB/transfertime)
        # 如kargs["speed"]不为空,则比较预期值
        # 如kargs["speed"]为空则返回计算出的值
        if kargs["speed"] != '':
            if transferspeed >= int(kargs["speed"]):
                return True
            else:
                return False
        else:
            return transferspeed
    def pppoeCli(self,kargs='{}'):
        init_default_dict = {"auth":"chap","iface":"eth1","user":"tenda","pwd":"tenda","mppe":"","mode":"add","unit":"1","expe":"pass"}
        
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#' > /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#' > /etc/ppp/pap-secrets""")
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/chap-secrets""" %(kargs['user'],kargs['pwd']))
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/pap-secrets""" %(kargs['user'],kargs['pwd']))
        #处理认证时参数
        pppoecfg = """ETH=%s
                    USER=%s
                    DNSTYPE=NOCHANGE
                    PEERDNS=no
                    DEFAULTROUTE=yes
                    CONNECT_TIMEOUT=30
                    CONNECT_POLL=2
                    CLAMPMSS=1412
                    LCP_INTERVAL=12
                    LCP_FAILURE=8""" %(kargs['iface'],kargs['user'])
        self.sendCmd("""echo -e '%s' > /etc/ppp/pppoe.conf""" %(pppoecfg))
        #配置/etc/ppp/options参数
        # self.waitTime(1)
        self.sendCmd("""echo -e "lock" > /etc/ppp/options""")
        self.sendCmd("""echo -e "unit %s" >> /etc/ppp/options""" %(kargs['unit']))
        self.sendCmd("""echo -e "require-%s" >> /etc/ppp/options""" %(kargs['auth']))
        if kargs['mppe']:
            if kargs['mppe'] == "both":
                self.sendCmd("""echo -e "require-mppe" >> /etc/ppp/options""")
            elif kargs['mppe'] == "40" or kargs['mppe'] == "128":
                self.sendCmd("""echo -e "require-mppe-%s" >> /etc/ppp/options"""%(kargs['mppe']))
        
        #开启连接
        cmd = """/usr/sbin/pppd pty "/usr/sbin/pppoe -p .pppoe -I %s -T  -U  -m 1412"    noipdefault noauth default-asyncmap defaultroute hide-password nodetach mtu 1492 mru 1492 noaccomp nodeflate nopcomp novj novjccomp user %s lcp-echo-interval 12 lcp-echo-failure 8 >/dev/null 2>&1 &""" %(kargs['iface'],kargs['user'])
        self.sendCmd(cmd)
        result = "fail"
        for x in xrange(15):
            ret = self.sendCmd("ifconfig")
            if re.search("ppp%s"%(kargs['unit']),ret):
                result = "pass"
                break
            self.waitTime(3)
        if kargs['expe'] == result:
            return True
        else:
            return False
    #如果flag = 0则断开连接
    def l2tpCli(self,kargs='{}'):
        init_default_dict = {"desc":"l2tp","ip":"","user":"tenda","pingip":"","pwd":"tenda","auth":"chap","mppe":"","cf":"/etc/xl2tpd/xl2tpd.conf","mode":"add","flag":"1","unit":"0","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['flag'] == "0":
            self.sendCmd("""echo 'd %s' >/var/run/xl2tpd/l2tp-control""" %(kargs['desc']))
            return True
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#' > /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#' > /etc/ppp/pap-secrets""")
            self.sendCmd("""killall -9 xl2tpd""")
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/chap-secrets""" %(kargs['user'],kargs['pwd']))
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/pap-secrets""" %(kargs['user'],kargs['pwd']))
        cfg_option_dict = {"desc":"--decr ","ip":"--serip ","user":"--user ","pwd":"--pwd ","auth":"--auth ","mppe":"--mppe ","cf":"-o "}
        cmd = ["%s/script/config_L2tpCliConf.sh" %(self.rootdir)]
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k] = v+kargs[k]
            if v != cfg_option_dict[k]:
                cmd.append(cfg_option_dict[k])
        self.sendCmd(" ".join(cmd))
        result = "fail"
        self.sendCmd("""echo 'c %s' > /var/run/xl2tpd/l2tp-control"""%(kargs['desc']))
        for x in xrange(15):
            ret = self.sendCmd("ifconfig")
            if re.search("Point-to-Point Protocol",ret):
                result = "pass"
                self.sendCmds("sh pingtest.sh ping -I ppp0 %s -c 100"%kargs['pingip'])
                self.sendCmds("sh pingtest.sh ping -I ppp1 %s -c 100"%kargs['pingip'])
                break
            self.waitTime(3)
        if kargs['expe'] == result:
            return True
        else:
            return False
    def pptpCli(self,kargs='{}'):
        self.sendCmd("killall -9 pppd,killall -9 pptpd")
        init_default_dict = {"desc":"pptp","ip":"","pingip":"","user":"tenda","pwd":"tenda","auth":"chap","mppe":"","cf":"/etc/ppp/peers/pptp","mode":"add","flag":"1","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        #flag=0表示断开连接
        if kargs['flag'] == "0":
            self.sendCmd("""%s/bin/poff %s""" %(self.rootdir,kargs['desc']))
            self.sendCmd("killall -9 pppd,killall -9 pptpd")
            return True
        if kargs['mode'] == "add":
            self.sendCmd("""echo -e '#' > /etc/ppp/chap-secrets""")
            self.sendCmd("""echo -e '#' > /etc/ppp/pap-secrets""")
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/chap-secrets""" %(kargs['user'],kargs['pwd']))
        self.sendCmd("""echo -e '"%s" * "%s" *' >> /etc/ppp/pap-secrets""" %(kargs['user'],kargs['pwd']))
        cfg_option_dict = {"desc":"--decr ","ip":"--serip ","user":"--user ","pwd":"--pwd ","mppe":"--mppe ","cf":"-o "}
        cmd = ["%s/script/config_PptpCliConf.sh " %(self.rootdir)]
        # check = kargs['desc']+" "+kargs['ip']
        # print 'check=',check
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k] = v+kargs[k]
            if v != cfg_option_dict[k]:
                cmd.append(cfg_option_dict[k])
        self.sendCmd(" ".join(cmd))
        print "************************%s"," ".join(cmd)
        result = "fail"
        for i in xrange(5):
            self.sendCmd("""%s/bin/pon %s""" %(self.rootdir,kargs['desc']))
            self.waitTime(20)
            for i in xrange(5):
                ret = self.sendCmd("ifconfig")
                if re.search("Point-to-Point Protocol",ret):
                    result = "pass"
                    self.sendCmds("sh pingtest.sh ping -I ppp0 %s -c 100"%kargs['pingip'])
                    self.sendCmds("sh pingtest.sh ping -I ppp1 %s -c 100"%kargs['pingip'])
                    break
            if result == "pass":
                break
            self.waitTime(3)
        if kargs['expe'] == result:
            return True
        else:
            return False
        # for x in xrange(10):
            # ret = self.sendCmd("ps ax")
            # if re.search(check,ret):
                # for j in xrange(10):
                    # ret1 = self.sendCmd("ifconfig")
                    # if re.search("ppp%s"%(kargs['unit']),ret1):
                        # result = "pass"
                        # break
                    # self.waitTime(3)
                # break
            # self.waitTime(3)
        # if kargs['expe'] == result:
            # return True
        # else:
            # return False
    def pktRecv(self,kargs='{}'):
        self.sendCmd("killall -9 pkrecv")
        init_default_dict = {"sip":"","ipver":"","sport":"60000","pro":"tcp","num":"","size":""}
        option_dict = {"sport":"-P ","num":"-c ","size":"-s "}
        init_option_dict = {"sport":"-P ","num":"-c ","size":"-s "}
        mapdict = {"tcp":"-t","udp":"-u","all":"-u -t"}
        kargs = self.init_args(kargs,**init_default_dict)
        print "**************kargs=",kargs
        cmd_cfg = ["%s/bin/pkrecv %s" %(self.rootdir,kargs['sip'])]
        print "**************before cmd_cfg=",cmd_cfg
        for k,v in option_dict.iteritems():
            option_dict[k]=v+kargs[k]
        for k,v in option_dict.iteritems():
            if v != init_option_dict[k]:   
                cmd_cfg.append(v)
        print "**************after cmd_cfg=",cmd_cfg
        precmd = " ".join(cmd_cfg)
        print "**************precmd=",precmd
        if kargs['pro'] == "all":
            self.sendCmd("%s -t >/dev/null 2>&1 &" %(precmd))
            self.sendCmd("%s -u >/dev/null 2>&1 &" %(precmd))
        else:
            self.sendCmd("%s %s >/dev/null 2>&1 &" %(precmd,mapdict[kargs['pro']]))
        for x in xrange(4):
            self.waitTime(1)
            ret = self.sendCmd("ps ax | grep pkrecv|grep -v grep")
            if re.search("pkrecv",ret):
                self.waitTime(1)
                return True
        return False
    def upnpMap(self,kargs='{}'):
        init_default_dict = {"lip":"","wport":"9999","lport":"9999","pro":"all"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "%s/bin/upnpc-static -a %s %s %s " %(self.rootdir,kargs['lip'],kargs['lport'],kargs['wport'])
        if kargs['pro'] == "all":
            self.sendCmd(cmd+" tcp")
            self.sendCmd(cmd+" udp")
        else:
            self.sendCmd(cmd+kargs['pro'])
        return True
    def upnpChk(self,kargs='{}'):
        kargs=eval(kargs)
        init_default_dict = {"modelname":"","modelnumber":"","url":"","manufacturer":""}
        ret = self.sendCmd("%s/bin/upnpc-static -P" %(self.rootdir))
        urlinfo = re.search("(desc: .*)",ret)
        url = urlinfo.group().split(" ")[-1]
        filename = url.split("/")[-1]
        self.sendCmd("wget %s -P /tmp/" %(url))
        allinfo = self.sendCmd("cat /tmp/%s" %(filename))
        root = ET.fromstring(allinfo)
        factdict = {}
        factdict['friendlyname'] = root[1][1].text
        factdict['manufacturer'] = root[1][2].text
        factdict['modelname'] = root[1][4].text
        factdict['modelnumber'] = root[1][5].text
        factdict['url'] = root[1][-1].text
        for k,v in kargs.iteritems():
            if v != factdict[k]:
                print "keys={%s} expe=%s fact=%s" %(k,v,factdict[k])
                return False
        return True
    def encapPing(self,kargs='{}'):
        init_default_dict = {"dip":"192.168.0.1","iface":"eth1","sip":"","smask":"","smac":"","rip":"","size":"64","num":"5","flood":"1","flag":"0","loss":"10","expe":"pass"}
        
        cfg_option_dict = {"iface":"-I ","sip":"--sip ","smask":"--smask ","smac":"--smac ","rip":"--rip ","size":"-s ","num":"-c "}
        init_cfg_option_dict = {"iface":"-I ","sip":"--sip ","smask":"--smask ","smac":"--smac ","rip":"--rip ","size":"-s ","num":"-c "}
        kargs = self.init_args(kargs,**init_default_dict)
        #第一步先获取得到默认参数
        cmd = ["%s/bin/encapping %s" %(self.rootdir,kargs['dip'])]
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k] = v+kargs[k]
            if cfg_option_dict[k] != init_cfg_option_dict[k]:
                cmd.append(cfg_option_dict[k])
        if kargs['flag'] != "0":
            cmd.append("-F")
        if kargs['flood'] == "1":
            cmd.append("-f")
        ret = self.sendCmd(" ".join(cmd))
        lossper=re.search("([0-9]+%)",ret)
        lossper = float(lossper.group().strip("%"))
        result = "pass"
        if lossper>float(kargs['loss']):
            result = "fail"
        if result == kargs["expe"]:
            return True
        else:
            return False
    def ping(self,kargs='{}'):
        init_default_dict = {"dip":"192.168.0.1","iface":"eth1","size":"64","flood":"0","flag":"0","expe":"pass","maxerr":"5","maxsuc":"5"}
        
        cfg_option_dict = {"iface":"-I ","size":"-s "}
        init_cfg_option_dict = {"iface":"-I ","size":"-s "}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = ["ping %s -c 1" %(kargs['dip'])]
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k] = v+kargs[k]
            if cfg_option_dict[k] != init_cfg_option_dict[k]:
                cmd.append(cfg_option_dict[k])
        if kargs['flag'] != "0":
            cmd.append(" -M do")
        if kargs['flood'] == "1":
            cmd.append("-f")
        maxerr = int(kargs['maxerr'])
        print "maxerr = ",maxerr
        maxsuc = int(kargs['maxsuc'])
        print "maxsuc = ",maxsuc
        sumnum = maxerr+maxsuc
        factsuc = 0
        facterr = 0
        result = "fail"
        self.sendCmd("ip route flush cache")
        for x in xrange(sumnum):
            ret = self.sendCmd(" ".join(cmd))
            print ret
            if re.search("ttl=",ret):
                factsuc = factsuc + 1
            else:
                facterr = facterr + 1
            if factsuc >= maxsuc:
                result = "pass"
                break
            elif facterr >= maxerr:
                result = "fail"
                break
            self.waitTime(1)
        print "factsuc =",factsuc
        print "facterr =",facterr
        if result == kargs["expe"]:
            return True
        else:
            return False
    def dnsInvalid(self,kargs='{}'):
        u"""
            使用iptables对53端口进行过滤
        """
        init_default_dict = {"dns":""}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['dns']:
            for dns in kargs['dns'].split(","):
                self.sendCmd("iptables -t filter -A INPUT -s %s -p udp --dport 53 -j DROP"%(dns))
        else:
            self.sendCmd("iptables -t filter -F")
        return True
    def arpSend(self,kargs='{}'):
        #arpSend---发送arp数据包"""
        # sip-表示源IP地址 smac-表示源Mac地址 
        # type= 1表示arp请求  2表示相应
        # time  表示发包时间长度 num 表示发包个数
        init_default_dict = {"sip":"","smac":"","dip":"","dmac":"","type":"1","time":"1","num":"1000","macincr":"0","iface":"eth1","expe":"pass"}
        cfg_option_dict = {"sip":"-sip ","dip":"-dip ","smac":"-smac ","dmac":"-dmac ","type":"-type ","num":"-num ","time":"-time "}
        init_cfg_option_dict = {"sip":"-sip ","dip":"-dip ","smac":"-smac ","dmac":"-dmac ","type":"-type ","num":"-num ","time":"-time "}
        kargs = self.init_args(kargs,**init_default_dict)
        cmdlst = ["%s/bin/arpsend " %(self.rootdir)]
        for k,v in cfg_option_dict.iteritems():
            if k in ['smac','dmac']:
                kargs[k] = re.sub("([-:])","",kargs[k])
            cfg_option_dict[k] = v+kargs[k]
            if cfg_option_dict[k] != init_cfg_option_dict[k]:
                cmdlst.append(cfg_option_dict[k])
        if kargs['macincr'] != "0":
            cmdlst.append("-chmac")
        cmdlst.append(kargs['iface'])
        
        self.sendCmd(" ".join(cmdlst))
        return True
    def getTime(self):
        ret = self.sendCmd("""date +"%F %T" """)
        return ret
    def nslookup(self,kargs='{}'):
        init_default_dict = {"url":"","serip":"192.168.0.1","expeip":"","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "nslookup %s %s" %(kargs['url'],kargs['serip'])
        ret = self.sendCmd(cmd)
        pos  = ret.find("Name:")
        result = "fail"
        if pos != -1:
            fact = re.search("(([0-9]+.){3}([0-9]+))",ret[pos:])
            factip = fact.group()
            if factip == kargs['expeip']:
                result = "pass"
        if result == kargs['expe']:
            return True
        else:
            return False
    def wireless_connect(self,kargs='{}'):
        #authmode OPEN/SHARED/WPAPSK/WPA2PSK
        #crypto NONE/WEP/AES/TKIP
        #pwd   #用于WPAPSK或者WPA2PSK加密
        #key 用于WEP加密密码
        #index 用于WEP加密
        
        #pairwise NONE/WEP/AES/TKIP
        #key_mgmt NONE WPA-PSK
        #proto WPA RSN NONE
        #psk
        init_default_dict = {'ssid':'','authmode':'OPEN','crypto':'NONE','key':'','index':'','expe':'pass','channel':'1','pwd':'','bssid':''}
        cryptodict = {'AES':'CCMP','TKIP':'TKIP','WPAPSK':'WPA','WPA2PSK':'RSN'}
        kargs = self.init_args(kargs,**init_default_dict)
        channel = self.channelToHz(kargs['channel'])
        network = ['ctrl_interface=/var/run/wpa_supplicant','ctrl_interface_group=wheel','update_config=1']
        network.append("""network={""")
        network.append('frequency=%s'%(channel))
        network.append('ssid="%s"'%(kargs['ssid']))
        if kargs['crypto'] == 'NONE':
            network.append('key_mgmt=NONE')
        elif kargs['crypto'] in ['AES','TKIP']:
            network.append('proto=%s' %(cryptodict[kargs['authmode']]))
            network.append('key_mgmt=WPA-PSK')
            network.append('pairwise=%s' %(cryptodict[kargs['crypto']]))
            network.append('group=%s' %(cryptodict[kargs['crypto']]))
            network.append('psk="%s"' %(kargs['pwd']))
        elif kargs['crypto'] in ['WEP']:
            network.append('proto=WEP')
            network.append('wep_tx_keyidx=%s' %(kargs['index']))
            network.append('auth_alg=%s' %(kargs['authmode']))
            network.append('wep_key%s=%s' %(int(kargs['index'])-1,kargs['key']))
        network.append('}')
        cmdlist = ["rm -rf /etc/wpa_supplicant/wpa_supplicant.conf"]
        cmdlist.append("""echo '%s' > /etc/wpa_supplicant/wpa_supplicant.conf""" %("\n".join(network)))
        cmdlist.append("%s/script/connect.sh 2>&1 >>/dev/null &" %(self.rootdir))
        command = "iwconfig wlan0 >/tmp/iwconfig.txt"
        commands = 'cat /tmp/iwconfig.txt|grep "%s"'%kargs['ssid']
        for cmd in cmdlist:
            print "cmd=",cmd
            self.sendCmd(cmd)
        for x in xrange(30):
            ret = self.sendCmd('cat /tmp/wl.log|grep "result=SUCCESS"')
            if kargs['crypto'] == 'NONE':
                print "command = ",command
                self.sendCmd(command)
                log=self.sendCmd(commands)
                if re.srearch('%s'%kargs['ssid'],log):
                    print "log = ",log
                    result = 'pass'
            elif re.search('SUCCESS',ret):
                result = 'pass'
            else:
                result = 'fail'
            print "%d/30" %(x)
            self.waitTime(3)
            if kargs['expe'] == result:
                return True
        return False
    #使用W522U连接无线扩展，用于ssid或密码带特殊字符的连接
    def w522u_wireless_connect_extend(self,kargs='{}'):
        #AuthMode OPEN/SHARED/WPAPSK/WPA2PSK
        #EncrypType NONE/WEP/AES/TKIP
        #WpaPsk   #用于WPAPSK或者WPA2PSK加密
        #Key 用于WEP加密密码
        #DefaultKeyID 用于WEP加密
        init_default_dict = {'WirelessMode':5,'NetworkType':'Infra','ssid':'','AuthMode':'OPEN','EncrypType':'NONE','DefaultKeyID':'1','Key':'','expe':'pass','Intf':'ra0','WpaPsk':'','HSsid':''}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd('ifconfig %s down' %kargs['Intf'])
        self.waitTime(1)
        self.sendCmd('ifconfig %s up' %kargs['Intf'])
        self.waitTime(2)
        cmd_list=['iwpriv %s set WirelessMode=%d'%(kargs['Intf'],kargs['WirelessMode'])]
        cmd_list.append('iwpriv %s set NetworkType=%s'%(kargs['Intf'],kargs['NetworkType']))
        if kargs['EncrypType'] == 'NONE':
            cmd_list.append('iwpriv %s set AuthMode=OPEN'%kargs['Intf'])
            cmd_list.append('iwpriv %s set EncrypType=NONE'%kargs['Intf'])
        else:
            if kargs['AuthMode'] == 'OPEN' or kargs['AuthMode'] == 'SHARED':
                cmd_list.append('iwpriv %s set AuthMode=%s'%(kargs['Intf'],kargs['AuthMode']))
                cmd_list.append('iwpriv %s set EncrypType=%s'%(kargs['Intf'],kargs['EncrypType']))
                cmd_list.append('iwpriv %s set DefaultKeyID=%s'%(kargs['Intf'],kargs['DefaultKeyID']))
                cmd_list.append("""iwpriv %s set Key%s=%s"""%(kargs['Intf'],kargs['DefaultKeyID'],kargs['Key']))
            elif kargs['AuthMode'] == 'WPAPSK' or kargs['AuthMode'] == 'WPA2PSK':
                cmd_list.append('iwpriv %s set AuthMode=%s'%(kargs['Intf'],kargs['AuthMode']))
                cmd_list.append('iwpriv %s set EncrypType=%s'%(kargs['Intf'],kargs['EncrypType']))
                cmd_list.append("""iwpriv %s set WPAPSK='%s'"""%(kargs['Intf'],kargs['WpaPsk']))
            else:
                print u"加密方式错误"
                return False
        cmd_list.append("iwpriv %s set SSID='%s'"%(kargs['Intf'],kargs['ssid']))
        for i in range(3):
            for cmd in cmd_list:
                self.sendCmd(cmd)
                self.waitTime(1)
            self.waitTime(3)
            for j in range(5):
                result_msg = self.sendCmd('iwpriv %s connStatus'%kargs['Intf'])
                if 'Connected' in result_msg:
                    re = 'pass'
                    break
                else:
                    re = 'fail'
                    self.waitTime(2)
            if re == kargs['expe']:
                return True
        return False
    #使用W522U连接无线           
    def w522u_wireless_connect(self,kargs='{}'):
        #workhz 2.4/5
        #authmod OPEN/SHARED/WPAPSK/WPA2PSK
        #encryptype NONE/WEP/AES/TKIP
        #wpapsk   #用于WPAPSK或者WPA2PSK加密
        #Key 用于WEP加密密码
        #DefaultKeyID 用于WEP加密
        
        init_default_dict = {'workhz':'2.4','channel':'','ssid':'','authmode':'OPEN','encryptype':'NONE','DefaultKeyID':'1','Key1':'12345','Key2':'12345','Key3':'12345','Key4':'12345','expe':'pass','Intf':'ra0','wpapsk':'','HSsid':''}
        kargs = self.init_args(kargs,**init_default_dict)
        print kargs
        self.sendCmd('ifconfig %s down' %kargs['Intf'])
        self.waitTime(1)
        self.sendCmd('ifconfig %s up' %kargs['Intf'])
        self.waitTime(2)
        for i in range(3):
            scan_msg = self.sendCmd('%s/script/config_W522U.sh --intf %s --scan %s'%(self.rootdir,kargs['Intf'],kargs['workhz']))
            #self.waitTime(5)
            wifi_list = scan_msg.split('\n')
            #print wifi_list
            wifi_info=""
            for wifi in wifi_list:
                if re.search(' %s '%kargs['ssid'],wifi):
                    wifi_info = wifi.strip()
                    break
            else:
                print u"第%d次未扫描到指定的ssid"%(i+1)
            if wifi_info != "":
                break
        else:
            print u"3次都未扫描到信号"
            if kargs['expe'] == 'pass':
                return False
            else:
                return True
        wifi_info = wifi_info.split(' ')
        while '' in wifi_info:
            wifi_info.remove('')
        print wifi_info
        kargs['channel'] = wifi_info[0]
        for j in range(3):
            result_msg = self.sendCmd("""%s/script/config_W522U.sh --intf %s --ssid %s --workhz %s --authmod %s --channel %s --encryptype %s --wpapsk %s --defkeyid %s --key1 %s --key2 %s --key3 %s --key4 %s"""%(self.rootdir,kargs['Intf'],kargs['ssid'],kargs['workhz'],kargs['authmode'],kargs['channel'],kargs['encryptype'],kargs['wpapsk'],kargs['DefaultKeyID'],kargs['Key1'],kargs['Key2'],kargs['Key3'],kargs['Key4']))
            self.waitTime(1)
            print result_msg
            print "6666",kargs
            if 'Link Suc' in result_msg:
                ret = 'pass'
                break
            else:
                ret = 'fail'
        if ret == kargs['expe']:
            return True
        else:
            return False
              
    def channelToHz(self,channel):
        chan = int(channel)
        ret = 2412
        if chan < 14:
            ret  = 2407 +chan*5
        elif chan == 14:
            ret = 2484
        elif chan >=36:
            ret = 5030+(chan-6)*5
        return ret

    def wireless_scan(self,kargs='{}'):
        args = eval(kargs)
        result = 'pass'
        for i in range(3):
            self.sendCmd("iwlist scan|grep -A 12 '%s' >/tmp/tmp.txt"%args['ssid'])
            ret = self.sendCmd('cat /tmp/tmp.txt | grep "%s"'%args['ssid'])
            if re.search("%s"%args['ssid'],ret):
                if result == args['expe'] :
                    return True 
                else:
                    return False
            else :
                continue
        if result != args['expe']:
            return True
        else:   
            return False
    def default_channel(self,kargs='{}'):
        args = eval(kargs)
        for i in range(5):
            self.sendCmd("iwlist scan|grep -A 12 '%s' >/tmp/tmp.txt"%args['ssid'])
            ret = self.sendCmd('cat /tmp/tmp.txt | grep -A 4 Channel')
            if re.search("Channel %s"%args['channel'],ret):
                return True
            else :
                continue
        return False 
    def default_band(self,kargs='{}'):
        args = eval(kargs)
        print "%s"%args['rate']
        for i in range(5):
            self.sendCmd("iwlist scan|grep -A 12 '%s' >/tmp/tmp.txt"%args['ssid'])
            ret = self.sendCmd('cat /tmp/tmp.txt | grep -A 6 Bit')
            if re.search("Bit Rates:%s Mb/s"%args['rate'],ret):
                return True #Bit Rates:867 Mb/s
            else :
                continue
        return False    
    def default_rate(self,kargs='{}'):
        #{"ssid":"123","rate":"867"}
        args = eval(kargs)
        for i in range(5):
            self.sendCmd("iwlist scan|grep -A 12 '%s' >/tmp/tmp.txt"%args['ssid'])
            ret = self.sendCmd('cat /tmp/tmp.txt | grep -A 6 Bit')
            if re.search("Bit Rates:%s"%args['rate'],ret):
                    return True
            else :
                continue
        return False    
    def default_protocol(self,kargs='{}'):
        #{"ssid":"123","channel":"11"}
        args = eval(kargs)
        channel = args['channel']
        for i in range(5):
            self.sendCmd("iwlist scan|grep -A 12 '%s' >/tmp/tmp.txt"%args['ssid'])
            ret = self.sendCmd('cat /tmp/tmp.txt | grep -A 2 Protocol')
            if int(channel)<14:
                if re.search("IEEE 802.11bgn",ret):
                    return True
                else :
                    continue
            else:
                if re.search("IEEE 802.11AC",ret):
                    return True
                else :
                    continue
        return False 
        
    def packetCapture(self,kargs='{}'):
        #tcpdump开启抓包
        init_default_dict = {"iface":"eth1","filter":"",'result':"/tmp/packet.pcap"}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = "tcpdump -i %s %s -w %s  >/dev/null 2>&1 &"  %(kargs['iface'],kargs['filter'],kargs['result'])
        self.sendCmd("killall -9 tcpdump")
        self.sendCmd(cmd)
        for x in xrange(5):
            ret = self.sendCmd("ps ax | grep -v grep | grep tcpdump")
            if re.search("tcpdump",ret):
                return True
            self.waitTime(1)
        return False
    def PKT_Mss_Capture(self,kargs='{}'):
        #tcpdump开启抓包
        init_default_dict = {"iface":"eth1","pro":"tcp","dport":"60000",'result':"/tmp/packet"}
        kargs = self.init_args(kargs,**init_default_dict)
        self.sendCmd("killall -9 tcpdump")
        self.sendCmds("tcpdump -i %s %s port %s -c 6 >%s "%(kargs['iface'],kargs['pro'],kargs['dport'],kargs['result']))
        for x in xrange(5):
            ret = self.sendCmd("ps ax | grep -v grep | grep tcpdump")
            if re.search("tcpdump",ret):
                return True
            self.waitTime(1)
        return False
    def PKT_Mss(self,kargs='{}'):
        self.sendCmd("killall -9 tcpdump")
        init_default_dict = {"mss":"",'result':"/tmp/packet","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        ret = self.sendCmd("cat %s"%kargs['result'])
        print "ret",ret
        if kargs['expe'] == 'pass':
            flag = False
        else:
            flag = True
        flag1= False
        if re.search("mss %s"%kargs['mss'],ret):
            flag1 = True
        return flag1|flag
    def parserPacket(self,kargs='{}'):
        self.sendCmd("killall -9 tcpdump")
        self.waitTime(5)
        #tshark解析数据包是否包含字段进行匹配
        #filter = ip.src=1.1.1.1,ip.dst=1.1.1.2,eth.type = 0x8864,ppp.code = 9,eth.dst = c8:3a:35:d4:96:6f
        #num 表示匹配filter的次数 bootp.option.static_route.ip = 
        init_default_dict = {"filter":"a=1","result":"/tmp/packet.pcap","num":"1","expe":"pass"}
        kargs = self.init_args(kargs,**init_default_dict)
        #filter使用“,‘分格
        retlst = kargs['filter'].split(",")
        keylst = []
        #valuelst = ""
        valuelst = []
        for i in retlst:
            k,v = i.split("=",1)
            keylst.append(k)
            valuelst.append(v)
        valuelst1 = []
        for value in valuelst:
            value = value.strip()
            valuelst1.append(value)
        valuelst = valuelst1
        cmd = ["tshark -r %s -T fields" %(kargs['result'])]
        location = []
        sumlocation = []
        for j,key in enumerate(keylst):
            cmd.append("-e %s" %(key))
            print "cmd:",cmd
            # ret = self.sendCmd(cmd)
            ret = self.sendCmd(" ".join(cmd))
            for i,element in enumerate(ret.split("\n")):
                if valuelst[j] in element.split(' '): 
                    location.append(i)
                elif valuelst[j] in element.split(','):
                    location.append(i)
            sumlocation.append(location)
            location = []
            cmd = ["tshark -r %s -T fields" %(kargs['result'])]
        print "sumlocation",sumlocation
        sums=0
        #几组过滤条件
        lens=len(sumlocation)
        lenss=len(sumlocation[0])
        if lens!=1:
            for i in range(lenss):
                sumss=0  
                for j in range(lens):
                    if sumlocation[0][i] in sumlocation[j]:
                        sumss = sumss+1 
                    if sumss==lens:
                        sums = sums+1        
        else:
            sums=lenss
        print "lens:",lens
        print "sums:",sums
        try:
            kargs['num'] = int(kargs['num'])
        except:
            kargs['num'] = 1
        if kargs['num'] <= sums and sums!=0:            
            result = "pass"
        else:
            result = "fail"
        if kargs['expe'] == result:
            print u"#######所有字段匹配成功%s次#######"%sums
            print u"#######大于等于预期%s次    #######"%kargs['num']
            return True
        else:
            return False
    def init_args(self,args,**kargs):
        retdict =eval(args)
        for k,v in kargs.iteritems():
            if not retdict.has_key(k):
                retdict[k] = v
        return retdict
  
    def parserdict(self,key,value,**kargs):
        #如果kargs字典中无key 则返回value
        if kargs.has_key(key):
            return kargs[key]
        else:
            return value
    def login(self):
        #循环三次进行登录判断
        password = "Fireitup"
        for i in range(3):
            text = self.read_cominfo()
            print "1111++++++++"
            self.sendCmd(password)
            print "++++++++"
            logindata=self.read_cominfo()
            print "----------"
            print "logindata=",logindata
            print "----------"
            if logindata.find("~ #") >= 0:
                print u"登录成功"
                return True
            else:
                print u"第%d次登录失败" %(i)
            self.waitTime(5)
        return False
    def sendCmd(self,cmd):
        #用于在函数中调用
        if self.type == "ssh":
            print "cmd=",cmd
            stdin,stdout,sterr = self.t.exec_command(cmd)
            # stdout.flush()
            results=stdout.read()  
            self.waitTime(1)
            # print results
            return results
            # self.t.close())
        elif self.type == "telnet":
            self.t.write(cmd+"\n")
            self.waitTime(1) ;#很重要
            return self.t.read_some()
        elif self.type == "com":
            cmd="""%s\x0d\x0a""" %(cmd)
            print "cmd",cmd
            # cmd=self.str2bin(cmd)
            self.t.write(cmd)
            self.waitTime(1)
            return self.read_cominfo()
            #return True
        elif self.type == "adb":
            pipe = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            cmdlst = ["su",cmd,'exit','exit']
            code = pipe.communicate("\n".join(cmdlst) + "\n")
            retstr = ""
            for i in code:
                retstr = retstr+str(i)+"\n"
            return retstr
    def sendCmds(self,cmd):
        
        if self.type == "ssh":
            print "cmd=",cmd
            self.t.exec_command(cmd)
            self.waitTime(10)
            return True
    def read_cominfo(self):
        alldata=""
        while True:
            data=self.t.readlines()
            if data:
                alldata = "".join(data)
                break
        print "alldata=",alldata
        return alldata
        
    def reboot(self):
        #dut reboot
        self.sendCmd("reboot")
        for i in range(0,20):
            #wait for 30 seconds
            self.waitTime(1)
            print "i=%d/20" %(i)
        if self.login():
            for j in range(0,20):
                self.waitTime(1)
                print "i=%d/20" %(j)
                self.waitTime(1)  
            return True
        else:
            return False
    def face_updown(self,nums,iface = 'eth1'):
        cmdlist=[]
        cmdlist.append('ifconfig %s down'%iface)
        cmdlist.append('ifconfig %s up'%iface)
        for num in xrange (nums):
            for cmd in cmdlist: 
                self.sendCmd(cmd)
                self.waitTime(3)
        return True
    #用于在用例中直接调用
    def sendcmd(self,cmd):
        if self.type == "ssh":
            print "cmd=",cmd
            stdin,stdout,sterr = self.t.exec_command(cmd)
            return True
            
    #用于串口调用函数比对
    def return_func(self,value):
        return value
    def close(self):
        self.t.close()
        return True
    #用于跑流方法
    #src=192.168.5.125 源地址
    #dst=192.168.30.1  目的地址
    #pro=udp tcp       跑流协议   
    #size=1500         包大小
    #upnum=0           上行流的数目 -1表示全部上行
    #num=10            流的总条数
    #expenum=100       预期流量值单位Mbps
    #runtime=30        流持续时间
    #headlen=0         包头长度
    #errallow=0.10     允许误差值10%
    #iface=eth1        windows电脑网卡接口名 
    #gateway           windows电脑网卡gateway
    #dns               windows电脑网卡dns
    #mask              windows电脑网卡mask
    def IxChariot(self,kargs ='{}'):
        init_default_dict = {"iface":"eth1","mask":"255.255.255.0","gateway":"192.168.5.1","dns":"192.168.5.1","src":"192.168.5.125","dst":"192.168.30.1","pro":"tcp","size":1500,"upnum":0,"num":10,"expenum":10,"runtime":30,"headlen":0,"errallow":"0.10","tclpath":"","manageip":""}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['manageip'] =='':
            #设置网卡Windows Ip地址
            self.windows_iface_mode(str({"iface":kargs['iface'],"ip":kargs['src'],"mask":kargs['mask'],"gateway":kargs['gateway'],"dns":kargs['dns']}))
            self.waitTime(5)
        if kargs['tclpath'] !='':
            IxchaDir = kargs['tclpath']
        #print "IxchaDir",IxchaDir
        # cmd ='%s src=%s dst=%s pro=%s size=%d upnum=%d num=%d expenum=%d runtime=%d headlen=%d errallow=%f'%(IxchaDir,kargs['src'],kargs['dst'],kargs['pro'],int(kargs['size']),int(kargs['upnum']),int(kargs['expenum']),int(kargs['runtime']),int(kargs['headlen']),float(kargs['errallow']))
        cmd ='tclsh %s src=%s dst=%s pro=%s size=%s upnum=%s num=%s expenum=%s runtime=%s headlen=%s errallow=%s manageip=%s'%(IxchaDir,kargs['src'],kargs['dst'],kargs['pro'],int(kargs['size']),int(kargs['upnum']),int(kargs['num']),int(kargs['expenum']),int(kargs['runtime']),int(kargs['headlen']),float(kargs['errallow']),kargs['manageip'])
        print "cmd",cmd
        wtime=int(kargs['runtime'])+10
        wtime = wtime*3
        result1=os.popen(cmd)
        for _ in range(wtime):
            self.waitTime(1)
            cmd2='tasklist | findstr "WerFault.exe"'
            result = os.popen(cmd2)
            result = result.read()
            print "result",result
            if 'WerFault.exe' in result:
                cmd1 = 'taskkill /im WerFault.exe /f'
                os.system(cmd1)
                break
        result1 = result1.read()
        print "result1",result1
        if 'result pass' in result1:
            if kargs['manageip'] =='':
                self.windows_iface_mode(str({"iface":kargs['iface'],"ip":"1.1.1.1","mask":kargs['mask'],"gateway":"","dns":""}))
            return True
        else:
            if kargs['manageip'] =='':
                self.windows_iface_mode(str({"iface":kargs['iface'],"ip":"1.1.1.1","mask":kargs['mask'],"gateway":"","dns":""}))
            return False
    def windows_iface_mode(self,kargs='{}'):
        init_default_dict = {"iface":"eth1","mode":"static","ip":"1.1.1.1","mask":"255.255.255.0","gateway":"","dns":""}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == 'dhcp':
            cmd = 'netsh interface ip set dns %s dhcp'%kargs['iface']
            os.system(cmd)
            cmd1 = 'netsh interface ip set address %s dhcp'%kargs['iface']
            os.system(cmd1)
        else:
            cmd = 'netsh interface ip set address %s static %s %s %s'%(kargs['iface'],kargs['ip'],kargs['mask'],kargs['gateway'])
            os.system(cmd)
            cmd1 = 'netsh interface ip set dns %s static %s'%(kargs['iface'],kargs['dns'])
            os.system(cmd1)
    #使用U12连接无线      
    def u12_wireless_connect(self,kargs='{}'):
        #U12ConnectDir 网卡配置bat 文件路径
        #iface 无线网卡名称 ra0
        #ssid tenda
        #pwd 12345678
        #authmod WPAPSK/WPA2PSK
        #encryptype AES/TKIP
        #mac 传入需要修改的mac地址 格式为829b20097842
        #mode 网络模式 auto=8 a=1 an=32 anac=64 ac=256 b=2 bg=4 bgn=16
        #dip 上级Ip地址 当wifi连接成功之后查看是否可以ping通上级
        #expe 期待是否可以连接成功
        init_default_dict = {'dir':'','iface':'ra0','ssid':'','pwd':'','authmode':'WPA2PSK','encryptype':'AES','mac':'829b20097842','mode':'8','expe':'pass'}
        kargs = self.init_args(kargs,**init_default_dict)
        print kargs
        if kargs['dir'] =='':
            kargs['dir'] = U12ConnectDir
        cmd ='%s %s %s %s %s %s %s %s'%(kargs['dir'],kargs['iface'],kargs['ssid'],kargs['pwd'],kargs['authmode'],kargs['encryptype'],kargs['mac'],kargs['mode'])
        flag1 = False
        for i in range(3):
            result = os.popen(cmd)
            result = result.read()
            print "result",result
            if kargs['expe'] != 'pass':
                if 'connect_fail' in result:
                    print u"无线网卡连接失败"
                    break
            if 'connect_pass' in result:
                flag1 = True
                print u"无线网卡连接成功"
                break
        if kargs['expe'] == 'pass':
            flag2 = False
        else:
            flag2 = True
        if flag1^flag2:
            return True
        else:
            return False
    #检查无线网卡连接信息
    #运行一次检查一个参数
    def check_wireless_info(self,kargs='{}'):
        #channel
        #mode
        #mac地址
        #连接速率
        #加密方式
        #名称                   : ra0
        #描述                   : Tenda Wireless USB Adapter
        #GUID                   : 5d6c5177-0a06-44ac-ae1a-ac7743c61737
        #物理地址               : 82:9b:20:56:ae:59
        #状态                   : 已连接
        #SSID                   : NOVA_79D8
        #BSSID                  : c8:3a:35:ef:79:f1
        #网络类型               : 结构
        #无线电类型             : 802.11n
        #身份验证               : WPA2 - 个人
        #密码                   : CCMP
        #连接模式               : 配置文件
        #信道                   : 149
        #接收速率(Mbps)         : 867
        #传输速率 (Mbps)        : 867
        #信号                   : 100%
        init_default_dict = {'channel':'','mode':'','speed':'','mac':''}
        kargs = self.init_args(kargs,**init_default_dict)
        print kargs
        cmd = 'netsh wlan show interfaces'
        result = os.popen(cmd)
        result = result.read()
        print "result",result
        if kargs['channel']!= '':
            kargs['channel'] = ': '+kargs['channel']
            if kargs['channel'] in result:
                return True
        if kargs['mode']!= '':
            kargs['mode'] = ': 802.11'+kargs['mode']
            if kargs['mode'] in result:
                return True
        if kargs['speed']!= '':
            kargs['speed'] = ': '+kargs['speed']
            if kargs['speed'] in result:
                return True
        if kargs['mac']!= '':
            kargs['mac'] = ': '+kargs['mac']
            if kargs['mac'] in result:
                return True
        return False
    #拉起ping包 重定向至pingtest.txt
    def ping_redirect(self,kargs='{}'):
        #iface ra0
        #dip 192.168.5.1
        #dir: pingtest.txt
        #num 60 ping包个数
        init_default_dict = {'iface':'ra0','dip':'192.168.5.1','dir':'pingtest.txt','num':'60'}
        kargs = self.init_args(kargs,**init_default_dict)
        print kargs
        cmd = 'rm -rf pingtest.txt'
        self.t.exec_command(cmd)
        cmd = 'ping %s -I %s -c %s >> %s'%(kargs['dip'],kargs['iface'],kargs['num'],kargs['dir'])
        self.t.exec_command(cmd)
        return True
    #检查ping包是否,在预期范围内则返回成功，否则存在丢包返回失败
    def check_ping_lost(self,dir='pingtest.txt'):
        cmd = 'cat %s'%dir
        stdin,stdout,sterr = self.t.exec_command(cmd)
        # stdout.flush()
        results=stdout.read() 
        if '0% packet loss' in results:
            return True
        else:
            return False
    #检查无线网卡所连接的信号的mac地址是否与传入的一致
    def check_ap_mac(self,kargs='{}'):
        #iface = ra0
        #mac = C8:3A:35:EF:79:E9
        init_default_dict = {'iface':'ra0','mac':'C8:3A:35:EF:79:E9'}
        kargs = self.init_args(kargs,**init_default_dict)
        print kargs
        cmd = 'iwpriv %s connStatus'%kargs['iface']
        stdin,stdout,sterr = self.t.exec_command(cmd)
        results=stdout.read() 
        if kargs['mac'] in results:
            return True
        else:
            return False
parity=PARITY_NONE
class ks():
    def __init__(self,**kargs):
        print 'kargs=',kargs
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs.has_key('iface'):
            self.expe = kargs['iface']
        else:
            self.expe = 'br0'
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        else:
            # self.expe =G_MainDict['dut']['dip']             
            self.expe = '192.168.5.1'             
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'            
        if kargs.has_key('passwd'):
            self.passwd=b64encode(kargs['passwd'])
        else:
            self.passwd=''
        try:
            self.mpp_passwd=b64encode(G_MainDict["dut"]["wifi_password"])
        except:
            pass
        try:
            self.map1_passwd=b64encode(G_MainDict["map1"]["wifi_pwd"])
        except:
            pass
        try:
            self.map2_passwd=b64encode(G_MainDict["map2"]["wifi_pwd"])
        except:
            pass
        if kargs.has_key('PORT'):
            self.PORT=kargs['PORT']
            self.PORT=int(self.PORT)
            print "PORT=",self.PORT
        else:
            self.PORT = 12345   
        ip_port = ('127.0.0.1',self.PORT)
        self.ip_port = ip_port
        try:
            self.socket_connect()
        except Exception,e:
            print "not open socket"
        print "-------connect success-------"
        if self.login():
            print 'login success'
        print "_________"
        self.close()
        if kargs.has_key('waitflag'):
            flags = kargs['waitflag']
        else:
            flags = True
        if kargs.has_key('reset'):
            if kargs['reset'] == 'yes':
                self.reset(flag=flags)
    def socket_connect(self):
        sk = socket.socket()
        self.sk = sk
        self.sk.connect_ex(self.ip_port)
        return self.sk
    def waitTime(self,num):
        try:
            for x in xrange(int(num)):
                print "%d/%d sum=%d" %(x,num,num)
                time.sleep(1)
            return True
        except:
            return False
    def init_args(self,args,**kargs):
        retdict =eval(args)
        for k,v in kargs.iteritems():
            if not retdict.has_key(k):
                retdict[k] = v
        return retdict
    @catch_exception
    def config_rssi(self,num):
        cmd=""
        self.send_cmd(cmd)
    '''
        用于类中调用
    '''
    def send_cmd(self,cmd):
        # print "cmd",cmd
        try:
            self.sk.send(cmd)
        except socket.error,e:
            # print "error",e  
            pass
    '''
        用于用例中调用
    '''    
    @catch_exception
    def sendCmd(self,cmd):
        # print "cmd",cmd
        try:
            self.sk.send(cmd)
            # alldata=self.sk.recv(4096)
            return True
        except socket.error,e:
            print "error",e  
            return False
    def recv_cmd(self):
        alldata=""
        try:
            alldata=self.sk.recv(4096)
            # print "alldata",alldata
            return alldata
        except socket.error,e:
            print "error",e  
    def readfromcom(self):
        alldata=""
        while True:
            data=self.recv_cmd()
            if data:
                alldata = "".join(data)
                break
        print "alldata=",alldata
        return alldata
        
    """
        用于重启设备
    """
    @catch_exception
    def reboot(self,pwd=None):
        print "reboot pwd",pwd
        # self.waitTime(5)
        if pwd:
            self.passwd=b64encode(pwd)
            print "reboot self.passwd",self.passwd
            # self.waitTime(5)
        self.send_cmd("iwpriv wlan2 write_reg b,23,c")
        self.send_cmd("reboot")
        # text = self.recv_cmd()
        self.close()
        self.socket_connect()
        for i in range(0,60):
            print "i=%d/60" %(i)
            self.waitTime(1)
        if self.login():
            self.send_cmd("iwpriv wlan2 write_reg b,23,c")
            return True
        else:
            return False
    """
        用于恢复出厂设置
    """
    @catch_exception
    def reset(self,num=60,flag=True):
        num = int(num)
        try:
            flag=flag.capitalize()
        except:
            pass
        try:
            flag = eval(flag)
        except:
            pass
        self.send_cmd("iwpriv wlan2 write_reg b,23,c")
        self.send_cmd("cfm restore;reboot")
        if flag:
            for i in range(0,num):
                self.waitTime(1)
                print "i=%d/%d" %(i,num)
            # text = self.recv_cmd()
            self.close()
            self.socket_connect()
            for j in xrange(10):
                if self.login():
                    self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                    return True
                else:
                    self.waitTime(5)
        return True
        
    """ 
        从串口判断mesh的时区是否同步，
        使用cfm get sys.timezone.offset.sec命令
        timezone参数为当前时区与GMT+00时区的偏移秒数，如GMT+02为2*3600=7200
    """
    @catch_exception
    def checkTimezone(self,timezone):
        timezone = str(timezone)
        for i in range(6):
            self.send_cmd('cfm get sys.timezone.offset.sec')
            text = self.recv_cmd()
            try:
                print timezone
                print text.strip()
                if timezone in text.strip():
                    return True   
            except Exception,e:
                pass
        return False
    """ 
        从串口判断mesh的时间是否同步，
        使用date命令重串口读取时间
        time参数为对比时间，形式如“2018-06-20 18:15:02”
        maxErr参数为允许的最大误差
    """
    @catch_exception
    def checkTime(self,timess,maxErr):
        month_dict = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sept":"09","Oct":"10","Nov":"11","Dec":"12"}
        #处理预期时间，日期转化为xxxx-xx-xx，时间转化为已秒为单位
        expect_date = timess.split(" ")[0]
        print "expect_date",expect_date
        expect_time = timess.split(" ")[1]
        print "expect_time",expect_time
        expect_time_s = int(expect_time.split(":")[0])*3600+int(expect_time.split(":")[1])*60+int(expect_time.split(":")[2])
        print "expect_time_s",expect_time_s
        #获取路由器时间并处理为与上面时间同一种形式
        for i in range(6):
            try:
                self.send_cmd('date')
                line = self.recv_cmd()
                date = ""
                if "UTC" in line.strip():
                    date = line.strip()
                print "---------------------------"
                print "date",date
                print "+++++++++++++++++++++++++++"
                date = date.split("\r\n")
                date = date[1]
                print "1111",date
                date_list = date.split(" ")
                date_list = list(filter(None, date_list)) # 去除date_list中的空字符
                print 'date_list',date_list
                print "date_list[2]",date_list[2]
                if len(date_list[2])==1:
                    date_list[2] = '0'+date_list[2]
                try:
                    fact_date = date_list[5]+"-"+month_dict[date_list[1]]+"-"+date_list[2]   
                    print "fact_date",fact_date
                except Exception,e:
                    print e
                fact_time = date_list[3]
                print "fact_time",fact_time
                fact_time_s = int(fact_time.split(":")[0])*3600+int(fact_time.split(":")[1])*60+int(fact_time.split(":")[2])
                print "fact_time_s",fact_time_s
                if expect_date == fact_date and abs(fact_time_s-expect_time_s) <= maxErr:
                    return True 
            except Exception,e:
                pass
        return False
    """
        从串口读取iptables nat表MINIUPNPD链的内容
    """
    #重复
    # def checkUpnp(self,*args):
        # self.send_cmd('iptables -t nat -nvL')
        # text = self.readfromcom()
        # re.findall(r'Chain MINIUPNPD (1 references)(+)?Chain',text)
    def login(self,pwd=''):
        #循环三次进行登录判断
        def revlog():
            self.waitTime(4)
            logindata=self.readfromcom()
            print "logindata",logindata
            if logindata.find("~ #") >= 0:
                print u"登录成功"
                return True
            else:
                print u"第%d次登录失败" %(i)
        if pwd:
            passwd =b64encode(pwd)
        else:
            passwd = self.passwd
        for i in range(4):
            #主节点密码
            try:
                self.mpp_passwd = self.mpp_passwd+'\n'
                self.send_cmd(self.mpp_passwd)
                if revlog():
                    self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                    return True
            except:
                pass
            passwd = passwd+'\n'
            self.send_cmd(passwd)
            if revlog():
                self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                return True
            #次节点1密码
            try:
                self.map1_passwd = self.map1_passwd+'\n'
                self.send_cmd(self.map1_passwd)
                if revlog():
                    self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                    return True
            except:
                pass
            #次节点2密码
            try:
                self.map2_passwd = self.map2_passwd+'\n'
                self.send_cmd(self.map2_passwd)
                if revlog():
                    self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                    return True
            except:
                pass
            #Fireitup
            self.send_cmd('Fireitup\n')
            if revlog():
                self.send_cmd("iwpriv wlan2 write_reg b,23,c")
                return True
        return False
    '''
        "ip":"192.168.5.1"
        "iface":"br0"
        "expe":"pass"
        通过串口检查DUT各端口配置参数
        如 IP地址 MTU值 等 
        如传入参数与串口读取抑一致则返回 True
    '''
    @catch_exception
    def checkIp(self,kargs='{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        if kargs.has_key('iface'):
            self.iface = kargs['iface']
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            self.send_cmd('ifconfig %s'%self.iface)
            text = ''
            # with eventlet.Timeout(2,False):
            text = self.recv_cmd()
            # print "text",text
            try:
                if re.search(self.ip,text):
                    flag = True    
                    break
                    print "flag",flag
            except Exception,e:
                print e
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False

    #@catch_exception
    def getChannel(self,kargs='{}'):
        kargs = eval(kargs)
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        self.socket_connect()
        for i in range(5):
            self.send_cmd('%s'%self.iface)
            text_line = self.recv_cmd()
            regex = r'dot11channel:([\s\S]*)dot11ch_low'
            matchs = re.findall(regex,text_line)
            
            print "6666666666666666666666666666666666666666666"
            print text_line
            
            
            try:
                ch5g = matchs[0].strip()
                
            except:
                pass
            print "dot11channel:",ch5g
            if ch5g:
                break
        return ch5g


    @catch_exception
    def getIp(self,kargs='{}'):
        # print "1232"
        init_default_dict = {"iface":"br0","ip":"","mask":"","mac":"","mtu":""}
        try:
            kargs = self.init_args(kargs,**init_default_dict)
        except Exception,e:
            print "error = ",e
        # print "2222"
        retdict = {"iface":kargs['iface']}
        for i in range(5):
            try:
                self.send_cmd('ifconfig %s'%kargs['iface'])
                # print "666666"
                ret = self.recv_cmd()
                # print "777777"
                macinfo = re.findall("(HWaddr.*)",ret)
                ipinfo = re.findall("(inet addr:[0-9.]+)",ret)
                maskinfo = re.findall("(Mask:[0-9.]+)",ret)
                mtuinfo = re.findall("(MTU:[0-9]+)",ret)
                if macinfo:
                    retdict['mac'] = macinfo[0].strip().split(" ")[-1]
                    break
            except Exception,e:
                pass
        if macinfo:
            retdict['mac'] = macinfo[0].strip().split(" ")[-1]
        if ipinfo:
            retdict['ip'] = ipinfo[0].strip().split(":")[-1]
        if maskinfo:
            retdict['mask'] = maskinfo[0].strip().split(":")[-1]
        if mtuinfo:
            retdict['mtu'] = mtuinfo[0].strip().split(":")[-1]
        return retdict
    '''
        向串口循环发送 
        ifconfig %s down
        ifconfig %s up
        模拟反复插拔WAN口网线
        num 控制 插拔次数
        iface 模拟端口
    '''
    @catch_exception
    def face_updown(self,nums,iface = 'eth1'):
        cmdlist=[]
        cmdlist.append('ifconfig %s down'%iface)
        cmdlist.append('ifconfig %s up'%iface)
        print "666"
        try:
            for num in xrange (int(nums)):
                print nums
                for cmd in cmdlist: 
                    print "777"
                    self.send_cmd(cmd)
                    print "888"
                    self.waitTime(3)
            return True
        except Exception,e:
            print "error = ",e
    '''
        串口抓包
    '''
    @catch_exception
    def packetCapture(self,kargs='{}'):
        #tcpdump开启抓包
        init_default_dict = {"iface":"br0","filter":"",'result':"/tmp/packet.pcap"}
        kargs = self.init_args(kargs,**init_default_dict)
        # cmd = "tcpdump -i %s %s -w %s  >/dev/null 2>&1 &"  %(kargs['iface'],kargs['filter'],kargs['result'])
        cmd = "tcpdump -i %s -w %s &" %(kargs['iface'],kargs['result'])
        self.send_cmd("killall -9 tcpdump")
        self.waitTime(3)
        self.send_cmd(cmd)
        self.waitTime(5)
        return True
        
    '''
        串口停止抓包并将包传输到pc
        注意运行此函数前，pc端需要开启tftp服务器
    '''
    @catch_exception
    def packetStop(self,kargs='{}'):
        init_default_dict = {"ip":""}
        kargs = self.init_args(kargs,**init_default_dict)
        self.send_cmd("killall -9 tcpdump")
        self.waitTime(5)
        self.send_cmd('cd tmp')
        cmd = "tftp -pl packet.pcap %s" %(kargs['ip'])   
        self.send_cmd(cmd)
        self.waitTime(20)
        self.send_cmd('cd ..')
        
        return True
    ''' 
        串口检查UPNP功能是否开启
        target =  'MINIUPNPD' 
        sent   =  'iptables -t nat -nvL'
        expe   =  'pass' or 'fail'
    '''
    @catch_exception
    def checkUpnp(self,kargs='{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            self.waitTime(1)
            self.send_cmd('%s'%self.iface)
            text_line = ''
            text_line = self.recv_cmd()
            print "text_line",text_line
            try:
                text_line = text_line.strip()
            except:
                pass
            if re.match(self.ip,text_line):   # re.search
                flag = True    
                break
            else :
                pass
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False  
    ''' 
        串口检查UPNP功能是否开启
        target =  'MINIUPNPD' 
        sent   =  'iptables -t nat -nvL'
        expe   =  'pass' or 'fail'
    '''
    @catch_exception
    def checkUpnp_count(self,kargs='{}',count=False,num=''):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            self.send_cmd('%s'%self.iface)
            text_line = self.recv_cmd()
            print "text_line",text_line
            try:
                text_line = text_line.strip()
            except:
                pass
            if re.search(self.ip,text_line):
                flag = True    
                break
            else :
                pass
        text_line = text_line.split(self.ip)
        target_num = len(text_line)-1
        if count==True and num=='':
            return target_num
        elif count == True and num != '':
            if int(num) <= target_num + 2:
                return True
            else:
                return False
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False  
    ''' 
        串口检查Guest功能是否开启
        target =  '192.168.11.31,192.168.11.254' 
        sent   =  'cat /etc/dhcps.conf'
        expe   =  'pass' or 'fail'
    '''
    @catch_exception
    def checkGuest(self,kargs='{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(10):
            self.send_cmd('%s'%self.iface)
            text_line = self.recv_cmd()
            print "text_line",text_line
            try:
                text_line = text_line.strip()
            except:
                pass
            if re.search(self.ip,text_line):
                flag = True    
                break
            else :
                pass
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False  
    ''' 
        串口检查Main_wifi地址池
        target =  '192.168.5.31,192.168.5.254' 
        sent   =  'cat /etc/dhcps.conf'
        expe   =  'pass' or 'fail'
    '''
    @catch_exception
    def checkMain_wifi(self,kargs='{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(10):
            self.send_cmd('%s'%self.iface)
            text_line = self.recv_cmd()
            print "text_line",text_line
            try:
                text_line = text_line.strip()
            except:
                pass
            if re.search(self.ip,text_line):
                flag = True    
                break
            else :
                pass
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False  
    #用于进程占用率检测
    #cmd = 'top -n 1 |grep "ucloud -l" |grep -v grep'
    #num =15
    @catch_exception
    def checkucloud(self,cmd,num):
        self.socket_connect()
        for i in range(15):
            try:
                self.send_cmd(cmd)
                tops =self.recv_cmd()
                tops=tops.split('\n')
                tops = tops[1].strip()
                tops = tops.split()
                print "tops=",tops
                try:
                    if float(num)>float(tops[7]):
                        return True
                except:
                    pass
            except Exception,e:
                pass
        self.close()
        return False
    #phonetime = '18-15'(h.m)
    @catch_exception
    def checkDateTime(self,phonetime):
        self.socket_connect()
        for i in range(5):
            self.send_cmd('date +"%H-%M"')
            tops =self.recv_cmd()
            print "tops=",tops
            try:
                if phonetime in tops:
                    return True
            except:
                pass
        self.close()
        return False
    '''
        检查上电时间，并比较
        
    '''
    
    #phonetime = '18-15'(h.m)
    #检查手机时间和设备时间是否一致
    @catch_exception
    def checkPhoneDutTime(self):
        self.socket_connect()
        for i in range(5):
            self.send_cmd('date +"%H-%M"')
            tops =self.recv_cmd()
            print "tops=",tops
            # phonetime=shell("date +'%H-%M'").read().strip()
            cmd = """adb shell  su -c "date +'%H-%M'" """
            phonetime = os.popen(cmd)
            phonetime=phonetime.read().strip()
            print "phonetime=",phonetime
            try:
                if phonetime in tops:
                    return True
            except:
                pass
        self.close()
        return False
        
    '''
        检查上电时间，并比较
        
    '''
    @catch_exception
    def checkupTime(self,kargs='{}'):
        self.login()
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.uptime = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            try:
                self.send_cmd('%s'%self.uptime)
                text_line = self.recv_cmd()
                text_line = text_line.split('uptime')[1]
                text_line = text_line.split('up')[1]
                if 'min' in text_line:
                    break
            except Exception,e:
                print e
                pass
        if 'min' in text_line:
            text_line = text_line.split('min')[0]
            min = text_line.strip()
            print "min=",min
            print "min type",type(min)
        else:
            print u"上电时间超过1小时"
            return False 
        if int(min) < int(kargs['target']):
            flag = True
            print u"target真值"
        if self.expe == 'pass':
            flags = False
            print u"pass 真值"
        else:
            flags = True
            print u"fali 假值"
        print "flag=",flag
        print "flags=",flags
        if flag^flags:
            return True
        else:
            return False
    @catch_exception
    def checkMtu(self,kargs='{}'):
        kargs = eval(kargs)
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs['iface'] != "":
            for i in range(5):
                try:
                    self.send_cmd('ifconfig %s' %kargs['iface'])
                    text = self.recv_cmd()
                    print "text=",text
                    if kargs['mtu'] != "":
                        factmtu = re.search(r'MTU:([0-9]+)',text).group(1)
                        print "********factmtu=",factmtu
                        if factmtu.lstrip("") == kargs['mtu']:
                            flag = 1
                        else:
                            flag = 0
                    if flag==1:
                        break
                except Exception,e:
                    print e
                    pass
        if kargs['expe'] == "pass" and flag == 1:
            return True
        elif kargs['expe'] == 'fail' and flag == 0:
            return True
        else:
            return False  
    '''
        检查无线客户端数量
    '''
    @catch_exception
    def check_Wireless_Client(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('target'):
            self.ip = kargs['target']
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            try:
                self.send_cmd('%s'%self.iface)
                #等待时间非常重要
                text_line = self.recv_cmd()
                text_line = text_line.split(':')[1]
                text_line = text_line.split(')')[0]
                text_line = text_line.split(' ')[1]
            except:
                pass
            print "text_line=",text_line
            if text_line == kargs['target']:
                flag = True
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False    
    '''
        检查漫游是否开启
    '''
    @catch_exception
    def check_Fast_Roaming(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('sent'):
            self.iface = kargs['sent']
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        print "555"
        for i in range(5):
            self.send_cmd('%s'%self.iface)
            #等待时间非常重要
            # self.waitTime(1.5)
            text_line = self.recv_cmd()
            try:
                print "text_line",text_line
                text_line = text_line.split('get_mib:')[1]
                print "text_line1",text_line
                # text_line = text_line.split(' ')[0]
                text_line = text_line.split(' ')
                print "text_line2",text_line
                # if text_line == kargs['target']:
                if  kargs['target'] in text_line:
                    flag = True
                    break
            except:
                pass
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        print (flag,flags)
        if flag^flags:
            return True
        else:
            return False      
    '''
        检查LAN、WAN口连接速率 consult
        port （Port0，Port1，Port2，Port3，Port4）
        speed (1G 100M 10M)
        mode  (Eabled Disabled) 这里Eabled指的是Eabled Duplex 使用全双工模式 
              1G速率只有全双工模式 
              Mesh只能自协商 设置上级的双工模式为非自协商时100M
              100M速率只能协商出半双工的工作模式 ，无法匹配出100M的全双工
              所以1G速率 肯定是双工模式 Eabled Duplex
              100M速率 只有是半双工模式 Disabled Duplex
    '''
    @catch_exception
    def check_link_speed(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('port'):
            self.port = kargs['port']
        else:
            self.port = ''
        if kargs.has_key('speed'):
            self.speed = kargs['speed']
        else:
            self.speed = ''
        if kargs.has_key('mode') :
            self.mode = kargs['mode']
        else:
            self.mode = ''
        for i in range(5):
            try:
                self.send_cmd('cat /proc/rtl865x/port_status |grep -A 3 %s'%self.port)
                #等待时间非常重要
                text_line = self.recv_cmd()
                print "text_line",text_line
                speed = text_line.split('| ')[3]
                speed = speed.split('~')[0]
                speed = speed.split(' ')[1]
                speed = speed.strip()
                print "speed =",speed
                mode  = text_line.split('Duplex ')[1]
                mode  = mode.split(' |')[0]
                print "mode =",mode
                if speed == self.speed:
                    flag = True
                    break 
            except Exception,e:
                print "false",e
                pass
        if mode == self.mode:
            flags = False
        else:
            flags = True
        print (flag,flags)
        if flag^flags:
            return True
        else:
            return False    
    '''
       检查当前设备的角色
       role=1固定MPP
       role=3临时MPP
       role=4为MAP
       send "cfm get sys.role "
    '''
    @catch_exception
    def check_role(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('role') :
            self.role = kargs['role']
        else:
            self.role = ''
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            self.send_cmd('cfm get sys.role')
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                role = self.recv_cmd()
                role = role.split('cfm get sys.role')[1]
                role = role.split('~ #')[0]
                role = role.strip()
                print "role =",role
                if int(role) == int(self.role):
                    break
            except Exception,e:
                pass
        if int(role) == int(self.role):
            flag = True        
        else:
            flag = False
            
        if self.expe == 'pass':
            flags = False
        else:
            flags = True
        if flag^flags:
            return True
        else:
            return False  
    #dns1 = ''
    #dns2 = ''
    #expe = 'pass'
    @catch_exception
    def check_dns(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            try:
                self.send_cmd('cat /etc/dns.conf')
                role = self.recv_cmd()
                print "role",role
                if kargs.has_key('dns1') and kargs.has_key('dns2'):
                    if kargs['dns1'] in role and kargs['dns2'] in role:
                        flag = True
                        break
                elif kargs.has_key('dns1'):
                    print "role",role
                    if kargs['dns1'] in role :
                        flag = True
                        break
                else:
                    if kargs['dns2'] in role :
                        flag = True
                        break
            except Exception,e:
                pass
        if flag and self.expe=='pass':
            return True        
        elif not flag and self.expe =='fail':
            return True
        else:
            return False
    '''
        用于从串口检查设备 主网络ssid 是否和传入的一致
        send "cfm get wl2g.ssid0.ssid"
        send "cfm get wl5g.ssid0.ssid"
        band:2g
        band:5g
        ssid:12345678
    '''
    @catch_exception
    def check_main_ssid(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('ssid') :
            self.ssid = kargs['ssid']
        else:
            self.ssid = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wl2g.ssid0.ssid'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wl5g.ssid0.ssid'
        else:
            return False
        for i in range(5):
            try:
                self.send_cmd(cmd)
                #等待时间非常重要
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('cfm get wl2g.ssid0.ssid')[1]
                else :
                    recv_cmd = recv_cmd.split('cfm get wl5g.ssid0.ssid')[1]
                recv_cmd = recv_cmd.split('~ #')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.ssid == recv_cmd :
                    break
            except Exception,e:
                pass
        if self.ssid == recv_cmd :
            return True        
        else:
            return False    
    '''
        用于从串口检查设备 主网络pwd 是否和传入的一致
        send "cat var/run/wlan1_ssid_sync.sh "
        send "cat var/run/wlan0_ssid_sync.sh "
        band:2g
        band:5g
        pwd:12345678
    '''
    @catch_exception
    def check_main_pwd(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('pwd') :
            self.pwd = kargs['pwd']
        else:
            self.pwd = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cat var/run/wlan1_ssid_sync.sh |grep "iwpriv wlan1 set_mib passphrase"'
            elif kargs['band'] == '5g':
                cmd = 'cat var/run/wlan0_ssid_sync.sh |grep "iwpriv wlan0 set_mib passphrase"'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('iwpriv wlan1 set_mib passphrase="')[1]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('iwpriv wlan0 set_mib passphrase="')[1]
                recv_cmd = recv_cmd.split('"')[0]            
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.pwd == recv_cmd :
                    break
            except Exception,e:
                pass
        if self.pwd == recv_cmd :        
            return True
        else:
            return False    
    '''
        用于从串口检查设备 访客网络ssid 是否和传入的一致
        send "cfm get wl2g.ssid1.*"
        send "cfm get wl5g.ssid1.*"
        band:2g
        band:5g
        ssid:12345678
    '''
    @catch_exception
    def check_guest_ssid(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('ssid') :
            self.ssid = kargs['ssid']
        else:
            self.ssid = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wl2g.ssid1.* |grep "wl2g.ssid1.ssid"'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wl5g.ssid1.* |grep "wl5g.ssid1.ssid"'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('wl2g.ssid1.ssid=')[1]
                    recv_cmd = recv_cmd.split('wl2g.ssid1.ssid_encode=utf-8')[0]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('wl5g.ssid1.ssid=')[1]
                    recv_cmd = recv_cmd.split('wl5g.ssid1.ssid_encode=utf-8')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.ssid == recv_cmd :
                    return True
            except Exception,e:
                pass
        else:
            return False    
    '''
        用于从串口检查设备 访客网络pwd 是否和传入的一致
        send "cat var/run/wlan1_ssid_sync.sh "
        send "cat var/run/wlan0_ssid_sync.sh "
        band:2g
        band:5g
        pwd:12345678
    '''
    @catch_exception
    def check_guest_pwd(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('pwd') :
            pwd = kargs['pwd']
        else:
            pwd = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wl2g.ssid1.* |grep "wl2g.ssid1.wpapsk_psk"'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wl5g.ssid1.* |grep "wl5g.ssid1.wpapsk_psk"'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('wl2g.ssid1.wpapsk_psk=')[1]
                    recv_cmd = recv_cmd.split('wl2g.ssid1.wpapsk_type=')[0]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('wl5g.ssid1.wpapsk_psk=')[1]
                    recv_cmd = recv_cmd.split('wl5g.ssid1.wpapsk_type=')[0]
                recv_cmd = recv_cmd.split('\r\n')
                if pwd == recv_cmd[0] :
                    break
            except Exception,e:
                pass
        if pwd == recv_cmd[0] :
            return True
        else:
            return False
    '''
        检查设备频宽
        cmd = ''
        result = ''
        expe = ''
    '''
    @catch_exception
    def check_channel(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('cmd'):
            cmd = kargs['cmd']
        else:
            cmd =''
        if kargs.has_key('result'):
            result = kargs['result']
        else:
            result =''
        if kargs.has_key('expe') :
            expe = kargs['expe']
        else:
            expe = 'pass'
        print "555"
        for i in range(8):
            self.send_cmd('%s'%cmd)
            text_line = self.recv_cmd()
            try:
                if result in text_line:
                    flag = True
                    break
            except:
                pass
        if expe == 'pass':
            flags = False
        else:
            flags = True
        print (flag,flags)
        if flag^flags:
            return True
        else:
            return False    
    '''
        用于从串口检查设备 默认路由是否与传入的一致        
        send "route | grep 'default'"
        route:"192.168.5.1"
    '''
    @catch_exception
    def check_default_route(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('route') :
            self.route = kargs['route']
        else:
            self.route = ''        
        cmd = 'route | grep "default"'
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                recv_cmd = recv_cmd.split('default ')[1]
                recv_cmd = recv_cmd.split('0.0.0.0')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.route == recv_cmd :
                    break
            except Exception,e:
                pass
        if self.route == recv_cmd :
            return True
        else:
            return False
    '''
        用于从串口检查设备 mesh ID 和 密钥 的长度        
        send "cat /proc/mesh/status | grep 'Mesh ID'"
        send "cat /proc/mesh/status | grep 'psk key'"
        len:"16"
        mode:"id" or mode:"key"
    '''
    @catch_exception
    def check_mesh_info(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('len') :
            self.len = kargs['len']
        else:
            self.len = ''        
        if kargs.has_key('mode') :
            self.mode = kargs['mode']
        else:
            self.mode = ''
        cmd ="cat /proc/mesh/status"
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            self.waitTime(1)
            try:
                if kargs['mode']=='id':
                    recv_cmd = self.recv_cmd()
                    recv_cmd = recv_cmd.split('Mesh ID: ')[1]
                    recv_cmd = recv_cmd.split('Local')[0]
                    recv_cmd = recv_cmd.strip()
                    print "recv_cmd= ",recv_cmd
                    lens = len(recv_cmd)
                    if int(self.len) == lens:
                        return True
                elif kargs['mode']=='key':
                    recv_cmd = self.recv_cmd()
                    recv_cmd = recv_cmd.split('Mesh psk key: ')[1]
                    recv_cmd = recv_cmd.split('Local')[0]
                    recv_cmd = recv_cmd.strip()
                    print "recv_cmd= ",recv_cmd
                    lens = len(recv_cmd)
                    if int(self.len) == lens:
                        return True  
            except Exception,e:
                pass
        return False   
    '''
       查看设备某个进程是否开启
        ps = 'dhcpd'
        ps = 'dhcpcd_lan'
        expe = 'pass'or 'fail'
    '''
    @catch_exception
    def check_ps(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('ps') :
            self.ps = kargs['ps']
        else:
            self.ps = ''        
        if kargs.has_key('expe') :
            self.expe = kargs['expe'] 
        else:
            self.expe = 'pass'            
        cmd = "ps ax | grep '%s' | grep -v grep"%self.ps
        for j in range(5):
            try:
                self.send_cmd(cmd)
                #等待时间非常重要
                recv_cmd = self.recv_cmd()
                recv_cmd=recv_cmd.split('\n')
                print "recv_cmd =",recv_cmd
                for i in recv_cmd:
                    if self.ps in i and 'grep -v grep' not in i:
                        flag = True
                        print "i==============%s"%i
                        break
                if flag == True:
                    break
            except Exception,e:
                pass
        if self.expe =='pass':
            flags = False
        else:
            flags = True
        if flags^flag:
            return True
        else:
            return False
    #phonenum = ''
    #expe = 'pass'
    @catch_exception
    def check_bind(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            try:
                self.send_cmd('cfm get sys.man*')
                role = self.recv_cmd()
                print "role",role
                if kargs.has_key('phonenum'):
                    if kargs['phonenum'] in role:
                        flag = True
                        break
            except Exception,e:
                pass
        if flag and self.expe=='pass':
            return True        
        elif not flag and self.expe =='fail':
            return True
        else:
            return False
    # 获取正常功率
    @catch_exception
    def get_power_norm(self,kargs = '{}'):
        init_lst =  {'target':'','HT MCS 1SS':'23','HT MCS 2SS':'23','VHT MCS 1SS':'22','VHT MCS 2SS':'22','OFDM':'23','CCK':'26','HT1S':'22.5','HT2S':'22','cmd':'','filename':'power.ini'}
        kargs = self.init_args(kargs,**init_lst)
        kargs = eval(kargs)
        
        
        if kargs['target'] == '5g':
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan0 reg_dump'
            self.get_power_5g(kargs)
        elif kargs['target'] == '2.4g':
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan1 reg_dump'
            self.get_power_2g(kargs)
        elif kargs['target'] == '':
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan0 reg_dump'
                self.get_power_5g(kargs)
                kargs['cmd'] == 'iwpriv wlan1 reg_dump'
                self.get_power_2g(kargs)
            else:
                print "请输入target参数！！！"
                return False
            
        return True
        
    def save_inidata(self,filename,dictdata):
        init_pow1 = ParserCfg(filename)
        cf = ConfigParser.ConfigParser()
        for key, value in init_pow1.iteritems():
            cf.add_section(key)
            for k, v in value.iteritems():
                # print k,v
                if dictdata.has_key(key):
                    if dictdata[key].has_key(k):
                        cf.set(key, k, dictdata[key][k])
                        continue
                cf.set(key, k, v)
        with open(filename.replace("\\", "/"), "w+") as f:
            cf.write(f)
            
            # 提取power index
    
    def pow_indx_5g(self,target, text_line):
        # 提取 通过串口（iwpriv wlan0 reg_dump）读取到的各速率power index
        regex = r'%s.*' % target
        matchs = re.findall(regex, text_line)
        pow_indx = [[] for _ in range(len(matchs))]
        for m in range(len(matchs)):
            pow_ind = matchs[m].split(':')[1].strip()
            pow_ind = pow_ind.split(',')
            pow_ind = list(filter(None, pow_ind))
            for pow_i in range(len(pow_ind)):
                pow_ind[pow_i] = eval('0x' + pow_ind[pow_i])  # 16进制转10进制
            pow_indx[m] = pow_ind
        return pow_indx
        
    @catch_exception
    def get_power_5g(self,kargs = '{}'):
        init_lst =  {'OFDM':'24','HT MCS 1SS':'23','HT MCS 2SS':'23','VHT MCS 1SS':'22','VHT MCS 2SS':'22','cmd':'iwpriv wlan0 reg_dump','filename':''}
        kargs = self.init_args(kargs,**init_lst)
        max_tgpwr = [float(kargs['OFDM']),float(kargs['HT MCS 1SS']),float(kargs['HT MCS 2SS']),float(kargs['VHT MCS 1SS']),float(kargs['VHT MCS 2SS'])]
        cmd = kargs['cmd']
        self.waitTime(1)
        self.send_cmd('%s'%cmd)
        text_line = self.recv_cmd()
        print "text_line",text_line
        
        # 各模式速率名称
        ant_name = ['A_5G', 'B_5G']
        mode_name = ['OFDM', 'HT MCS 1SS', 'HT MCS 2SS', 'VHT MCS 1SS', 'VHT MCS 2SS']
        mode11a_name = ['11a_6m', '11a_9m', '11a_12m', '11a_18m', '11a_24m', '11a_36m', '11a_48m', '11a_54m']
        mode11n_name = ['11n_mcs0', '11n_mcs1', '11n_mcs2', '11n_mcs3', '11n_mcs4', '11n_mcs5', '11n_mcs6', '11n_mcs7']
        mode11n_name_2 = ['11n_mcs8', '11n_mcs9', '11n_mcs10', '11n_mcs11', '11n_mcs12', '11n_mcs13', '11n_mcs14', '11n_mcs15']
        mode801s_name = ['80m1s_mcs0', '80m1s_mcs1', '80m1s_mcs2', '80m1s_mcs3', '80m1s_mcs4', '80m1s_mcs5', '80m1s_mcs6',
                         '80m1s_mcs7', '80m1s_mcs8', '80m1s_mcs9']
        mode802s_name = ['80m2s_mcs0', '80m2s_mcs1', '80m2s_mcs2', '80m2s_mcs3', '80m2s_mcs4', '80m2s_mcs5', '80m2s_mcs6',
                         '80m2s_mcs7', '80m2s_mcs8', '80m2s_mcs9']
        mode_names = ['mode11a_name', 'mode11n_name', 'mode11n_name_2', 'mode801s_name', 'mode802s_name']
        path = os.path.dirname(os.path.realpath(__file__)).decode('gbk')
        tmpdir = os.path.join(path,"WEB\\tmp")
        filename = os.path.join(tmpdir,kargs['filename'])

            
        # PIs = [[] for _ in range(5)]
        # PIs[0] = pow_indx_ext('OFDM', text_line)
        # PIs[1] = pow_indx_ext('HT MCS 1SS', text_line)
        # PIs[2] = pow_indx_ext('HT MCS 2SS', text_line)
        # PIs[3] = pow_indx_ext('VHT MCS 1SS', text_line)
        # PIs[4] = pow_indx_ext('VHT MCS 2SS', text_line)
        PIs = [[] for _ in range(len(mode_name))]
        pow_index = [[] for _ in range(len(mode_name))]
        for mod_i in range(len(mode_name)):
            PIs[mod_i] = self.pow_indx_5g(mode_name[mod_i], text_line)
        
        # init_pow = ParserCfg('powerCE.ini')
        # 将得到的变量存储
        init_pow = {}
        init_pow['A_5G'] = {}
        init_pow['B_5G'] = {}
        PIs_i = 0
        try:
            for PIs_i in range(len(PIs)):
                pow_ind = PIs[PIs_i]
                mode_name = eval(mode_names[PIs_i])
                # 根据Power Index和最大速率的target power计算Target Power/dbm
                tp_dbm = [[] for _ in range(len(pow_ind))]
                for i in range(len(pow_ind)):
                    tp_dbm[i] = [max_tgpwr[PIs_i] + (pi - pow_ind[i][-1]) * 0.5 for pi in pow_ind[i]]  # 6M,9M,12M,18M,24M,36M,48M,54M
                # 将计算出的Power Index和Target Power/dbm保存
                for pw_i in range(len(ant_name)):
                    for na_i in range(len(mode_name)):
                        ant = ant_name[pw_i]
                        model = mode_name[na_i]
                        # print ant,model,pow_ind[pw_i][na_i],tp_dbm[pw_i][na_i]
                        init_pow[ant][model] = str(pow_ind[pw_i][na_i]) + ' ' + str(tp_dbm[pw_i][na_i])
        except:
            pass
        self.save_inidata(filename,init_pow)
        return init_pow,PIs
   # 提取power index
    def pow_indx_2g(self,target, text_line):
        regex = r'%s.*'%target
        matchs = re.findall(regex, text_line)
        pow_indx = [[] for i in range(len(matchs))]
        for m in range(len(matchs)):
            pow_ind = matchs[m].split(':')[1].strip()
            pow_ind = pow_ind.split(',')
            pow_ind = list(filter(None, pow_ind))
            for pow_i in range(len(pow_ind)):
                pow_inde = [[] for i in range(int(len(pow_ind[0]) / 2) - 1)]
                for i in range(int(len(pow_ind[0]) / 2) - 1):
                    pow_inde[i] = pow_ind[pow_i][2*i+2 : 2*i+4]
                    pow_inde[i] = eval('0x' + pow_inde[i])  # 16进制转10进制
            pow_indx[m] = pow_inde
        return pow_indx
        
    @catch_exception
    def get_power_2g(self,kargs = '{}'):
        init_lst =  {'OFDM':'23','CCK':'26','HT1S':'22.5','HT2S':'22','cmd':'iwpriv wlan1 reg_dump','filename':''}
        kargs = self.init_args(kargs,**init_lst)
        max_tgpwr = [float(kargs['OFDM']),float(kargs['CCK']),float(kargs['HT1S']),float(kargs['HT2S'])]
        
        cmd = kargs['cmd']
        self.waitTime(1)
        self.send_cmd('%s'%cmd)
        text_line = self.recv_cmd()
        print "text_line",text_line
        
        ant_name = ['A_2G', 'B_2G']
        mode_name = ['A_CCK1_Mcs32', 'B_CCK5_1_Mcs32', 'A_CCK11_2_B_CCK11', 'A_Rate18_06', 'A_Rate54_24', 'A_Mcs03_Mcs00', 'A_Mcs07_Mcs04', 'A_Mcs11_Mcs08', 'A_Mcs15_Mcs12', 'B_Rate18_06', 'B_Rate54_24', 'B_Mcs03_Mcs00', 'B_Mcs07_Mcs04', 'B_Mcs11_Mcs08', 'B_Mcs15_Mcs12']
        mode11b_name = ['11b_1m','11b_2m','11b_5.5m','11b_11m']
        mode11g_name = ['11g_6m','11g_9m','11g_12m','11g_18m','11g_24m','11g_36m','11g_48m','11g_54m']
        mode11n_name = ['11n_mcs0','11n_mcs1','11n_mcs2','11n_mcs3','11n_mcs4','11n_mcs5','11n_mcs6','11n_mcs7']
        mode11n_name_2 = ['11n_mcs8','11n_mcs9','11n_mcs10','11n_mcs11','11n_mcs12','11n_mcs13','11n_mcs14','11n_mcs15']
        mode_names = ['mode11b_name', 'mode11g_name', 'mode11n_name']
        path = os.path.dirname(os.path.realpath(__file__)).decode('gbk')
        tmpdir = os.path.join(path,"WEB\\tmp")
        filename = os.path.join(tmpdir,kargs['filename'])
        print "filename",filename
        
        PIsall = [[] for _ in range(len(mode_name))]
        for mod_i in range(len(mode_name)):
            PIsall[mod_i] = self.pow_indx_2g(mode_name[mod_i], text_line)
        
        # mat_ind = [[0,2,2,2],
        # #            [1,1,1,2]]
        # 索引值，通过索引值来提取各速率的Power Index
        # ind_11b[0]表示A天线索引值；ind_11b[0][0]对应PIs，ind_11b[0][1]对应PIs[i]的第几个值
        # ind_11b[1]表示B天线索引值
        ind_11b = [[[0,2,2,2],[2,2,1,0]],
                   [[1,1,1,2],[2,1,0,3]]]
        ind_11g = [[[3,3,3,3,4,4,4,4],[3,2,1,0,3,2,1,0]],
                   [[9,9,9,9,10,10,10,10],[3,2,1,0,3,2,1,0]]]
        ind_11n = [[[5,5,5,5,6,6,6,6],[3,2,1,0,3,2,1,0]],[[11,11,11,11,12,12,12,12],[3,2,1,0,3,2,1,0]]]
        ind_11n_2 = [[[7,7,7,7,8,8,8,8],[3,2,1,0,3,2,1,0]],[[13,13,13,13,14,14,14,14],[3,2,1,0,3,2,1,0]]]
        ind_mode_name = ['ind_11b','ind_11g','ind_11n','ind_11n_2']
        ConfigFile = 'powerCE.ini'
        # init_pow = ParserCfg('powerCE.ini')
        # 将得到的变量存储
        init_pow = {}
        init_pow['A_2G'] = {}
        init_pow['B_2G'] = {}
        PIs_i = 0
        PIs = [[] for _ in range(len(ind_mode_name))]
        try:
        
            for mod_i in range(len(ind_mode_name)):
                mode_name = eval(mode_names[mod_i])
                ind_mode = eval(ind_mode_name[mod_i])
                # 根据索引提取Power Index,得到每种mode下的Power Index
                PIs1 = [[] for _ in range(len(ant_name))]
                for pw_i in range(len(ant_name)):
                    PIs1_1 = [[] for _ in range(len(mode_name))]
                    for na_i in range(len(mode_name)):
                        ind1 = ind_mode[pw_i][0][na_i]
                        ind2 = ind_mode[pw_i][1][na_i]
                        PIs1_1[na_i] = PIsall[ind1][0][ind2]
                    PIs1[pw_i] = PIs1_1
                PIs[mod_i] = PIs1
                # 根据Power Index和最大速率的target power计算Target Power/dbm
                tp_dbm = PIs
                for i in range(len(PIs[mod_i])):
                    tp_dbm[mod_i][i] = [max_tgpwr[mod_i] + (pi - PIs[mod_i][i][-1]) * 0.5 for pi in PIs[mod_i][i]]  # 6M,9M,12M,18M,24M,36M,48M,54M
                # 将计算出的Power Index和Target Power/dbm保存
                for pw_i in range(len(ant_name)):
                    for na_i in range(len(mode_name)):
                        ant = ant_name[pw_i]
                        model = mode_name[na_i]
                        # print ant,model,pow_ind[pw_i][na_i],tp_dbm[pw_i][na_i]
                        init_pow[ant][model] = str(PIs[mod_i][pw_i][na_i]) + ' ' + str(tp_dbm[mod_i][pw_i][na_i])
        except:
            pass
        print "6666666666666666666666"
        self.save_inidata(filename,init_pow)
        return init_pow,PIsall
    def get_cepower(self,kargs = '{}'):
        init_lst =  {'target':'','HT MCS 1SS':'23','HT MCS 2SS':'23','VHT MCS 1SS':'22','VHT MCS 2SS':'22','OFDM':'23','CCK':'26','HT1S':'22.5','HT2S':'22','cmd':'','filename':'powerCE.ini'}
        kargs = self.init_args(kargs,**init_lst)
        # kargs = eval(kargs)
        
        #2.4G
        mode11b_name = ['11b_1m','11b_2m','11b_5.5m','11b_11m']
        mode11g_name = ['11g_6m','11g_9m','11g_12m','11g_18m','11g_24m','11g_36m','11g_48m','11g_54m']
        mode11n_name = ['11n_mcs0','11n_mcs1','11n_mcs2','11n_mcs3','11n_mcs4','11n_mcs5','11n_mcs6','11n_mcs7']
        mode11n_name_2 = ['11n_mcs8','11n_mcs9','11n_mcs10','11n_mcs11','11n_mcs12','11n_mcs13','11n_mcs14','11n_mcs15']
        # mode11_name = mode11b_name+mode11g_name+mode11n_name+mode11n_name_2
        
        
        # 5G
        mode11a_name = ['11a_6m', '11a_9m', '11a_12m', '11a_18m', '11a_24m', '11a_36m', '11a_48m', '11a_54m']
        # mode11n_name = ['11n_mcs0', '11n_mcs1', '11n_mcs2', '11n_mcs3', '11n_mcs4', '11n_mcs5', '11n_mcs6', '11n_mcs7']
        # mode11n_name_2 = ['11n_mcs8', '11n_mcs9', '11n_mcs10', '11n_mcs11', '11n_mcs12', '11n_mcs13', '11n_mcs14', '11n_mcs15']
        mode801s_name = ['80m1s_mcs0', '80m1s_mcs1', '80m1s_mcs2', '80m1s_mcs3', '80m1s_mcs4', '80m1s_mcs5', '80m1s_mcs6',
                         '80m1s_mcs7', '80m1s_mcs8', '80m1s_mcs9']
        mode802s_name = ['80m2s_mcs0', '80m2s_mcs1', '80m2s_mcs2', '80m2s_mcs3', '80m2s_mcs4', '80m2s_mcs5', '80m2s_mcs6',
                         '80m2s_mcs7', '80m2s_mcs8', '80m2s_mcs9']
        mode11_name = mode11b_name+mode11g_name+mode11n_name+mode11n_name_2+mode11a_name+mode801s_name+mode802s_name
        
        ant_name = ['A_2G', 'B_2G','A_5G', 'B_5G']
        thres_ce = [10,10,12,12]
        if kargs['target'] == '2.4g':
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan1 reg_dump'
            self.get_power_2g(kargs)
        elif kargs['target'] == '5g':
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan0 reg_dump'
            self.get_power_5g(kargs)
        else:
            if kargs['cmd']=='':
                kargs['cmd'] == 'iwpriv wlan0 reg_dump'
                self.get_power_5g(kargs)
                kargs['cmd'] == 'iwpriv wlan1 reg_dump'
                self.get_power_2g(kargs)
            else:
                print "请输入正确的target参数！！！"
                return False
        #获取CE功率下的taeget index
        # get_power_2g(str({'OFDM':'23','CCK':'26','HT1S':'22.5','HT2S':'22','cmd':'iwpriv wlan1 reg_dump','filename':'powerCE.ini'}))
        path = os.path.dirname(os.path.realpath(__file__)).decode('gbk')
        tmpdir = os.path.join(path,"WEB\\tmp")
        filename = os.path.join(tmpdir,kargs['filename'])
        pi_ce = ParserCfg(filename)
        filename2 = os.path.join(tmpdir,'power.ini')
        pi = ParserCfg(filename2)
        ant_i = 0
        flag = [[] for _ in range(len(ant_name))]
        try:
            for ant_i in range(len(ant_name)):
                for mod_i in range(len(mode11_name)):
                    modname = mode11_name[mod_i]
                    ant = ant_name[ant_i]
                    pitp = pi[ant][modname].split(" ")
                    pitp_ce = pi_ce[ant][modname].split(" ")
                    pitp = map(eval, pitp)
                    pitp_ce = map(eval, pitp_ce)                    
                    pow_ce = pitp[1]-(pitp[0] - pitp_ce[0])*0.5
                    pi_ce[ant][modname] = str(pitp_ce[0]) + ' ' + str(pow_ce)
                    
                    if pow_ce <= thres_ce[ant_i]:
                        flag = flag + 1
        except:
            pass
        # print "pi_ce",pi_ce
        self.save_inidata(filename,pi_ce)
        if kargs['target'] == '2.4g':
            if flag == 28*2:
                return True
            else:
                return False
        if kargs['target'] == '5g':
            if flag == 44*2:
                return True
            else:
                return False                
        if kargs['target'] == '':        
            if flag == 28*2+44*2:
                return True
            else:
                return False
        
    # 检查目标功率
    @catch_exception
    def check_power(self,kargs,power_index):
        init_lst =  {'target':'','ce':'','cmd':'','expe':''}
        kargs = self.init_args(kargs,**init_lst)
        # kargs = eval(kargs)
        self.send_cmd('%s'%kargs['cmd'])
        text_line = self.recv_cmd()
        print "text_line",text_line
        # 提取power index
        
        if kargs['target'] == '5g':
            mode_name = ['OFDM','HT MCS 1SS','HT MCS 2SS','VHT MCS 1SS','VHT MCS 2SS']
            PIsall = [[] for _ in range(len(mode_name))]
            for mod_i in range(len(mode_name)):
                PIsall[mod_i] = self.pow_indx_5g(mode_name[mod_i], text_line)
                
        elif kargs['target'] == '2.4g':
            mode_name = ['A_CCK1_Mcs32', 'B_CCK5_1_Mcs32', 'A_CCK11_2_B_CCK11', 'A_Rate18_06', 'A_Rate54_24', 'A_Mcs03_Mcs00', 'A_Mcs07_Mcs04', 'A_Mcs11_Mcs08', 'A_Mcs15_Mcs12', 'B_Rate18_06', 'B_Rate54_24', 'B_Mcs03_Mcs00', 'B_Mcs07_Mcs04', 'B_Mcs11_Mcs08', 'B_Mcs15_Mcs12']
            PIsall = [[] for _ in range(len(mode_name))]
            for mod_i in range(len(mode_name)):
                PIsall[mod_i] = self.pow_indx_2g(mode_name[mod_i], text_line)
        for mod_i in range(len(mode_name)):
            PIs = PIsall[mod_i]
            PIs_raw = power_index[mod_i]
            print "PIs",PIs
            print "PIs_raw",PIs_raw
            for PI_i in range(len(PIs)):
                if PIs_raw[PI_i] == PIs[PI_i]:
                    flags = False
                    continue
                else:
                    print mode_name[mod_i]
                    flags = True
                    break
        
        if kargs['expe'] ^ flags:
            return True
        else:
            return False  
            
            
    #用于串口调用函数比对
    def return_func(self,value):
        return value
    def close(self):
        self.sk.close()
        # print "close  suc!" 
        return True
    #串口查看设备位置名称
    @catch_exception
    def check_localtion(self,localtion='node.location',expe='pass'):
        flag = False
        for _ in range(5):
            self.send_cmd("cfm get location*")
            text_line = self.recv_cmd()
            try:
                print '111111111'
                print text_line
                print '222222222'
                if re.search(localtion,text_line):
                    print "333333"
                    flag = True
                    break
            except:
                print text_line
        #以下代码正确
        print "flag ",flag
        if expe == 'pass' :
            flag1=False
        else:
            flag1=True
        print "flag1",flag1
        if flag^flag1:
            return True
        else:
            return False
    #串口查看高待机模式是否开启
    @catch_exception
    def check_high_devices(self,state='',expe='pass'):
        flag = False
        for _ in range(5):
            self.send_cmd("cfm get high*")
            text_line = self.recv_cmd()
            if state =='ON':
                state1 = 'highdevice_en=1'
            else:
                state1 = 'highdevice_en=0'
            try:
                print 'state',state
                print text_line
                if re.search(state1,text_line):
                    return True
            except:
                print text_line
        return False
class ks_MW12(ks):
    def __init__(self,**kargs):
        print 'kargs=',kargs
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs.has_key('iface'):
            self.expe = kargs['iface']
        else:
            self.expe = 'br0'
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        else:
            # self.expe =G_MainDict['dut']['dip']             
            self.expe = '192.168.5.1'             
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'            
        if kargs.has_key('passwd'):
            self.passwd=b64encode(kargs['passwd'])
        else:
            self.passwd = ''
        try:
            self.mpp_passwd=b64encode(G_MainDict["dut"]["wifi_password"])
        except:
            pass
        try:
            self.map1_passwd=b64encode(G_MainDict["map1"]["wifi_pwd"])
        except:
            pass
        try:
            self.map2_passwd=b64encode(G_MainDict["map2"]["wifi_pwd"])
        except:
            pass
        if kargs.has_key('PORT'):
            self.PORT=kargs['PORT']
            self.PORT=int(self.PORT)
            print "PORT=",self.PORT
        else:
            self.PORT = 12345   
        ip_port = ('127.0.0.1',self.PORT)
        self.ip_port = ip_port
        try:
            self.socket_connect()
        except Exception,e:
            print "not open socket"
        print "-------connect success-------"
        if self.login():
            print 'login success'
        print "_________"
        self.close()
        if kargs.has_key('waitflag'):
            flags = kargs['waitflag']
        else:
            flags = True
        if kargs.has_key('reset'):
            if kargs['reset'] == 'yes':
                self.reset(flag=flags)
    '''     
        检查设备频宽
        cmd = ''
        result = ''
        expe = ''
    '''
    @catch_exception
    def check_channel(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('cmd'):
            cmd = kargs['cmd']
        else:
            cmd =''
        if kargs.has_key('result'):
            result = kargs['result']
        else:
            result =''
        if kargs.has_key('expe') :
            expe = kargs['expe']
        else:
            expe = 'pass'
        print "555"
        for i in range(8):
            self.send_cmd('%s'%cmd)
            text_line = self.recv_cmd()
            try:
                if result in text_line:
                    flag = True
                    break
            except:
                pass
        if expe == 'pass':
            flags = False
        else:
            flags = True
        print (flag,flags)
        if flag^flags:
            return True
        else:
            return False    
    #language  =en
    @catch_exception
    def check_language(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('language'):
            result = kargs['language']
        for i in range(8):
            self.send_cmd('cfm get sys.app.lang*')
            text_line = self.recv_cmd()
            try:
                if result in text_line:
                    return True
            except:
                pass
        return False
                
        # self.reset()
    '''
        用于返回串口打印
    '''  
        
    @catch_exception
    def check_sn(self,sn=''):
        flag = False
        for i in range(5):
            self.send_cmd('cfm get serial.number') 
            # self.send_cmd('ifconfig')
            text_line = self.recv_cmd()
            print text_line
            try:
                if sn in text_line:
                    flag = True
                    break
            except:
                pass
        if flag :
            return True
        else:
            return False
    #查看设备某个进程是否开启
    # @catch_exception
    # def check_ps(self,ps='',expe='pass'):
        # flag = False
        # for _ in range(5):
            # self.send_cmd("ps ax | grep %s | grep -v grep"%(ps))
            # text_line = self.recv_cmd()
            # try:
                # print text_line
                # rets = "root"
                # if re.search(rets,text_line):
                    # return True
            # except:
                # print text_line
        # return False
    def check_write_flash(self,con,recv):
        print "--------------------------------------"
        print con
        print recv
        print "--------------------------------------"
       
        if recv:
            if re.search(con,recv):
                return True
            else:
                return False 
        else:
            return False            
    '''
       检查当前设备的角色
       role=1固定MPP
       role=3临时MPP
       role=4为MAP
       send "cfm get sys.role "
    '''
    @catch_exception
    def check_role(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('role') :
            self.role = kargs['role']
        else:
            self.role = ''
        for i in range(5):
            self.send_cmd('cfm get sys.role')
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                role = self.recv_cmd()
                role = role.split('cfm get sys.role')[1]
                role = role.split('~ #')[0]
                role = role.strip()
                print "role =",role
                if int(role) == int(self.role):
                    break
            except Exception,e:
                pass
        if int(role) == int(self.role):
            return True        
        else:
            return False  
    #dns1 = ''
    #dns2 = ''
    #expe = 'pass'
    @catch_exception
    def check_dns(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('expe') :
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        for i in range(5):
            try:
                self.send_cmd('ps | grep dnrd')
                role = self.recv_cmd()
                print "role",role
                if kargs.has_key('dns1') and kargs.has_key('dns2'):
                    if kargs['dns1'] in role and kargs['dns2'] in role:
                        flag = True
                        break
                elif kargs.has_key('dns1'):
                    print "role",role
                    if kargs['dns1'] in role :
                        flag = True
                        break
                else:
                    if kargs['dns2'] in role :
                        flag = True
                        break
            except Exception,e:
                pass
        if flag and self.expe=='pass':
            return True        
        elif not flag and self.expe =='fail':
            return True
        else:
            return False
            
            
    '''
        三频串口命令改动，重写check_main_ssid方法
        用于从串口检查设备 主网络ssid 是否和传入的一致
        
        send "cfm get wlan1.0_bss_ssid" 
        send "cfm get wlan2.0_bss_ssid" 
        band:5g
        band:2g
        ssid:12345678
    '''
    @catch_exception
    def check_main_ssid(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('ssid') :
            self.ssid = kargs['ssid']
        else:
            self.ssid = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wlan2.0_bss_ssid'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wlan1.0_bss_ssid'
        else:
            return False
        for i in range(5):
            try:
                self.send_cmd(cmd)
                #等待时间非常重要
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('cfm get wlan2.0_bss_ssid')[1]
                else :
                    recv_cmd = recv_cmd.split('cfm get wlan1.0_bss_ssid')[1]
                recv_cmd = recv_cmd.split('~ #')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.ssid == recv_cmd :
                    break
            except Exception,e:
                pass
        if self.ssid == recv_cmd:
            return True        
        else:
            return False    
    '''
        三频串口命令改动，重写check_main_pwd方法
        用于从串口检查设备 主网络pwd 是否和传入的一致
        send "cfm get wlan2.0_bss_wpapsk_key"
        send "cfm get wlan1.0_bss_wpapsk_key"
        band:2g
        band:5g
        pwd:12345678
    '''
    @catch_exception
    def check_main_pwd(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('pwd') :
            self.pwd = kargs['pwd']
        else:
            self.pwd = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wlan2.0_bss_wpapsk_key'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wlan1.0_bss_wpapsk_key'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('cfm get wlan2.0_bss_wpapsk_key')[1]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('cfm get wlan1.0_bss_wpapsk_key')[1]
                print "recv_cmd =",recv_cmd
                recv_cmd = recv_cmd.split('~ #')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.pwd == recv_cmd :
                    break
            except Exception,e:
                pass
        if self.pwd == recv_cmd :        
            return True
        else:
            return False    
    '''
        三频串口命令改动，重写check_guest_ssid方法
        用于从串口检查设备 访客网络ssid 是否和传入的一致
        send "cfm get wlan2.1_bss_ssid"
        send "cfm get wlan1.1_bss_ssid"
        band:2g
        band:5g
        ssid:12345678
    '''
    @catch_exception
    def check_guest_ssid(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('ssid') :
            self.ssid = kargs['ssid']
        else:
            self.ssid = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wlan2.1_bss_ssid'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wlan1.1_bss_ssid'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('cfm get wlan2.1_bss_ssid')[1]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('cfm get wlan1.1_bss_ssid')[1]
                recv_cmd = recv_cmd.split('~ #')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if self.ssid == recv_cmd :
                    return True
            except Exception,e:
                pass
        else:
            return False    
    '''
        三频串口命令改动，重写check_guest_pwd方法
        用于从串口检查设备 访客网络pwd 是否和传入的一致
        send "cfm get wlan2.1_bss_wpapsk_key"
        send "cfm get wlan1.1_bss_wpapsk_key"
        band:2g
        band:5g
        pwd:12345678
    '''
    @catch_exception
    def check_guest_pwd(self,kargs = '{}'):
        kargs = eval(kargs)
        if kargs.has_key('pwd') :
            pwd = kargs['pwd']
        else:
            pwd = ''     
        if kargs.has_key('band') :
            if kargs['band'] == '2g':
                cmd = 'cfm get wlan2.1_bss_wpapsk_key'
            elif kargs['band'] == '5g':
                cmd = 'cfm get wlan1.1_bss_wpapsk_key'
        else:
            return False
        for i in range(5):
            self.send_cmd(cmd)
            #等待时间非常重要
            # self.waitTime(1.5)
            try:
                recv_cmd = self.recv_cmd()
                if kargs['band'] == '2g':
                    recv_cmd = recv_cmd.split('cfm get wlan2.1_bss_wpapsk_key')[1]
                elif kargs['band'] == '5g':
                    recv_cmd = recv_cmd.split('cfm get wlan1.1_bss_wpapsk_key')[1]
                recv_cmd = recv_cmd.split('~ #')[0]
                recv_cmd = recv_cmd.strip()
                print "recv_cmd =",recv_cmd
                if pwd == recv_cmd:
                    break
            except Exception,e:
                pass
        if pwd == recv_cmd:
            return True
        else:
            return False
            
    '''
        检查LAN、WAN口连接速率 consult
        port （Port0，Port1，Port2，Port3，Port4）
        speed (1G 100M 10M)
        mode  (Eabled Disabled) 这里Eabled指的是Eabled Duplex 使用全双工模式 
              1G速率只有全双工模式 
              Mesh只能自协商 设置上级的双工模式为非自协商时100M
              100M速率只能协商出半双工的工作模式 ，无法匹配出100M的全双工
              所以1G速率 肯定是双工模式 Eabled Duplex
              100M速率 只有是半双工模式 Disabled Duplex
    '''
    @catch_exception
    def check_link_speed(self,kargs = '{}'):
        kargs = eval(kargs)
        flag = False
        if kargs.has_key('port'):
            self.port = kargs['port']
        else:
            self.port = ''
        if kargs.has_key('speed'):
            self.speed = kargs['speed']
        else:
            self.speed = ''
        if kargs.has_key('mode') :
            self.mode = kargs['mode']
        else:
            self.mode = ''
        for i in range(5):
            try:
                port = "'Port\[" + self.port + "\]'"
                self.send_cmd('test_lib_drv | grep %s'%port)               
                text_line = self.recv_cmd()
                print "text_line",text_line                          
                speed = text_line.split('Port[' + self.port + ']')[1]
                speed = speed.split('speed:')[1]
                speed = speed.split(' ')[0]                
                print "speed =",speed
                mode  = text_line.split('duplex:')[1]
                mode  = mode.split(' ')[0]
                print "mode =",mode
                if speed == self.speed:
                    flag = True
                    break 
            except Exception,e:
                print "false",e
                pass
        if mode == self.mode:
            flags = False
        else:
            flags = True
        print (flag,flags)
        if flag^flags:
            return True
        else:
            return False    
class ks_SP3(ks):
    def __init__(self,**kargs):
        print 'kargs=',kargs
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs.has_key('iface'):
            self.expe = kargs['iface']
        else:
            self.expe = 'br0'
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        else:
            # self.expe =G_MainDict['dut']['dip']             
            self.expe = '192.168.5.1'             
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'            
        if kargs.has_key('baudrate'):
            self.baudrate=kargs['baudrate']
        else:
            self.baudrate=115200
        if kargs.has_key('port'):
            self.port=kargs['port']
        else:
            self.port = 'COM1'
        if kargs.has_key('PORT'):
            self.PORT=kargs['PORT']
            self.PORT=int(self.PORT)
            print "PORT=",self.PORT
        else:
            self.PORT = 12345   
        ip_port = ('127.0.0.1',self.PORT)
        self.ip_port = ip_port
        try:
            self.socket_connect()
        except Exception,e:
            print "not open socket"
        # print "-------connect success-------"
        # self.reset()
        # print "____reset_____"
        self.close()
    def reboot(self):
        self.send_cmd("reboot")
        # text = self.recv_cmd()
        self.close()
        self.socket_connect()
        for i in range(0,10):
            print "i=%d/10" %(i)
            self.waitTime(1)
        return True
    """
        用于恢复出厂设置
    """
    @catch_exception
    def reset(self):
        self.send_cmd("ATSF")
        for i in range(0,10):
            self.waitTime(1)
            print "i=%d/10" %(i)
        self.close()
        return True
    """
        用于查看插座开关状态
        switch = 'ON' or 'OFF'
        expe = 'pass' or 'fail'
    """
    @catch_exception
    def check_switch(self,switch,expe='pass'):
        flag = False
        if expe =='pass':
            flag1 = False
        else:
            flag1=True
        for i in range(0,5):
            self.send_cmd("ATSI")
            self.waitTime(1)
            text = self.recv_cmd()
            if 'switch status: 1' in text:
                if switch=='ON':
                    flag = True
                    break
            elif 'switch status: 0' in text:
                if switch=='OFF':
                    flag = True
                    break
            
        if flag1^flag:
            return True
        else:
            return False
    """
        用于返回设备信息
        hard_ver: V1.0
        soft_ver:V1.1.0.4(91)
        model:SP3V1
        mac:00:e0:4c:81:96:ci
        sn:1234567890a8000001

    """
    @catch_exception
    def get_device_info(self,cmd):
        flag = False
        print "666"
        retdict = {}
        for i in range(0,5):
            self.send_cmd(cmd)
            # self.waitTime(1)
            ret = self.recv_cmd()
            print "ret",ret
            hard_ver = re.findall("(hard_ver.*)",ret)
            print "hard_ver",hard_ver
            soft_ver = re.findall("(soft_ver.*)",ret)
            print "soft_ver",soft_ver
            model = re.findall("(model.*)",ret)
            mac = re.findall("(mac.*)",ret)
            sn = re.findall("(SN.*)",ret)
            if hard_ver:
                retdict['hard_ver'] = hard_ver[0].strip().split(":")[-1]
                retdict['hard_ver'] = retdict['hard_ver'].strip(' ')
            if soft_ver:
                retdict['soft_ver'] = soft_ver[0].strip().split(":")[-1]
                retdict['soft_ver'] = retdict['soft_ver'].strip(' ')
            if model:
                retdict['model'] = model[0].strip().split(":")[-1]
                retdict['model'] = retdict['model'].strip(' ')
            if mac:
                retdict['mac'] = mac[0].strip().split(" ")[-1]
            if sn:
                retdict['sn'] = sn[0].strip().split(":")[-1]
                retdict['sn'] = retdict['sn'].strip(' ')
            if retdict != {}:
                print "retdict",retdict
                self.waitTime(5)
                return retdict
            else:
                continue
        return False
    def login(self):
        #循环三次进行登录判断
        return True
        
        
class ks_SP9(ks_SP3):
    def __init__(self,**kargs):
        # print 'kargs=',kargs
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs.has_key('iface'):
            self.expe = kargs['iface']
        else:
            self.expe = 'br0'
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        else:
            # self.expe =G_MainDict['dut']['dip']             
            self.expe = '192.168.5.1'             
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'            
        if kargs.has_key('baudrate'):
            self.baudrate=kargs['baudrate']
        else:
            self.baudrate=115200
        if kargs.has_key('port'):
            self.port=kargs['port']
        else:
            self.port = 'COM1'
        if kargs.has_key('PORT'):
            self.PORT=kargs['PORT']
            self.PORT=int(self.PORT)
            print "PORT=",self.PORT
        else:
            self.PORT = 12345   
        ip_port = ('127.0.0.1',self.PORT)
        self.ip_port = ip_port
        try:
            self.socket_connect()
        except Exception,e:
            print "not open socket"
        # print "-------connect success-------"
        # self.reset()
        if kargs.has_key('reset'):
            if kargs['reset'] == 'yes':
                self.reset()
        # print "____reset_____"
        self.close()
        
class ks_test(ks_SP3):
    def __init__(self,**kargs):
        print 'kargs=',kargs
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'
        if kargs.has_key('iface'):
            self.expe = kargs['iface']
        else:
            self.expe = 'br0'
        if kargs.has_key('ip'):
            self.ip = kargs['ip']
        else:
            # self.expe =G_MainDict['dut']['dip']             
            self.expe = '192.168.5.1'             
        if kargs.has_key('expe'):
            self.expe = kargs['expe']
        else:
            self.expe = 'pass'            
        if kargs.has_key('baudrate'):
            self.baudrate=kargs['baudrate']
        else:
            self.baudrate=115200
        if kargs.has_key('port'):
            self.port=kargs['port']
        else:
            self.port = 'COM1'
        if kargs.has_key('PORT'):
            self.PORT=kargs['PORT']
            self.PORT=int(self.PORT)
            print "PORT=",self.PORT
        else:
            self.PORT = 12346   
        ip_port = ('127.0.0.1',self.PORT)
        self.ip_port = ip_port
        try:
            self.socket_connect()
        except Exception,e:
            print "not open socket"
        print "-------connect success-------"
        # self.reset()
        if kargs.has_key('reset'):
            if kargs['reset'] == 'yes':
                self.reset()
        print "____reset_____"
        self.close()
        
    @catch_exception
    def login(self):
        #循环三次进行登录判断
        def revlog():
            self.waitTime(4)
            logindata=self.readfromcom()
            print "logindata",logindata
            if logindata.find("~ #") >= 0:
                print u"登录成功"
                return True
            else:
                print u"第%d次登录失败" %(i)
        for i in range(4):
            try:
                self.mpp_passwd = 'Fireitup'+'\n'
                self.send_cmd(self.mpp_passwd)
                if revlog():
                    return True
            except:
                pass
        return False
    @catch_exception
    def ping(self,kargs='{}'):
        self.login()
        init_default_dict = {"dip":"192.168.0.1","iface":"eth1","size":"64","flood":"0","flag":"0","expe":"pass","maxerr":"5","maxsuc":"5"}
        
        cfg_option_dict = {"iface":"-I ","size":"-s "}
        init_cfg_option_dict = {"iface":"-I ","size":"-s "}
        kargs = self.init_args(kargs,**init_default_dict)
        cmd = ["ping %s -c 1" %(kargs['dip'])]
        for k,v in cfg_option_dict.iteritems():
            cfg_option_dict[k] = v+kargs[k]
            if cfg_option_dict[k] != init_cfg_option_dict[k]:
                cmd.append(cfg_option_dict[k])
        if kargs['flag'] != "0":
            cmd.append(" -M do")
        if kargs['flood'] == "1":
            cmd.append("-f")
        maxerr = int(kargs['maxerr'])
        print "maxerr = ",maxerr
        maxsuc = int(kargs['maxsuc'])
        print "maxsuc = ",maxsuc
        sumnum = maxerr+maxsuc
        factsuc = 0
        facterr = 0
        result = "fail"
        self.send_cmd("ip route flush cache")
        for x in xrange(sumnum):
            ret = self.send_cmd(" ".join(cmd))
            ret = self.recv_cmd()
            print ret
            if re.search("ttl=",ret):
                factsuc = factsuc + 1
            else:
                facterr = facterr + 1
            if factsuc >= maxsuc:
                result = "pass"
                break
            elif facterr >= maxerr:
                result = "fail"
                break
            self.waitTime(1)
        print "factsuc =",factsuc
        print "facterr =",facterr
        if result == kargs["expe"]:
            return True
        else:
            return False
            
    def init_args(self,args,**kargs):
        retdict =eval(args)
        for k,v in kargs.iteritems():
            if not retdict.has_key(k):
                retdict[k] = v
        return retdict
        
class kmClass():
    def __init__(self,dip='192.168.0.1'):
        self.rootdir = r'D:\Program Files (x86)\Thunder Network\Thunder\Program'
        self.user = 'admin'
        self.pwd = 'admin'
        self.dip=dip
        self.session=requests.Session()
    def open(self,path):
        program = path.title()+'.exe'
        path = os.path.join(self.rootdir,program)
        subprocess.call([path])
        return True
    def close(self,path):
        program = path.title()+'*'
        os.system("taskkill /f /im %s" %program)
        alldata=""
        while True:
            data=os.popen('tasklist').read()
            if data:
                alldata = "".join(data)
                break
        if not re.search(path,alldata):
            return True
    def login(self):
        header = {'Host': '%s' %self.dip, 
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://%s/' %self.dip,
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cookie': 'jxtd_IP-COM_user=admin|0}'
                 }
        url = "http://%s/cgi/login?username=%s&password=%s" %(self.dip,self.user,self.pwd)
        ret = self.session.get(url,headers=header)
        if ret.status_code == 200:
            print "login successfully"
            return True
        else:
            print "login unsucessfully"
            return False
    def config_port(self,kargs=None):
        header = {'Host': '%s' %self.dip, 
                  'Connection': 'keep-alive',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400',
                  'Accept': '*/*',
                  'Referer': 'http://%s/' %self.dip,
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cookie': 'jxtd_IP-COM_user=admin|admin|guest|0|24|3'
                 }
        kargs = eval(kargs)
        auto_dict = {'auto':'0','10M/half':'1','10M/full':'2','100M/half':'3','100M/full':'4','1000M/full':'5'}
        state_dict = {'ON':'1','OFF':'0'}
        payload = {'rand': '0.18340834263774553', 
                   'opt': '1',
                   'port': '%s' %kargs['port'],
                   'autocfg': '%s' %auto_dict[kargs['autocfg']],
                   'state': '%s' %state_dict[kargs['state']],
                   'priority': '0',
                   'flowcfg': '0',
                   'broadcast': '3',
                   'isolation': '0',
                   'jumbocfg': '1518'
                   }
        port_url = "http://%s/cgi/set_port" %self.dip
        print "*********port_url=",port_url
        if self.login():
            ret = self.session.get(port_url,params=payload,headers=header)
            if ret.status_code == 200:
                self.waitTime(2)
                return True
            return False
    def osSendCmd(self,cmd):
        os.system(cmd)
        return True
    def init_args(self,args,**kargs):
        retdict =eval(args)
        for k,v in kargs.iteritems():
            if not retdict.has_key(k):
                retdict[k] = v
        return retdict
    def windows_iface_mode(self,kargs='{}'):
        init_default_dict = {"iface":"kc","mode":"static","ip":"","mask":"255.255.255.0","gateway":"","dns":""}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == 'dhcp':
            cmd = 'netsh interface ip set dns %s dhcp'%kargs['iface']
            os.system(cmd)
            cmd1 = 'netsh interface ip set address %s dhcp'%kargs['iface']
            os.system(cmd1)
        else:
            cmd = 'netsh interface ip set address %s static %s %s %s'%(kargs['iface'],kargs['ip'],kargs['mask'],kargs['gateway'])
            os.system(cmd)
            cmd1 = 'netsh interface ip set dns %s static %s'%(kargs['iface'],kargs['dns'])
            os.system(cmd1)
        return True
    def waitTime(self,num):
        for x in xrange(int(num)):
            print "%d/%d sum=%d" %(x,num,num)
            time.sleep(1)
        return True
class kmClass_i21():
    def __init__(self,kargs='{}'):
        kargs = eval(kargs)
        self.rootdir = r'D:\Program Files (x86)\Thunder Network\Thunder\Program'
        if kargs.has_key('user'):
            self.user = kargs['user']
        else:
            self.user = 'admin'
        if kargs.has_key('pwd'):
            self.pwd = kargs['pwd']
        else:
            self.pwd = 'admin'
        if kargs.has_key('dip'):
            self.dip = kargs['dip']
        else:
            self.dip="192.168.1.254"
        if kargs.has_key('ssid'):
            self.ssid = kargs['ssid']
        else:
            self.ssid = ''
        if kargs.has_key('pwd'):
            self.pwd = kargs['pwd']
        else:
            self.pwd = ''
        # self.session=requests.Session()
        self.config_wireless()
    def login(self):
        url= "http://%s/"%(self.dip)
        headers = {"Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","X-DevTools-Emulate-Network-Conditions-Client-Id": "ED1D01C0276BCC11E96C5678943A7897"}
        requests.get(url,headers)
        url = "http://%s/login/Auth"%(self.dip)
        data  ={'usertype':"%s"%self.user,
                'password':"YWRtaW4=",
                'username':"admin"}
        headers = {'Host': '%s' %self.dip, 
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://%s'%self.dip,
                "X-Requested-With": "XMLHttpRequest",
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-GB,en;q=0.9,kk;q=0.8,zh;q=0.7,zh-CN;q=0.6,en-US;q=0.5,hu;q=0.4,ko;q=0.3',
                'Cookie': 'i21_user=admin; bLanguage=cn'
                 }
        ret = requests.post(url,data = data,headers=headers)
        if ret.status_code == 200:
            print "ret.url",ret.url
            print "login successfully"
            return True
        else:
            print "login unsucessfully"
            return False    
    '''
    ssid:设备ssid配置
    wifiPwd ：设备pwd配置
    secMode ：设备加密方式 可选 
            wpa2psk
            none
            wep
            wpapsk
            wpa2psk
            wpawpa2psk
    ssidEn :true,false
    cipherType: 加密方式
            aes
            tkip
            aes+tkip
    broadcastSsidEn :true,false 开启/关闭ssid隐藏
    '''
    def config_wireless(self,kargs='{}'):
        self.login()
        init_default_dict = {"GO":"wireless_basic.asp","wrlRadio":"2.4G","enableWireless":"","broadcast":"","ssidIndex":"0","ssidEn":"true","broadcastSsidEn":"true","apIsolationEn":"false","wmfEn":"true","probeEn":"false","maxClients":"48","ssid":"tendatest","ssidEncode":"utf-8","secMode":"wpa2psk","wepAuth":"open","radiusServerIp":"","radiusPort":"1812","radiusPwd":"","wepDefaultKey":"1","wepKey1":"12345","wepKey1Type":"1","wepKey1":"12345","wepKey1Type":"1","wepKey1":"12345","wepKey1Type":"1","wepKey2":"12345","wepKey2Type":"1","wepKey3":"12345","wepKey3Type":"1","wepKey4":"12345","wepKey4Type":"1","cipherType":"aes","wifiPwd":"123654789","keyPeriod":"0","radio":"2.4G",}
        kargs = self.init_args(kargs,**init_default_dict)
        print "data",kargs
        if self.ssid != '' and kargs['ssid'] =='tendatest':
            kargs['ssid']=self.ssid
        if self.pwd != '' and kargs['wifiPwd'] =='123654789':
            kargs['wifiPwd']=self.pwd
        data = {
                "GO":"%s"%kargs['GO'],
                "wrlRadio":"%s"%kargs['wrlRadio'],
                "enableWireless":"",
                "broadcast":"",
                "ssidIndex":"0",
                "ssidEn":"%s"%kargs['ssidEn'],
                "hideSsid":"false",
                "broadcastSsidEn":"%s"%kargs['broadcastSsidEn'],
                "apIsolationEn":"false",
                "wmfEn":"true",
                "probeEn":"false",
                "maxClients":"48",
                "ssid":"%s"%kargs['ssid'],
                "ssidEncode":"utf-8",
                "secMode":"%s"%kargs['secMode'],
                "wepAuth":"open",
                "radiusServerIp":"",
                "radiusPort":"1812",
                "radiusPwd":"",
                "wepDefaultKey":"1",
                "wepKey1":"12345",
                "wepKey1Type":"1",
                "wepKey2":"12345",
                "wepKey2Type":"1",
                "wepKey3":"12345",
                "wepKey3Type":"1",
                "wepKey4":"12345",
                "wepKey4Type":"1",
                "cipherType":"%s"%kargs['cipherType'],
                "wifiPwd":"%s"%kargs['wifiPwd'],
                "keyPeriod":"0",
                "radio":"%s"%kargs['radio'],
                }
        headers = {'Host': '%s' %self.dip, 
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.9,kk;q=0.8,zh;q=0.7,zh-CN;q=0.6,en-US;q=0.5,hu;q=0.4,ko;q=0.3",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "i21_user=admin; bLanguage=cn",
                "Host": "%s"%(self.dip),
                "Origin": "http://%s"%(self.dip),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                 }
        url = "http://%s/goform/setWrlBasicInfo"%(self.dip)
        ret = requests.post(url,data = data,headers=headers)
        if ret.status_code == 200:
            print "config_wireless_sucess"
            return True
    '''
    配置AP DHCP服务器
    dhcpEn：true or false
    
    '''
    def config_dhcpserver(self,kargs='{}'):
        self.login()
        init_default_dict = {"GO":"lan_dhcps.asp","dhcpEn":"true","dhcpStartIp":"192.168.1.100","dhcpEndIp": "192.168.1.200","dhcpLeaseTime": "86400","dhcpMask":"255.255.255.0","dhcpGw":"192.168.1.1","dhcpDns1": "192.168.1.1","dhcpDns2":"8.8.4.4","radio": "2.4G"}
        kargs = self.init_args(kargs,**init_default_dict)
        print "data",kargs
        #if self.ssid != '' and kargs['ssid'] =='tendatest':
        #    kargs['ssid']=self.ssid
        #if self.pwd != '' and kargs['wifiPwd'] =='123654789':
        #    kargs['wifiPwd']=self.pwd
        data = {
                "GO":"lan_dhcps.asp",
                "dhcpEn":"%s"%kargs['dhcpEn'],
                "dhcpStartIp":"192.168.1.100",
                "dhcpEndIp":"192.168.1.200",
                "dhcpLeaseTime":"86400",
                "dhcpMask":"255.255.255.0",
                "dhcpGw":"192.168.1.1",
                "dhcpDns1":"192.168.1.1",
                "dhcpDns2":"8.8.4.4",
                "radio":"2.4G",
                }
        headers = {'Host': '%s' %self.dip, 
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "i21_user=admin",
                "Origin": "http://%s"%(self.dip),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                 }
        url = "http://%s/goform/setDhcpInfo"%(self.dip)
        ret = requests.post(url,data = data,headers=headers)
        if ret.status_code == 200:
            print "config_dhcpserver_sucess"
            return True
    '''
    netMode : 网络模式a、an、ac
    channel ：设备channel配置
    bandwidth ：设备bandwidth配置  20 40 80
    extendChannel : upper lower扩展信道的配置 ，如8信道,upper为4，lower为12
    '''
    def config_RadioInfo_5G(self,kargs='{}'):
        self.login()
        init_default_dict = {"GO": "wireless_radio.asp",
                "wrlRadio": "1",
                "wirelessEn": "true",
                "country": "CN",
                "netMode": "ac",
                "channel": "0",
                "bandwidth": "20",
                "extendChannel": "lower",
                "channelLockEn": "false",
                "wmmEn": "true",
                "txPower": "18",
                "setPower": "true",
                "Plcp": "1",
                "sgiTx": "1",
                "ssidIsolationEn": "false",
                "radio": "5G",}
        kargs = self.init_args(kargs,**init_default_dict)
        data = {
                "GO": "wireless_radio.asp",
                "wrlRadio": "0",
                "wirelessEn": "true",
                "country": "CN",
                "netMode": "%s"%kargs['netMode'],
                "channel": "%s"%kargs['channel'],
                "bandwidth": "%s"%kargs['bandwidth'],
                "extendChannel": "%s"%kargs['extendChannel'],
                "channelLockEn": "false",
                "wmmEn": "true",
                "txPower": "20",
                "setPower": "true",
                "Plcp": "1",
                "sgiTx": "1",
                "ssidIsolationEn": "false",
                "radio": "%s"%kargs['radio']
                }
        headers = {'Host': '%s' %self.dip, 
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.9,kk;q=0.8,zh;q=0.7,zh-CN;q=0.6,en-US;q=0.5,hu;q=0.4,ko;q=0.3",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "i21_user=admin; bLanguage=cn",
                "Host": "%s"%(self.dip),
                "Origin": "http://%s"%(self.dip),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                 }
        url = "http://%s/goform/setWrlRadioInfo"%(self.dip)
        ret = requests.post(url,data = data,headers=headers)
        if ret.status_code == 200:
            print "config_wireless_sucess"
            return True
    '''
    netMode : 网络模式b、g、n、bg、bgn 
    channel ：设备channel配置
    bandwidth ：设备bandwidth配置 auto 20 40
    extendChannel : upper lower扩展信道的配置 ，如8信道,upper为4，lower为12
    '''
    def config_RadioInfo(self,kargs='{}'):
        self.login()
        init_default_dict = {"GO": "wireless_radio.asp",
                "wrlRadio": "0",
                "wirelessEn": "true",
                "country": "CN",
                "netMode": "bgn",
                "channel": "0",
                "bandwidth": "auto",
                "extendChannel": "lower",
                "channelLockEn": "false",
                "wmmEn": "true",
                "txPower": "20",
                "setPower": "true",
                "Plcp": "1",
                "sgiTx": "1",
                "ssidIsolationEn": "false",
                "radio": "2.4G",}
        kargs = self.init_args(kargs,**init_default_dict)
        data = {
                "GO": "wireless_radio.asp",
                "wrlRadio": "0",
                "wirelessEn": "true",
                "country": "CN",
                "netMode": "%s"%kargs['netMode'],
                "channel": "%s"%kargs['channel'],
                "bandwidth": "%s"%kargs['bandwidth'],
                "extendChannel": "%s"%kargs['extendChannel'],
                "channelLockEn": "false",
                "wmmEn": "true",
                "txPower": "20",
                "setPower": "true",
                "Plcp": "1",
                "sgiTx": "1",
                "ssidIsolationEn": "false",
                "radio": "2.4G"
                }
        headers = {'Host': '%s' %self.dip, 
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.9,kk;q=0.8,zh;q=0.7,zh-CN;q=0.6,en-US;q=0.5,hu;q=0.4,ko;q=0.3",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "i21_user=admin; bLanguage=cn",
                "Host": "%s"%(self.dip),
                "Origin": "http://%s"%(self.dip),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                 }
        url = "http://%s/goform/setWrlRadioInfo"%(self.dip)
        ret = requests.post(url,data = data,headers=headers)
        if ret.status_code == 200:
            print "config_wireless_sucess"
            return True

    #获取2.4G客户端ip地址
    #传入客户端2.4Gmac地址
    def get_client_info(self,kargs='{}'):
        self.login()
        init_default_dict = {"mac":"50:2B:73:FB:5F:E1"}
        kargs = self.init_args(kargs,**init_default_dict)
        headers = {'Host': '%s' %self.dip, 
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en;q=0.9,kk;q=0.8,zh;q=0.7,zh-CN;q=0.6,en-US;q=0.5,hu;q=0.4,ko;q=0.3",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "i21_user=admin",
                "Host": "%s"%self.dip,
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                }
        url = 'http://%s/goform/getWrlClients?radio=2.4G&ssidIndex=0&r=0.13778371262058386&_=1544403792681'%self.dip
        ret = requests.get(url,headers=headers)
        if ret.status_code == 200:
            ret=ret.json()
            print "ret.json",ret
            try:
                for i in range(10):
                    if kargs['mac'] == str(ret['clients'][i]['mac']):
                        ip=str(ret['clients'][i]['ip'])
                        return ip
            except:
                return False
            
    def init_args(self,args,**kargs):
        retdict =eval(args)
        for k,v in kargs.iteritems():
            if not retdict.has_key(k):
                retdict[k] = v
        return retdict
    def windows_iface_mode(self,kargs='{}'):
        init_default_dict = {"iface":"kc","mode":"static","ip":"","mask":"255.255.255.0","gateway":"","dns":""}
        kargs = self.init_args(kargs,**init_default_dict)
        if kargs['mode'] == 'dhcp':
            cmd = 'netsh interface ip set dns %s dhcp'%kargs['iface']
            os.system(cmd)
            cmd1 = 'netsh interface ip set address %s dhcp'%kargs['iface']
            os.system(cmd1)
        else:
            cmd = 'netsh interface ip set address %s static %s %s %s'%(kargs['iface'],kargs['ip'],kargs['mask'],kargs['gateway'])
            os.system(cmd)
            cmd1 = 'netsh interface ip set dns %s static %s'%(kargs['iface'],kargs['dns'])
            os.system(cmd1)
        return True
    def waitTime(self,num):
        for x in xrange(int(num)):
            print "%d/%d sum=%d" %(x,num,num)
            time.sleep(1)
        return True
if __name__ == "__main__":
    km = kmClass_i21()
    km.get_client_info()
    #kt_obj = ktClass(type="adb",host="192.168.20.2",username="root",password="tendatest")
    #kt_obj = ktClass(type="ssh",host="192.168.3.128",username="root",password="tendatest")
    #kt_obj2 = ktClass(type="ssh",host="192.168.20.10",username="root",password="tendatest")
    # ks=ks()
    # aaa = {'ip':'MTU:1500','iface':'br0','expe':'pass'}
    # ss=ks.checkIp(str(aaa))
    # ss=ks.face_updown(5,'eth1')
    upnps = {"target":"MINIUPNPD","sent":"iptables -t nat -nvL","expe":"pass"}
    # for i in range(10):
        # ss=ks.checkUpnp(str(upnps))
        # ss=ks.reboot()
        # print "ss==",ss
    aaa = {'target':'10','sent':'uptime','expe':'pass'}
    bbb = {'target':'0','sent':'iwpriv wlan1 get_mib rm_activated','expe':'pass'}
    # bbb = {'target':'0','sent':'ifconfig','expe':'pass'}
    
    # ss=ks.check_Fast_Roaming(str(bbb))
    # ss=ks.checkupTime(str(aaa))
    # print "ss = ",ss
    # pwd = '123456789'
    # ks.reboot(pwd)
    #ssid={'ssid':'Mesh_Auto_Test',"WpaPsk":"12345678",'AuthMode':'WPA2PSK',"EncrypType":"AES"}
    #ssid={'ssid':'~!@#$%^*()_+{}:?,c.#',"WpaPsk":"12345678",'AuthMode':'WPA2PSK',"EncrypType":"AES"}
    #ssid={'ssid':'`~!@#$%^&*()_+\{\}|:<>?-\=\[]\;,./',"WpaPsk":"12345678",'AuthMode':'WPA2PSK',"EncrypType":"AES"}
    #ssid={'ssid':'Mesh_Auto_Test',"WpaPsk":"~!@#$%^*()_+{}:?,5.#;[]\/=-123451234567812345678123456781234567",'AuthMode':'WPA2PSK',"EncrypType":"AES"}
    #ssid={'ssid':'Mesh_Auto_Test',"WpaPsk":'123451234567812345678123456781234567','AuthMode':'WPA2PSK',"EncrypType":"AES"}
    ssid={'ssid':'1mmmmmmmm',"wpapsk":"12345678","workhz":"5",'authmode':'WPA2PSK',"encryptype":"AES"}
    #ssid={'ssid':'Nove_Test_Mesh_Guest',"wpapsk":"12345678","workhz":"5",'authmode':'WPA2PSK',"encryptype":"AES"}
    #ssid={'ssid':'Mesh_Auto_Test',"wpapsk":"123456789012345678901234567890123456789012345678901234567890AAA","workhz":"2.4",'authmode':'WPA2PSK',"encryptype":"AES"}
    #ssid={'ssid':'Mesh_Auto_Test',"wpapsk":"~!@#$%^*()_+{}:?,5.#;[]\/=-123451234567812345678123456781234567","workhz":"2.4",'authmode':'WPA2PSK',"encryptype":"AES"}
    #ssid={'ssid':'NOVA_VIP',"wpapsk":"12345678","workhz":"5",'authmode':'WPA2PSK',"encryptype":"AES"}
    #ch = {'ssid':'Mesh_Auto_Test','authmode':'WPA2PSK','crypto':'AES','channel':'40','pwd':'12345678'}
    #a=kt_obj2.default_channel(str(ch))
    #print "a",a
    
        #AuthMode OPEN/SHARED/WPAPSK/WPA2PSK
        #EncrypType NONE/WEP/AES/TKIP
        #WpaPsk   #用于WPAPSK或者WPA2PSK加密
        #Key 用于WEP加密密码
        #DefaultKeyID 用于WEP加密
        
        #init_default_dict = {'WirelessMode':5,'NetworkType':'Infra','ssid':'','AuthMode':'OPEN','EncrypType':'NONE','DefaultKeyID':'1','Key':'','expe':'pass','Intf':'ra0','WpaPsk':'','HSsid':''}    

    #kt_obj2.w522u_wireless_connect_extend(str(ssid))
    #kt_obj2.w522u_wireless_connect(str(ssid))
    #kt_obj3 = ktClass(type="ssh",host="192.168.20.30",username="admin",password="admin")
    #print "a=",a
    #kt_obj = ktClass(type="com",host="192.168.3.160",password="MTIzNDU2Nzg=")
    #kt_obj = ktClass(type="com",host="192.168.3.160",password="Fireitup")
    #kt_obj.sendCmd("ifconfig")
    #ks_obj = ks()
    #code=ks_obj.reboot()
    #text = ks_obj.readfromcom()
    #print code
    ipdict = {"iface":"eth1","ip":"192.168.3.35","mask":"255.255.255.0","gateway":"192.168.3.1","dns":"192.168.3.1","mtu":"1450","mac":"00:ab:cd:11:22:33","dns":"223.5.5.5"}
    init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"10.10.10.1","rip":"10.10.10.10","num":"1","iface":"eth1","padot":"0","dns":"202.96.134.133,202.96.128.86","mtu":"","mru":"","mppe":"","servername":"","repadr":"","mode":"add"}
    pptp_dict = {"auth":"chap","user":["test"],"pwd":["test"],"lip":"21.1.1.1","rip":"21.1.1.100","iface":"eth1","dns":"202.96.134.133,202.96.128.86",'cf':"/etc/pptpd.conf","pptpopt":"/etc/ppp/options.pptpd","mppe":"","mode":"add"}
    l2tp_dict = {"auth":"chap","user":["test"],"pwd":["test"],"lip":"22.1.1.1","rip":"22.1.1.100","iface":"eth1","dns":"202.96.134.133,202.96.128.86","mppe":"","mode":"add"}
    ftpdict = {"port":"21","rootdir":"/var/ftp","cf":"/etc/vsftpd/vsftpd.conf","file":"testfile","data":"ABCDEFGHIJKLMNTEST"}
    httpdict = {"port":"80","rootdir":"/var/www","cf":"/etc/httpd/conf/httpd.conf","subdir":"index.htm","data":"ABCDEFGHIJKLMNTEST"}
    dnsdict = {"dns":"192.168.20.2","urlip":"www.baidu.com#1.1.1.1,www.tenda.com#2.2.2.2,www.sansang.com#3.3.3.3","cf":"/var/named"}
    #code= kt_obj.dnsSerCfg(str(dnsdict))
    #print code
    
    pkrecvdict = {"sip":"192.168.20.2","sport":"6000","pro":"tcp","num":"","size":""}
    pksenddict= {"dip":"192.168.20.2","dport":"6000","pro":"tcp","iface":"","sport":"","sip":"","num":"","size":"","flag":"1","loss":0.1,"expemss":"1455","expe":"pass"}
    #dhcpd_dict = {"pool":"192.168.20.3,192.168.20.10","lease":"60","gw":"192.168.20.2","dns":"8.8.8.8","mask":"255.255.255.0","cf":"/tmp/dhcpd.conf","iface":"eth5","lf":"/var/db/dhcpd.leases","adopt":"","delopt":"","chkopt":"","chklen":"","relet":"","noack":"","mac":"","alert":"","of":"/var/tendatest/TDRouter2/tmp/log_dhcpc.txt","dellog":"0"}
   # dhcpd_dict = {"pool":"192.168.20.3,192.168.20.10","lease":"30","gw":"192.168.20.1","dns":"8.8.8.8","mask":"255.255.255.0","iface":"eth5"}
    #dhcpd_dict = {"pool":"192.168.10.11,192.168.10.112","lease":"60","gw":"192.168.10.10","dns":"8.8.8.8","mask":"255.255.255.0","iface":"eth5","relet":"1","adopt":"33,8,I:192.168.11.1,192.168.10.1."}
    #dhcpd_dict = {"pool":"192.168.10.11,192.168.10.11","lease":"6","gw":"192.168.10.10","dns":"8.8.8.8","mask":"255.255.255.0","iface":"eth5","adopt":"121,8,N1:24,192,168,11,192,168,10,1."}
    #dhcpd_dict = {"pool":"192.168.10.11,192.168.10.11","lease":"6","gw":"192.168.10.10","mask":"255.255.255.0","dns":"8.8.8.8","iface":"eth5","noack":"1","adopt":"249,8,N1:24,192,168,11,192,168,10,1.","relet":"1"}
    #dhcpd_dict = {"pool":"192.168.10.11,192.168.10.11","lease":"6","gw":"192.168.10.10","mask":"255.255.255.0","dns":"8.8.8.8","iface":"eth5","noack":"1","adopt":"51,4,N4:-1.","relet":"1"}
    #dhcpd_dict = {"pool":"192.168.10.8,192.168.10.8","lease":"6","gw":"192.168.10.10","mask":"255.255.255.0","dns":"8.8.8.8","iface":"eth5","noack":"1","adopt":"249,8,N1:24,192,168,11,192,168,10,1.","relet":"1"}
    #dhcpd_dict = {"pool":"192.168.5.8,192.168.5.8","lease":"60","gw":"192.168.5.1","mask":"255.255.255.128","iface":"eth1"}
    dhcpd_dict = {"pool":"10.10.10.10,10.10.10.10","lease":"6","gw":"10.10.10.1","mask":"255.0.0.0","dns":"8.8.8.8","iface":"eth1"}
    #code= kt_obj2.dhcpSerCfg(str(dhcpd_dict))
    #code= kt_obj2.sendCmd(str("killall -9 dhcpd"))
    #times = 60.0
    #code = kt_obj2.waitTime(times)
    #print code
    # code = kt_obj.pktRecv(str(pkrecvdict))
    upnpdict = {"lip":"192.168.3.105","wport":"10000","lport":"10000","pro":"all"}
    # upnpdict = {"lip":"192.168.3.105","wport":"10000","lport":"10000","pro":"all"}
    upnpchk_dict = {"modelname":"Tenda","modelnumber":"Tenda","url":"http://192.168.3.1/","manufacturer":"HF"}
    pingdict={"dip":"10.10.10.1","iface":"wlan0","size":"64","maxsuc":"5","maxerr":"5","expe":"pass"}
    #code= kt_obj.ping(str(pingdict))
    ssid={"switch":"ON","ssid":"","pwd":"12345678","config":"guest_network","authmode":"WPA2PSK","crypto":"AES","channel":"40"}
    #kt_obj.wireless_connect(str(ssid))
    setip = {"iface":"wlan0","ip":"192.168.3.166","mask":"","gateway":"","dns":"","mac":"","mtu":""}
    #code=kt_obj.setIp(str(setip))
    #init_default_dict = {"auth":"chap","user":['12345'],"pwd":["tenda"],"lip":"10.10.10.1","rip":"10.10.10.2","num":"1","iface":"eth4","padot":"0","dns":"202.96.134.133,202.96.128.86","mtu":"","mru":"","mppe":"","servername":"","repadr":"","mode":"add"}
    init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"172.16.0.1","rip":"172.16.0.2","num":"1","iface":"eth1","padot":"0","dns":"202.96.134.133,202.96.128.86","mtu":"","mru":"","mppe":"","servername":"","repadr":"","mode":"add"}
    init_default_dict = {"auth":"chap","user":["tenda"],"pwd":["tenda"],"lip":"10.10.10.1","rip":"10.10.10.2","num":"1","iface":"eth1","padot":"0","mtu":"","mru":"","mppe":"","servername":"","repadr":"","mode":"add"}
    #code= kt_obj2.pppoeSerCfg(str(init_default_dict))
    #print code
    #PSST_ceshi_qdy
    init_default = {'ssid':'jhgcd','authmode':'WPA2PSK','crypto':'AES','key':'','index':'','expe':'pass','channel':'6','rate':'144','pwd':'12345678','bssid':''}
    U12 = {"ssid":"5555U","channel":"6"}
    wireless = {"ssid":"mesh_auto_test","expe":"fail"}
    #code = kt_obj.wireless_scan(str(wireless))
    #code = kt_obj.default_guest(str(init_default))
    #print code
    #code = kt_obj.frequency_5G(str(U12))
    #code = kt_obj.default_protocol(str(U12))
    #print code
    httpdict = {"ip":"192.168.20.2"}
    # kt_obj.sendCmd("""echo lock > /etc/ppp/options""")
    # kt_obj.sendCmd("""echo "unit 1" >> /etc/ppp/options""")
    # kt_obj.sendCmd("""echo "require-chap" >> /etc/ppp/options""")
    l2tpclidict={"auth":"mschap","iface":"eth1","user":"tenda","pwd":"tenda","mppe":"both","unit":"1","expe":"pass"}
    l2tpclidict={"desc":"l2tp","ip":"192.168.20.3","user":"tenda","pwd":"tenda","auth":"mschap-v2","mppe":"both","mode":"add","expe":"pass"}
    arpsenddict = {"sip":"192.168.3.2","smac":"00:11:22:33:55:44","dip":"192.168.3.1","dmac":"00:11:22:33:55:ab","type":"2","time":"1","num":"10","iface":"eth1"}
    # code = kt_obj.arpSend(str(arpsenddict))
    nslookupdict = {'url':"www.tenda.com.cn",'expeip':"182.92.168.49","serip":"192.168.3.1"}
    # print kt_obj.nslookup(str(nslookupdict))
    parserPacketdict = {'filter':'bootp.option.dhcp=1,bootp.option.type = 12'}
    packetCapturedict = {"iface":"eth4"}
    #code1=kt_obj2.packetCapture(str(packetCapturedict))
    #print "code1 = ",code1
    #self.waitTime(10)
    #code=kt_obj2.parserPacket(str(parserPacketdict))
    #print "code = ",code 
    # kt_obj.sendCmd("dhclient eth1")
    ssid={"ssid":'6666',"pwd":"12345678"}
    #code = kt_obj.adb_wifi_config((str(ssid)))
    #print code
    #print code
    #print code
    # code = kt_obj.ntpSerCfg()
    # print code
    # print  kt_obj.sendCmd("ps")
