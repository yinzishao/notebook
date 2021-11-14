#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
题目:输入一个整数数组,实现一个函数来调整该数组中数字的顺序使得所有奇数位于数组的前半部分,所有偶数位于数组的后半部分。

前后两个指针，然后第一个指针是偶数，第二个指针是奇数的时候进行交换。结束条件是相遇
"""
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

beg = 0
end = len(a) - 1
while beg < end:

    while a[beg] % 2 == 1:
        beg += 1
    while a[end] % 2 == 0:
        end -= 1
    if beg < end:
        a[beg], a[end] = a[end], a[beg]
        beg += 1
        end -= 1

print(a)
