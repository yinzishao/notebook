#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
单向链表中的倒数k个节点

一般思路，遍历一遍获取链表长度n。然后n-k+1获取到倒数k个节点的顺序，然后在遍历一遍链表，获取值

如何在遍历一遍获得？

两个指针，第一个指针先走k-1步，然后第二个指针和第一个指针一起走，到第一个指针结束，第二个指针则是所得。

需要考虑各种异常处理

"""


"""
16 反转链表

要保留现场，避免修改下一个指针的时候造成的断裂
"""

"""
17 合并两个有序链表成一个有序链表
"""

ma = [1, 3, 5, 7]
mb = [2, 4, 6, 8, 10]
mc = []


def merge(a, b):
    if not a:
        mc.extend(b)
        return b
    if not b:
        mc.extend(a)
        return a
    if a[0] < b[0]:
        mc.append(a[0])
        return merge(a[1:], b)
    else:
        mc.append(b[0])
        return merge(a, b[1:])

# merge(ma, mb)
# print(mc)


# 不需要在外面保存变量，利用递归的思想
def merge_without(a, b):

    if not a:
        mc.extend(b)
        return b
    if not b:
        mc.extend(a)
        return a
    c = []
    if a[0] < b[0]:
        c.append(a[0])
        c.extend(merge_without(a[1:], b))
    else:
        c.append(b[0])
        c.extend(merge_without(a, b[1:]))
    return c


print(merge_without(ma, mb))

