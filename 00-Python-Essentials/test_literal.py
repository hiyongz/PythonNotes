#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2020/8/22 16:53
# @Author:  haiyong
# @File:    test_literal.py

# python 字面量
name = 'tom'
age = 20
list = [1,2,3]
dict1 = {'name':'tom','gender':'male'}

print(f"my name is \n {name}, age is {age}")
print(f"my name is {name.upper()}")
print(f"result is {(lambda x:x+2)(2)}")