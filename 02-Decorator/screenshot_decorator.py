#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/12/7 19:57
# @Author:  hiyongz
# @File:    screenshot_decorator.py
import time


class Screenshot(object):
    def __init__(self,data):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("66666666")
            print(args)
            print(kwargs)
            print("66666666")
            try:
                res = func(*args, **kwargs)
                return func(*args, **kwargs)
            except:
                now_time = time.strftime('%Y_%m_%d_%H_%M_%S')  # 异常时，截图
                self.capture_screenshot(f'{now_time}.png')
                raise  # 抛出异常，不然会认为测试用例执行通过

        return wrapper

    def capture_screenshot(self, filename='facebookwda-screenshot-{index}.png'):
        print(filename)
        # path, link = self._get_screenshot_paths(filename)
        # self._create_directory(path)
        # self.d.screenshot().save(path)
        # self._html('</td></tr><tr><td colspan="3"><a href="%s">'
        #            '<img src="%s" width="400px"></a>' % (link, link))


class Demo():
    @Screenshot(1)
    def test1(self,data1,data2):
        print("test1 begin")
        # assert 1 + 1 == 6
        try:
            assert 1 + 1 == 6
        except:
            print("error")


if __name__ == '__main__':
    d = Demo()
    d.test1(2,3)
