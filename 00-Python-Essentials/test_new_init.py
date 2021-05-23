#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/5/23 11:12
# @Author:  hiyongz
# @File:    test_new_init.py

# __new__和__init__
# https://zhuanlan.zhihu.com/p/35943253
class Person():
    def __new__(cls, *args, **kwargs):
        # print(cls)
        print("__new__ is called")
        return object.__new__(cls)

    def __init__(self,name,age):
        print("__init__ is called")
        self.name = name
        self.age = age

class Singleton(object):
    # 单例模式
    print("__new__ is called")
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance
    def __init__(self,name,age):
        print("__init__ is called")
        self.name = name
        self.age = age

class Fruit(object):
    def __init__(self):
        pass

    def print_color(self):
        pass

class Apple(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("apple is in red")

class Orange(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("orange is in orange")

class FruitFactory(object):
    fruits = {"apple": Apple, "orange": Orange}

    def __new__(cls, name):
        if name in cls.fruits.keys():
            return cls.fruits[name]()
        else:
            return Fruit()



if __name__ == '__main__':
    # p1 = Person("zhangsan",26)
    # print(p1)
    # print(p1.name)
    # p2 = Person("lishi",25)
    # print(p2)
    # print(p2.name)

    # p1 = Singleton("zhangsan",26)
    # print(p1)
    # print(p1.name)
    # p2 = Singleton("lishi", 25)
    # print(p2)
    # print(p2.name)

    fruit1 = FruitFactory("apple")
    fruit2 = FruitFactory("orange")
    fruit1.print_color()
    fruit2.print_color()