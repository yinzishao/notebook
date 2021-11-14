#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

注意点：
1. n过大导致数值溢出，故用字符
2. 如何判断结束，对比99..9效率过低，+1 第一位产生进位来判断


思路，从末尾遍历，+1 如果不超过10，则结束。如果超过10， 则保留+1用作上一位+1。-10替代当前位，后继续遍历


另一个思路：
补0到长度，全排列
递归思路： 从数组左边0开始遍历，代表最左边，会从0变化到9,
然后循环中，递归到下一个index。同样处理，从0变化到9
。。。
直到找到最后一位，0开始执行，后递归回去。保留很多堆栈信息。

"""
a = [0, 0, 0, 0]
length = len(a)


def m():
    for i in range(0, 10):
        a[0] = i
        b(0, i)


def b(idx, t):
    if idx + 1 == length:
        print(a)
        return
    for i in range(0, 10):
        a[idx + 1] = i  # 这一位从0到9
        b(idx + 1, i)  # 递归到下一位从0到9

# m()
# 上面简化成下面


def foo(idx=0):
    if idx == length:
        print(a)
        return
    for i in range(0, 10):
        a[idx] = i
        foo(idx+1)

foo()