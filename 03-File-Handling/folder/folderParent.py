# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os
import sys
import logging


class TestDir():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

    def test_parentpath(self):
        # 获取当前文件__file__的所在目录
        dirpath = os.path.dirname(os.path.realpath(__file__))
        logging.info(dirpath)
        parent_path   = os.path.abspath(os.path.join(dirpath, ".."))
        logging.info(parent_path)

        


if __name__ == '__main__':
    dir = TestDir()
    # dir.test_path()
    dir.test_parentpath()
