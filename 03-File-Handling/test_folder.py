#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os
import sys

# 获取当前文件__file__的路径
print(__file__)
print(sys.argv[0])
print(os.path.realpath(__file__))
print(os.path.abspath(sys.argv[0]))
print("#"*20)

# 获取当前文件__file__的所在目录
print(os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.split(os.path.realpath(__file__))[0])
path = os.path.dirname(os.path.realpath(__file__))

# 获取当前文件名名称
print("#"*20)
print(os.path.basename(sys.argv[0])) # 当前文件名名称
print(os.path.basename(__file__)) # 当前文件名名称
filename = os.path.basename(__file__)

# 拼接路径
abspath = os.path.join(path, filename)
print(abspath)

# 创建目录
if not os.path.exists(path):
    print(f"创建文件: {path}")
    os.makedirs(path)

# 创建文件：创建一个txt文件
text = "Hello World!"
newfilepath = os.path.join(path, "newfile.txt")
file = open(newfilepath, 'w')
file.write(text)  # 写入内容信息
file.close()

# 判断文件是否存在
print("#"*20)
print("判断文件是否存在")
print(os.path.isfile(path))
print(os.path.isfile(newfilepath))
print(os.path.exists(newfilepath))

# 判断文件属性
print("判断文件属性")
print(os.access(newfilepath,os.F_OK)) # 文件是否存在
print(os.access(newfilepath,os.R_OK)) # 文件是否可读
print(os.access(newfilepath,os.W_OK)) # 文件是否可以写入
print(os.access(newfilepath,os.X_OK)) # 文件是否有执行权限

# 打开文件
# https://www.geeksforgeeks.org/open-a-file-in-python/?ref=lbp
file = open(newfilepath, 'r')
print(file.read())
file.close()


