#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array-ii/


class Solution(object):
    def findMin(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return None
        length = len(nums)
        if length == 1:
            return nums[1]
        else:
            start = 0
            end = length - 1
            while True:
                # [1, 2, 3] 不能等于 [1, 1, 0, 1]
                if nums[start] < nums[end]:
                    return nums[start]
                mid = (start + end + 1) // 2
                if end == mid:
                    return nums[mid]
                if nums[mid] > nums[start]:
                    start = mid + 1
                elif nums[mid] < nums[start]:
                    end = mid
                else:
                    return min(nums)

print(Solution().findMin([4, 5, 6, 7, 1, 2, 3]))

#
# https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array-ii/solution/154-find-minimum-in-rotated-sorted-array-ii-by-jyd/
# 这个解题思路跟我想的相反，是用最后去比较，这样好处是也能符合顺序的数组检查
# 而且这个判断，直接也能递归最终结果. 为什么？如何想？ 主要是这样想：
# 顺序的，中间比前面大，往前区间拿
# 旋转的，如果中间跟开始的数比较，如果中间比开始大，反而要拿后区间，跟顺序规则不同，导致需要独立处理。
# 如果中间跟结束的数比较，如果中间比结束小，拿后区间，跟顺序规则相同，故能一起处理


class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            # [3, 1] 3跟1比较，然后+1，递归到最后结果
            if nums[mid] > nums[right]: left = mid + 1

            elif nums[mid] < nums[right]: right = mid
            else: right = right - 1 # key
        return nums[left]

