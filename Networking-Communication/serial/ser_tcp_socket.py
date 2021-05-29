# -*- coding:utf8 -*-  
'''
版本号:1.1
执行方式 ser.py 10 38400
#串口号
port='COM10'
#波特率
baudrate
'''
import socket,serial,threading,time,signal,os,sys,re,select
import json

#线程锁
mutex = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self,func,*args):
        threading.Thread.__init__(self)
        self.func = func
        self.args=args
    def run(self):
        self.func(*self.args)

class MySerial():

    def __init__(self):
        self.HOST = ''  # use '' to expose to all networks
        self.PORT = 12349
        self.data = []
        self.button = 1
        self.g_data = ""
        try:
            self.PORT = int(sys.argv[1])
            self.BaudRate = int(sys.argv[2])
            self.COM = sys.argv[3]
            self.COM = str(self.COM)
        except Exception as e:
            self.PORT = input('1 : Please Input connect_port*#example:12345#*  :')
            self.BaudRate = input('2 : Please Input BaudRate*#example:115200#*  :')
            self.COM = input('3 : Please Input COM number*example:1/2/3*  :')
            self.COM = 'com' + str(self.COM)

    def open_logfile(self):
        try:
            filename = "./log/"
            filename = filename + self.COM + '_' + '.log'
        except Exception as e:
            print("e\n", e)

        # filename="ser.log"
        print("filename=", filename)
        # if os.path.exists(filename):
        # os.remove(filename)
        self.f = open(filename, 'ab+')
        print("f", self.f)

    def connect_serial(self):
        self.ser = serial.Serial(
            port=self.COM,
            baudrate=self.BaudRate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            xonxoff=False,
            rtscts=False,
            timeout=0.2,        # set timeout 3s. It is best to set up more than 1 seconds and not too long time
            interCharTimeout=None
        )

        if ser is None:
            print("can't open serial")
            self.ser.write('automate_interface fflush')
            self.ser.write('\n')


                
    def loop_read_write(self):
        print("enter loop")
        try:
            while 1:
                list_data=ser.readlines()
                if list_data:
                    g_data = "".join(list_data)
                    timedate = "\n/******"+time.ctime()+"******/\n\n"
                    text = timedate + g_data
                    self.f.write(text)
                    self.f.flush()
        except KeyboardInterrupt:
            print('stopped by keyboard')
        except Exception as e:
            print(e)
        print("write data over")
        self.f.close()
        self.ser.close()


class MySocketServer(MySerial):
    def __init__(self,host, port):
        super(MySocketServer, self).__init__()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(10)

    def socket_accept(self,host,port=int(PORT)):
        global ser,button,g_data,FLAG
        sock = init_socket(host,port)
        inputs=[sock]
        # print("sock = ",inputs
        while 1:
            rs,ws,es=select.select(inputs,[],[],3) #有client connect/send 的时候会有可读对象
            # print(u"rs ..........对象.:",rs
            for r in rs:    #rs  [ser,clientsock],只有当客户端 connect/send/close 进入下面的循环
                            #rs 为空时 不进入
                if r is sock:    # 1.connect
                    print("++++++++++++++++++++++++++++connect+++++++++++++++++++++++++++")
                    clientsock, clientaddr = sock.accept()
                    inputs.append(clientsock);
                    #clientsock.settimeout(0.5)
                else:
                    #print("66666666666666666"
                    try:
                        recv_from_cli=r.recv(4096)   #r 为 clientsock 的对象
                    except Exception as e:
                        print("Exception.............",e)
                        recv_from_cli=None
                                        #2.close
                    if not recv_from_cli:      #没有数据会返回一个空字符串，  客户端 close 的时候会触发
                        print("close..................")
                        inputs.remove(r);
                                        #3.send
                    else:                #只要客户端不关闭连接，那么就会一直
                        #print("7777777778888888888888888888",recv_from_cli
                        global f,ser
                        cmd="""\x0d\x0a"""
                        # ser.write(cmd)
                        # ser.flushInput()
                        #time.sleep(0.4)
                        ser.flushInput()
                        ser.write(recv_from_cli+cmd)
                        time.sleep(0.1)

                        for x in range(10):
                            # print("g_data============================= = ",g_data
                            if 'reboot' not in recv_from_cli:
                                if re.search(r'# ',g_data):
                                    G_data=g_data
                                    g_data=''
                                    # print("find # ..................:\n",G_data
                                    try:
                                        r.sendall(G_data)
                                    except Exception as e:
                                        print(e)
                                    break
                                else:
                                    time.sleep(0.1)
                                    print("wait 0.1ssss!")
                        try:
                            if not g_data:
                                g_data='no g_data'
                            r.sendall(g_data)
                        except Exception as e:
                            print(e)


    
if __name__ == '__main__':
    threads = []
    # ThreadFuncs = [tcpser,PyAutoTest]
    ThreadFuncs = [PyAutoTest]
    for ThreadFunc in ThreadFuncs:
        t = MyThread(ThreadFunc, (HOST))
        t.setDaemon(True)
        threads.append(t)

    for thread in threads:
        thread.start()

    loop()
    
 

 
