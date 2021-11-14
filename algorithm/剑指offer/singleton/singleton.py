#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
1. 通过__new___和hasattr进行判断， 主要语句：cls._instance = super().__new__(cls)
2. 通过装饰器进行实现，设立一个字典，判断是否存在，存在则直接获取
3. 装饰器加上线程锁


__new__方法

使用类名（）创建对象的时候，python解释器首先会调用__new__方法为对象分配空间

__new__是一个由object基类提供的内置的静态方法，主要作用有两个：
1.在内存中为对象分配空间
2.返回对象的引用

python解释器获得对象的引用后，将引用作为第一个参数，传递给__init__方法
原文链接：https://blog.csdn.net/fjswcjswzy/article/details/105637086

"""
# ref: https://blog.csdn.net/qq_33733970/article/details/78792656


print('hasattr --------------')


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, a):
        self.a = a


s0 = Singleton(a=1)
s1 = Singleton(a=2)
print(s0.a)
print(s1.a)
print(id(s0))
print(id(s1))
print('hasattr --------------')

from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class Bar:

    def __init__(self, a):
        self.a = a

b0 = Bar(1)
b1 = Bar(2)
print(id(b0))
print(id(b1))

# 线程安全
#  https://stackoverflow.com/a/50567397
#  https://blog.csdn.net/lucky404/article/details/79668131

print('-' * 30)
import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


class Singleton:
    """
    单例模式
    """
    instance = None

    @synchronized
    # def __new__(cls):
    def __new__(cls, *args, **kwargs):
        # TypeError: __new__() got an unexpected keyword argument 'a'
        _ = args, kwargs
        if cls.instance is None:
            # TypeError: object.__new__() takes exactly one argument (the type to instantiate)
            # cls.instance = super().__new__(cls, *args, **kwargs)
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.a = kwargs['a']
        print(args, kwargs, self.a)


s0 = Singleton(a=1)
s1 = Singleton(a=2)
# all print are 2
print(s0.a)
print(s1.a)
print(id(s0))
print(id(s1))
