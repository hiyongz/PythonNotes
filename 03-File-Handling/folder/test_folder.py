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

    def test_dirfile(self):
        for root, dirs, files in os.walk(os.getcwd()):
            print(root)
            print(dirs)
            print(files)
            print("#" * 20)
        print(os.listdir(os.getcwd()))

if __name__ == '__main__':
    file = TestFile()
    # file.test_path()
    # file.create_file()
    file.file_split()
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

    # dir = TestDir()
    # # dir.test_path()
    # dir.test_dirfile()
