"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

注意：给定 n 是一个正整数。

示例 1：

输入： 2
输出： 2
解释： 有两种方法可以爬到楼顶。
1.  1 阶 + 1 阶
2.  2 阶

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/climbing-stairs
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


# 递归
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)


print(Solution().climbStairs(5))


# 迭代： 动态规划. o(n)空间
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = []
        for i in range(n + 1):
            if i == 0:
                dp.append(1)
            elif i == 1:
                dp.append(1)
            else:
                dp.append(dp[i - 1] + dp[i - 2])
        return dp[-1]


print(Solution().climbStairs(5))


# 斐波那契数列 notebook/algorithm/fib.py
class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 0, 1
        while n > 0:
            a, b = b, a + b
            n -= 1
        return b


print(Solution().climbStairs(5))
