# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os
import sys

class TestFile():
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

    def file_split(self):
        # 读取文件名称和后缀
        # fname, fextension = os.path.splitext(self.newfilepath)
        fname, fextension = os.path.splitext("D:\\newfile.txt")
        print(fname)
        print(fextension)

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



    def write_file(self):
        # 写文件
        file = open("newfile.txt", 'w')
        text1 = "Hello World!\n你好，世界！\r"
        file.write(text1)  # 写入内容信息

        text2 = ["To the time to life, \n", "rather than to life in time.\r"]
        file.writelines(text2)

        file.close()

    def read_file(self):
        # 打开并读取文件
        file = open(self.newfilepath, 'r')

        for line in file:
            print(line)
        print()

        file.seek(0, 0)
        print(file.read(5))  # read()执行完后，文本的光标会移动到最后，再次读取file需要将光标移到前面
        print()

        file.seek(0, 0)
        print(file.readline(12))
        print()

        file.seek(0, 0)
        print(file.readlines())
        print()

        file.close()

    def delete_file(self):
        os.remove("D:/ProgramWorkspace/PythonNotes/03-File-Handling/folder/test1.txt")
        os.unlink("D:/ProgramWorkspace/PythonNotes/03-File-Handling/folder/test2.txt")


    def with_statement(self):
        text1 = "Hello World!\n你好，世界！\r"
        text2 = ["To the time to life, \n", "rather than to life in time.\r"]
        # 写
        with open("newfile.txt", "w") as file:
            file.write(text1)
            file.writelines(text2)

        # 读
        with open("newfile.txt", "r+") as file:
            print(file.read())


if __name__ == '__main__':
    file = TestFile()
    # file.create_file()
    # file.file_split()
    # file.file_exists()
    # file.file_access()
    # file.open_file_a()
    # file.open_file_x()
    # file.open_file_r_plus()
    # file.open_file_w_plus()
    # file.open_file_a_plus()
    # file.open_file_x_plus()
    # file.write_file()
    # file.read_file()
    # file.with_statement()
    file.delete_file()

