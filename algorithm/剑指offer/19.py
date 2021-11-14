#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
二叉树，输出它的镜像
前序节点递归

左节点跟右节点交换，
后递归左右节点下去

"""

"""
顺时针打印矩阵

一开始只想怎么打印顺时针，没有想清楚结束的条件
"""
foo = [
    [1, 2, 3, 4, 5, 6],
    [5, 6, 7, 8, 9, 10],
    [9, 10, 11, 12, 13, 14],
    [13, 14, 15, 16, 17, 18]
]
#
# foo = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ]
foo = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]


class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        if not matrix:
            return []
        width = len(matrix)
        length = len(matrix[0])
        total = width * length
        a, b, c, d = 0, length - 1, 0, width - 1
        result = []
        while True:
            # 顺时针的打印
            for i in range(c, b+1):
                result.append(matrix[a][i])
            a += 1
            if len(result) == total:
                break

            for i in range(a, d+1):
                result.append(matrix[i][b])
            b -= 1
            if len(result) == total:
                break

            for i in range(c, b+1)[::-1]:
                result.append(matrix[d][i])
            d -= 1
            if len(result) == total:
                break

            for i in range(a, d+1)[::-1]:
                result.append(matrix[i][c])
            c += 1
            if len(result) == total:
                break

        return result


print(Solution().spiralOrder(foo))

"""

https://leetcode-cn.com/problems/spiral-matrix/solution/cxiang-xi-ti-jie-by-youlookdeliciousc-3/

这里的方法不需要记录已经走过的路径，所以执行用时和内存消耗都相对较小

首先设定上下左右边界
其次向右移动到最右，此时第一行因为已经使用过了，可以将其从图中删去，体现在代码中就是重新定义上边界
判断若重新定义后，上下边界交错，表明螺旋矩阵遍历结束，跳出循环，返回答案
若上下边界不交错，则遍历还未结束，接着向下向左向上移动，操作过程与第一，二步同理
不断循环以上步骤，直到某两条边界交错，跳出循环，返回答案

其实跟我的思路是一样的，只是没有想清楚怎么结束！！

之前单纯的想左小于右，上小于下就结束了，但是还是会在循环里面进行跑，
所以应该是while true 在在每一次的循环遍历后去判断是否有交错，但是判断条件是大于等于，而不是大于！！！看到不对，没有坚持想下去，就只能暴力根据长度去判断了！fuck

至于为什么是大于等于，原因是等于，也是代表下一次走的就是走过的了？想错了。你的等于是基于加的行，不是走过的！

"""


# 我的版本：
def my_version():

    foo = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]

    matrix = foo
    width = len(matrix)
    length = len(matrix[1])
    a, b, c, d = 0, length - 1, 0, width - 1
    result = []
    while True:
        # 顺时针的打印
        for i in range(c, b+1):
            result.append(matrix[a][i])
        a += 1
        if a > d:
            break

        for i in range(a, d+1):
            result.append(matrix[i][b])
        b -= 1
        if b < c:
            break

        for i in range(c, b+1)[::-1]:
            result.append(matrix[d][i])
        d -= 1
        if d < a:
            break

        for i in range(a, d+1)[::-1]:
            result.append(matrix[i][c])
        c += 1
        if c > b:
            break

    print(result)