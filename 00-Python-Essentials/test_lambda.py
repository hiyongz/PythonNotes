#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/6/3 22:23
# @Author:  hiyongz
# @File:    test_lambda.py


# 匿名函数
def cube(y):
    return y*y*y

lambda_cube = lambda y: y*y*y

print(cube(3))
print(lambda_cube(3))

# 例子1
list_num = [3, 4, 6, 2, 5, 8]
list_square = [x ** 2 for x in list_num if x % 2 == 0]
list_square2 = [(lambda x: x** 2)(x) for x in list_num if x % 2 == 0]
print(list_square)
print(list_square2)

# l1 = [(1, 20), (3, 0), (9, 10), (2, -1)]
# l.sort(key=lambda x: x[1]) # 按列表中元组的第二个元素排序
# print(l)

mydict = {1:"apple",3:"banana",2:"orange"}
mydict = sorted(mydict.items(), key=lambda x: x[0], reverse=True)
print(mydict)
