#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/6/6 16:32
# @Author:  hiyongz
# @File:    python_nest_function.py

# Python 嵌套函数

VALUE1 = 666

def TestFunc(val1):
    val = val1
    def innerFunc():
        print(val)

    innerFunc()



def TestFunc2():
    global VALUE1
    VALUE1 = VALUE1 + 1
    print(VALUE1)

def TestFunc3():
    VALUE1 = 2
    print(VALUE1)


def TestFunc4():
    val = 1
    def innerFunc():
        nonlocal val
        val = 2
        print("inner:",val)
    innerFunc()
    print("outer:", val)

# TestFunc('Hello world')

# TestFunc2()
# print(VALUE1)

# TestFunc3()
# print(VALUE1)

TestFunc4()

