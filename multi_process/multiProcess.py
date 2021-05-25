#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2020/10/23 15:58
# @Author:  haiyong
# @File:    calc_multiProcess.py

# python 多进程

from multiprocessing import Process
import os
import time
from multi_process.mytask import Task

class TestProcess():

    def multiprocess_cpu_bound(self):
        print(f'父进程: {os.getpid()}')
        start = time.time()
        p1 = Process(target=Task.cpu_bound_task, args=(self,100000000,1))
        p2 = Process(target=Task.cpu_bound_task, args=(self,100000000,2))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        end = time.time()
        print("耗时{}秒".format((end - start)))

    def multiprocess_io_bound(self):
        print(f'父进程: {os.getpid()}')
        start = time.time()
        p1 = Process(target=Task.io_bound_task, args=(self,4, 1))
        p2 = Process(target=Task.io_bound_task, args=(self,4, 2))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        end = time.time()
        print("耗时{}秒".format((end - start)))

if __name__=='__main__':
    proce = TestProcess()
    proce.multiprocess_cpu_bound()
    proce.multiprocess_io_bound()

