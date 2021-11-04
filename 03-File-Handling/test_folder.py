#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os

print(__file__)

# 获取当前文件__file__的路径
print(os.path.realpath(__file__))

# 获取当前文件__file__的所在目录
print(os.path.dirname(os.path.realpath(__file__)))
# 获取当前文件__file__的所在目录
print(os.path.split(os.path.realpath(__file__))[0])

# path = os.path.dirname(os.path.realpath(__file__)).decode('gbk')
# tmpdir = os.path.join(path, "tmp")
# staticdir = os.path.join(path, "static")
# image_one = os.path.join(tmpdir, self.im_source_path)
# image_two = os.path.join(staticdir, self.im_target_path)
# im_source_obj = Image.open(self.im_source_path)
