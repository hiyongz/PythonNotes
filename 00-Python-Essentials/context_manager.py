#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/27 17:02
# @Author:  haiyong
# @File:    test_context.py

class ContextDemo():
    def open_file(self):
        file_descriptors = []
        for x in range(100000):
            file = open('test.txt', 'w')
            file_descriptors.append(file)
            # file.close()


cont = ContextDemo()
cont.open_file()