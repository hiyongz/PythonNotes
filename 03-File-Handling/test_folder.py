#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os
import sys


class TestDir():
    def test_path(self):
        # 获取当前文件__file__的路径
        print(__file__)
        print(sys.argv[0])
        print(os.path.realpath(__file__))
        print(os.path.abspath(sys.argv[0]))
        print("#" * 20)

        # 获取当前文件__file__的所在目录
        print(os.getcwd())
        print(os.path.dirname(os.path.realpath(__file__)))
        print(os.path.split(os.path.realpath(__file__))[0])
        path = os.path.dirname(os.path.realpath(__file__))

        # 获取当前文件名名称
        print("#" * 20)
        print(os.path.basename(sys.argv[0]))  # 当前文件名名称
        print(os.path.basename(__file__))  # 当前文件名名称
        filename = os.path.basename(__file__)

        # 拼接路径
        abspath = os.path.join(path, filename)
        print(abspath)

        # 创建目录
        if not os.path.exists(path):
            print(f"创建文件: {path}")
            os.makedirs(path)


class TestFile(TestDir):
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))

    def create_file(self):
        # 创建文件：创建一个txt文件
        text = "Hello World!\n你好，世界！"
        self.newfilepath = os.path.join(self.path, "newfile.txt")
        file = open(self.newfilepath, 'w')
        file.write(text)  # 写入内容信息
        file.close()

    def file_exists(self):
        # 判断文件是否存在
        print("#" * 20)
        print("判断文件是否存在")
        print(os.path.isfile(self.path))
        print(os.path.isfile(self.newfilepath))
        print(os.path.exists(self.newfilepath))

    def file_access(self):
        # 判断文件属性
        print("判断文件属性")
        print(os.access(self.newfilepath, os.F_OK))  # 文件是否存在
        print(os.access(self.newfilepath, os.R_OK))  # 文件是否可读
        print(os.access(self.newfilepath, os.W_OK))  # 文件是否可以写入
        print(os.access(self.newfilepath, os.X_OK))  # 文件是否有执行权限

    def open_file_a(self):
        # 打开存在的文件，追加操作，不会覆盖先前文件中的内容。
        # file = open(self.newfilepath, 'a')
        file = open("123.txt", 'a')
        text = "new line"
        file.write(text)  # 追加内容
        file.close()

    def open_file_x(self):
        # 创建新文件，写操作，使用此模式打开存在的文件会抛出异常。
        file = open("test_x.txt", 'x')
        text = "new line"
        file.write(text)  # 追加内容
        file.close()

    def open_file_r_plus(self):
        # 读、写操作，不会覆盖先前文件中的内容。
        file = open(self.newfilepath, 'r+')
        text = "new line"
        file.write(text)  # 追加内容
        print(file.read())
        file.close()

    def open_file_w_plus(self):
        # 写、读操作，会覆盖先前文件中的内容。
        file = open(self.newfilepath, 'w+')
        print(file.read())
        text = "new line"
        file.write(text)  # 追加内容
        file.close()

    def open_file_a_plus(self):
        # 追加、读操作，不会删除和覆盖先前文件中的内容。
        file = open(self.newfilepath, 'a+')
        # print(file.read())
        text = "new line"
        file.write(text)  # 追加内容
        file.close()

    def open_file_x_plus(self):
        # 创建新文件，读写操作。
        file = open("test_x2.txt", 'x+')
        print(file.read())
        text = "new line"
        file.write(text)  # 追加内容
        file.close()

    def read_file(self):
        # 打开并读取文件
        file = open(self.newfilepath, 'r')
        print(file.read())  # read()执行完后，文本的光标会移动到最后，再次读取file需要将光标移到前面

        file.seek(0, 0)
        for line in file:
            print(line)
        file.close()

    def read_file2(self):
        # 打开并读取文件
        file = open(self.newfilepath, 'r')
        text = file.read()
        print(text)
        for line in text:
            print(line)
        file.close()






if __name__ == '__main__':
    file = TestFile()
    file.test_path()
    file.create_file()
    file.file_exists()
    file.file_access()
    # file.read_file()
    # file.read_file2()
    file.open_file_a()
    # file.open_file_x()
    # file.open_file_r_plus()
    # file.open_file_w_plus()
    # file.open_file_a_plus()
    # file.open_file_x_plus()
