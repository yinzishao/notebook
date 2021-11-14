#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Youmi
# @author yinzishao@youmi.net
# https://leetcode-cn.com/problems/permutations/

#
# 做的是 1到n位最大数的题目 面试题 12的题目

# class Solution(object):
#     def permute(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[List[int]]
#         """
#         result = []
#
#         for i in nums:
#             a = [i]
#             self.red(a, nums, 1, result)
#         print(result)
#
#     def red(self, l, nums, idx, result):
#         if idx >= len(nums):
#             result.append(l)
#         else:
#             for i in nums:
#                 b = l.copy()
#                 b.append(i)
#                 self.red(b, nums, idx + 1, result)
#
# print(Solution().permute([1,2,3]))

# 回溯法
# 第一个数，跟所有数交换，
# 然后，往下走，第二个数跟 第二以后的数交换
# 最后完成后，交换回来。可以理解子模式，首位依次是各位，子问题往下走。而交换让2去到1需要1回到2，后让3跟1交换。后子问题往下走


class Solution:
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def backtrack(first=0):
            # if all integers are used up
            if first == n:
                output.append(nums[:])
            for i in range(first, n):
                # place i-th integer first
                # in the current permutation
                nums[first], nums[i] = nums[i], nums[first]
                # use next integers to complete the permutations
                backtrack(first + 1)
                # backtrack
                nums[first], nums[i] = nums[i], nums[first]

        n = len(nums)
        output = []
        backtrack()
        return output


print(Solution().permute([1, 2, 3]))
