#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
编写一个高效的算法来判断 m x n 矩阵中，是否存在一个目标值。该矩阵具有如下特性：

每行中的整数从左到右按升序排列。
每行的第一个整数大于前一行的最后一个整数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/search-a-2d-matrix
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

leetcode的解法1： 二维看成递增的一维数组，进行二分查找

剑指offer的不是有序递增的，故不能
剑指offer解法： 右上方获取值，比较。若大于比较值，则删除列，若小于，删除行。

"""
# 剑指offer跟leetcode题目有点不一样


class Solution(object):
    def searchMatrix(self):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        matrix = [
              [1,   3,  5,  7],
              [10, 11, 16, 20],
              [23, 30, 34, 50]
            ]
        target = 3
        if not matrix:
            return False
        width = len(matrix) - 1
        length = len(matrix[0]) - 1
        while not(width < 0 or length < 0) and width < len(matrix) and length < len(matrix[0]):
            tmp = matrix[width][length]
            if target == tmp:
                return True
            elif target < tmp:
                # target是3的时候，往上比较超出范围了，注意边界的情况
                if width == 0:
                    length -= 1
                else:
                    width -= 1
            else:
                width += 1
                length -= 1
        return False


print(Solution().searchMatrix())
"""
执行结果：
通过
显示详情
执行用时 :
60 ms
, 在所有 Python 提交中击败了
94.28%
的用户
内存消耗 :
13.5 MB
, 在所有 Python 提交中击败了
43.70%
的用户

"""
