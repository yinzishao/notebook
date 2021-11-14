#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Youmi
# @author yinzishao@youmi.net
# https://leetcode-cn.com/problems/number-of-1-bits/

"""
编写一个函数，输入是一个无符号整数，返回其二进制表达式中数字位数为 ‘1’ 的个数（也被称为汉明重量）。

https://baike.baidu.com/item/%E8%A1%A5%E7%A0%81/6854613?fromtitle=%E4%BA%8C%E8%BF%9B%E5%88%B6%E8%A1%A5%E7%A0%81&fromid=5295284

时钟的计量范围是0～11，模=12
n位的计算机计量范围是0～2^(n)-1，模=2^(n)
8位二进制系统的模为2^8

补码：
在以12模的系统中，加8和减4效果是一样的，因此凡是减4运算，都可以用加8来代替。对“模”而言，8和4互为补数。

通俗易懂https://blog.csdn.net/zl10086111/article/details/80907428


10-4=6；另一种是顺拨8小时：10+8=12+6=6
利用模，将减法变成加法， 刚好去掉最高位去摸

注意，Python的int python是int类型是无精度类型,无限宽度，不会发生溢出而进行截取的情况
"""


# ！： 将 n 和 n−1 做与运算，会把最后一个 1 的位变成 0
class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        count = 0
        while n:
            count += 1
            n = n & n - 1
        return count

