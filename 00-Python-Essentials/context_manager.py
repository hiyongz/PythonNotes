#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/27 17:02
# @Author:  haiyong
# @File:    test_context.py

from contextlib import contextmanager

class ContextDemo():
    def open_file(self):
        file_descriptors = []
        for x in range(10000):
            file = open('test.txt', 'w')
            file_descriptors.append(file)
            # file.close()

    def open_file_with(self):
        file_descriptors = []
        for x in range(10000):
            with open('test.txt', 'w') as file:
                file_descriptors.append(file)
            # file.close()

    def open_file_with2(self):
        file_descriptors = []
        for x in range(10000):
            file = open('test.txt', 'w')
            try:
                file_descriptors.append(file)
            finally:
                file.close()


class FileManager:
    def __init__(self, name, mode):
        print('__init__ method called')
        self.name = name
        self.mode = mode
        self.file = None

    def __enter__(self):
        print('__enter__ method called')
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('__exit__ method called')
        if self.file:
            self.file.close()
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')
        return True

class contextmanagerdecorator():

    @contextmanager
    def file_manager(self, name, mode):
        try:
            file = open(name, mode)
            yield file
        finally:
            file.close()

    def demo(self):
        with self.file_manager('test.txt', 'w') as file:
            file.write('hello world')


if __name__ == '__main__':
    # cont = ContextDemo()
    # cont.open_file()
    # cont.open_file_with()
    # cont.open_file_with2()

    # 基于类的上下文管理器
    # with FileManager('test.txt', 'w') as f:
    #     print('开始写操作')
    #     f.write('hello world !')
    #     raise Exception('exception raised').with_traceback(None)
    #
    # print(f.closed)

    # 基于生成器的上下文管理器
    cont = contextmanagerdecorator()
    cont.demo()
