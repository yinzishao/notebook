"""
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。



示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List


class Solution:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        for idx, v in enumerate(nums):
            for idx_2 in range(idx+1, len(nums)):
                if v + nums[idx_2] == target:
                    return [idx, idx_2]


class SolutionDict:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for idx, v in enumerate(nums):
            # 数组元素允许一样，处理重复场景
            if v in d and 2*v == target:
                return [d[v], idx]
            d[v] = idx
        for n in nums:
            t = target - n
            # 需要注意单个元素重复计算的问题
            if t != n and t in d:
                return [d[n], d[target-n]]


class SolutionDict:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        # 不像上面那样先生成字典就思路简单很多也少一个for循环！
        # 不需要注意单个元素重复计算的问题
        for i, n in enumerate(nums):
            t = target - n
            if t in d:
                return [d[t], i]
            d[n] = i


nums = [2, 7, 11, 15]
target = 9
result = Solution().two_sum(nums, target)
assert result == [0, 1]
print(result)

nums = [3, 2, 4]
target = 6
result = SolutionDict().two_sum(nums, target)
assert result == [1, 2]
print(result)

nums = [3, 3]
target = 6
result = SolutionDict().two_sum(nums, target)
assert result == [0, 1]
print(result)

nums = [3, 2, 3]
target = 6
result = SolutionDict().two_sum(nums, target)
assert result == [0, 2]
print(result)


