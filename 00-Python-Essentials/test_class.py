#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/4/5 14:54
# @Author:  haiyong
# @File:    test_class.py


class A(object):
    def __init__(self):
        self._a = 1

    def __setattr__(self, key, value):
        if not isinstance(value, int):
            raise ValueError('该属性值必须为int')
        else:
            if key == 'a':
                self._a = value
    def test(self):
        print(self._a)


mya = A()

mya.a = 2
mya.test()
mya.a = "123"
