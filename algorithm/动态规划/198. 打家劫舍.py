"""
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

示例 1：

输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/house-robber
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 2:
            return max(nums[0], nums[1])
        dp = [nums[0], nums[1]]
        result = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            cur = max(dp[i - 1], dp[i - 2] + nums[i])
            dp.append(cur)
            if cur > result:
                result = cur
        return result


n = [2, 7, 9, 3, 1]
print(Solution().rob(n))


class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        # 长度2不需要在判断了
        # if len(nums) == 2:
        #     return max(nums[0], nums[1])

        # 最后肯定是最大
        # result = max(nums[0], nums[1])
        # nums[1] = result
        nums[1] = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            # cur = max(nums[i-1], nums[i-2] + nums[i])
            # nums[i] = cur
            # if cur > result:
            #     result = cur
            nums[i] = max(nums[i - 1], nums[i - 2] + nums[i])
        return nums[-1]


n = [2, 7, 9, 3, 1]
print(Solution().rob(n))
n = [2, 1, 1, 2]
print(Solution().rob(n))
