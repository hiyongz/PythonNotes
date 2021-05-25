#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2020/10/23 16:06
# @Author:  haiyong
# @File:    calc_multithreading.py

# Python多线程

import os
import threading
import time
from multiprocessing import Pool, cpu_count
from multi_process.mytask import Task

class TestThread():

    def multiprocess_cpu_bound(self):
        start = time.time()
        print(f'主线程: {os.getpid()}')
        thread_list = []
        for i in range(1, 3):
            t = threading.Thread(target=Task.cpu_bound_task, args=(self,100000000,i))
            thread_list.append(t)

        for t in thread_list:
            t.start()

        for t in thread_list:
            t.join()

        end = time.time()
        print(f"耗时{end - start}秒")

    def multiprocess_cpu_bound2(self):
        # https://zhuanlan.zhihu.com/p/46368084
        # Pool类创建多进程
        print(f"CPU内核数:{cpu_count()}")
        print(f'父进程: {os.getpid()}')
        start = time.time()
        p = Pool(4)
        for i in range(2):
            p.apply_async(Task.cpu_bound_task, args=(self,100000000,i))
        p.close()
        p.join()
        end = time.time()
        print(f"耗时{end - start}秒")


    def multiprocess_io_bound(self):
        start = time.time()
        print(f'主线程: {os.getpid()}')
        thread_list = []
        for i in range(1, 3):
            t = threading.Thread(target=Task.io_bound_task, args=(self,4, i))
            thread_list.append(t)

        for t in thread_list:
            t.start()

        for t in thread_list:
            t.join()

        end = time.time()
        print(f"耗时{end - start}秒")

    def multiprocess_io_bound2(self):
        # Pool类创建多进程
        print(f"CPU内核数:{cpu_count()}")
        print(f'父进程: {os.getpid()}')
        start = time.time()
        p = Pool(8)
        for i in range(2):
            p.apply_async(Task.io_bound_task, args=(self,4, i+1))
        p.close()
        p.join()
        end = time.time()
        print(f"耗时{end - start}秒")

if __name__=='__main__':
    proce = TestThread()
    proce.multiprocess_cpu_bound()
    proce.multiprocess_cpu_bound2()
    proce.multiprocess_io_bound()
    proce.multiprocess_io_bound2()
