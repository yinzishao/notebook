#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/
输入一个整型数组，数组里有正数也有负数。数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。

要求时间复杂度为O(n)。

"""

"""
# 狗屎
class Solution:
    def maxSubArray(self, nums):

        result = nums[0]
        rc = result
        for i in nums[1:]:
            # 应该是上一次的结果出发进行判断，如果上一次结果是大于0的，沿用。否则则为当前的值。然后比较当前的累加是否大于以往最大值
            rc = rc + i
            if rc > 0:
                if rc > result:
                    result = rc
            else:
                rc = 0
        return result
"""


class Solution:
    def maxSubArray(self, nums):
        cn = 0
        mn = nums[0]
        for i in nums:
            if cn <= 0:
                cn = i
            else:
                cn += i
            if cn >= mn:
                mn = cn
        return mn


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
arr = [-1]
arr = [-2, 1]

print(Solution().maxSubArray(arr))
