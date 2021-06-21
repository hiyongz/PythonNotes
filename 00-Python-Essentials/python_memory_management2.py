#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/6/21 16:02
# @Author:  haiyong
# @File:    python_memory_management2.py

a = 300
b = 300
print(id(a))

print(id(b))

c = b
print(id(c))


a = -6
b = -6
c = b
print(id(a))
print(id(b))

l1 = [1, 2, 3, 4]
l2 = [1, 2, 3, 4]
l3 = l2
print(id(l1))
print(id(l2))
print(id(l3))
print("666")
t1 = (1, 2, 3, 4)
t2 = (1, 2, 3, 4)
t3 = t2
print(id(t1))
print(id(t2))
print(id(t3))

a = 'Hello World'
b = 'Hello World'
c = 'Hello Worl'

print(a is b)
print(a == b)
print(a is c+'d')
print(a == c+'d')

a = "Data Science"
b = "Data Science"