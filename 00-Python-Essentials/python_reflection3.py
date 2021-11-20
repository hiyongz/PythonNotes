#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/20 15:28
# @Author:  hiyongz
# @File:    python_reflection3.py

import inspect

class Demo():
    def __init__(self):
        self.person = Person()

    def get_function_attribute(self, name):
        print(dir(self.person))
        func = getattr(self.person, name)
        print(dir(func))

    def get_function_document(self, name):
        func = getattr(self.person, name)
        print(func.__doc__)

    def get_function_arguments(self, name):
        func = getattr(self.person, name)
        func("zhangsan", 18, height=175)
        print(dir(func.__code__))
        print(func.__defaults__)
        print("co_name: ", func.__code__.co_name)  # 返回函数名
        print("co_argcount: ", func.__code__.co_argcount)  # 返回函数的参数个数
        print("co_varnames: ",func.__code__.co_varnames) # 返回函数的参数
        print("co_filename: ", func.__code__.co_filename) # 返回文件绝对路径
        print("co_consts: ", func.__code__.co_consts)
        print("co_firstlineno: ",func.__code__.co_firstlineno) # 返回函数行号
        print("co_kwonlyargcount: ",func.__code__.co_kwonlyargcount) # 关键字参数
        print("co_nlocals: ",func.__code__.co_nlocals) # 返回局部变量个数

        # inspect.getargspec(func)
        argspec = inspect.getfullargspec(func)
        print(argspec.args)
        print(argspec.defaults)
        print(argspec.varkw)
        sig = inspect.signature(func)
        print(sig)
        funcArgs = func.__code__.co_varnames
        if funcArgs[0] == "self":
            funcArgs = funcArgs[1:]

        return funcArgs

class Person():
    def talk(self, name, age, height=None):
        """talk function
        :return:
        """
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print(inspect.getframeinfo(frame))
        print(f'function name: {inspect.getframeinfo(frame).function}')
        for i in args:
            print(f"{i} = {values[i]}")

        print(f"My name is {name}")
        print(f"My age is {age}")
        if height is not None:
            print(f"My height is {height}")

if __name__ == '__main__':
    # demo = Demo()
    # demo.get_function_attribute("talk")
    # demo.get_function_document("talk")
    # demo.get_function_arguments("talk")
    p = Person()
    p.talk("zhangsan", 18, height=175)


