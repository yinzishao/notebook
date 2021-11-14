"""

给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。


示例 1：

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-subarray
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

"""
因为是连续的: 当前元素的最大值为其(上一个元素+当前元素)和当前元素的最大值
"""


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [nums[0]]
        result = nums[0]
        for idx, v in enumerate(nums[1:]):
            # 可以理解为，如果上一个元素>0则加上
            # 偷懒了，不能用max
            dpv = max(dp[idx] + v, v)
            dp.append(dpv)
            result = max(dpv, result)
        # ！：不能用max，直接通过在循环里面比较结果得到最大
        return result


print(Solution().maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return
        res = nums[0]
        s = nums[0]
        for i in nums[1:]:
            if s > 0:
                s += i
            else:
                s = i
            res = max(s, res)
        return res


print(Solution().maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
