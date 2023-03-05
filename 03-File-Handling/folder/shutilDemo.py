# -*-coding:utf-8-*-
# @Time:    2021/9/26 16:21
# @Author:  haiyong
# @File:    test_folder.py
import os
import sys
import logging
import shutil


class TestDir():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(name)s - %(asctime)s - %(message)s', datefmt='%Y%m%d-%H:%M:%S')

    def test_copyfileobj(self):
        sourcefile = open('test.txt', 'r')
        destfile   = open('file_copy.txt','w')
        shutil.copyfileobj(sourcefile, destfile) 
        sourcefile.close()
        destfile.close()

    def test_copyfile(self):
        dirpath    = os.path.dirname(os.path.realpath(__file__))
        sourcedir  = os.path.join(dirpath, "shutil_a")
        sourcefile = os.path.join(dirpath, "shutil_a", "test.txt")        
        destdir    = os.path.join(dirpath, "shutil_b")
        destfile   = os.path.join(dirpath, "shutil_b", "test2.txt")
        # 复制文件或目录
        shutil.copy(sourcefile, destdir)        
        # 复制文件
        shutil.copyfile(sourcefile, destfile) 
        # 复制目录
        shutil.copytree(sourcedir, destdir, dirs_exist_ok=True) 

    def test_move(self):
        dirpath    = os.path.dirname(os.path.realpath(__file__))
        sourcedir  = os.path.join(dirpath, "shutil_a")
        sourcefile = os.path.join(dirpath, "shutil_a", "test.txt")        
        destdir    = os.path.join(dirpath, "shutil_b")
        # shutil.move(sourcefile, destdir)
        # shutil.move(destdir, sourcedir)
        shutil.move(sourcedir, destdir)

    def test_remove(self):
        dirpath    = os.path.dirname(os.path.realpath(__file__))     
        destdir    = os.path.join(dirpath, "shutil_b")
        shutil.rmtree(destdir)

    def test_archive(self):
        # root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
        # logging.info(root_dir)
        # logging.info(shutil.get_archive_formats())
        dirpath    = os.path.dirname(os.path.realpath(__file__))
        archive_name  = os.path.join(dirpath, "shutil_a")
        root_dir = archive_name
        shutil.make_archive(archive_name, 'zip', root_dir)

    def test_unpack_archive(self):
        dirpath      = os.path.dirname(os.path.realpath(__file__))
        archive_name = os.path.join(dirpath, "shutil_a.zip")
        extract_dir  = os.path.join(dirpath, "shutil_a")   
        shutil.unpack_archive(archive_name, extract_dir, 'zip')
     


if __name__ == '__main__':
    dir = TestDir()
    # dir.test_copyfile()
    dir.test_move()
    # dir.test_archive()
    # dir.test_unpack_archive()
