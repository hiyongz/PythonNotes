#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/5/27 21:36
# @Author:  hiyongz
# @File:    python_memory_management.py

# 列表
l1 = [1, 2, 3]
print(id(l1))  # 返回对象的内存地址

l2 = l1
print(id(l2))

l1.append(4)
print(id(l1))

print(l1)
print(l2)

l3 = [4, 5, 6]
print(id(l3))

# 变量赋值
a = 1
print(id(a))
b = a
print(id(b))
a = a + 1
print(id(a))
c = 1
print(id(c))

# == vs is
a = 1
b = a
print(id(a))
print(id(b))
print(a == b)
print(a is b)

c = 6553600000000
d = 6553600000000
print(id(c))
print(id(d))
print(c == d)
print(c is d)