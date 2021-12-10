#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/12/7 19:57
# @Author:  hiyongz
# @File:    screenshot_decorator.py
import time

def Screenshot(log_data=None):
    def Screenshot_decorator(func):
        def wrapper(self, *args, **kwargs):
            print("66666666")
            print(args)
            print(kwargs)
            print("66666666")
            try:
                res = func(self, *args, **kwargs)
                print(res)
                return func(self, *args, **kwargs)
            except:
                now_time = time.strftime('%Y_%m_%d_%H_%M_%S')  # 异常时，截图
                self.capture_screenshot(f'{now_time}.png')
                print(log_data)
                raise  # 抛出异常，不然会认为测试用例执行通过

        return wrapper
    return Screenshot_decorator

class Demo():
    def __init__(self, data):
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



    @Screenshot(log_data="运行失败")
    def test1(self, data1, data2):
        print("test1 begin")
        self.d = "666"
        assert 1 + 1 == 3
        # try:
        #     assert 1 + 1 == 6
        # except:
        #     print("error")


if __name__ == '__main__':
    d = Demo(1)
    d.test1(6,8)

    # d.test1(2, 3)
