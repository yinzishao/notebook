"""
给定一个三角形 triangle ，找出自顶向下的最小路径和。

每一步只能移动到下一行中相邻的结点上。相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/triangle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

"""
自己的写法：
    dp[i] = min(dp[i-1], dp[i]) + cur_val
    从上往下遍历，麻烦在需要知道当前遍历的位置，因为需要确定上一次dp中的位置。
    如果当前位置是0,则上一轮的0,如果是最后了，则拿上一轮的最后，否则拿上一轮位置的-1和当前位置的最小值
"""


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        dp = [triangle[0]]
        for first_idx in range(1, len(triangle)):
            dp.append([])
            for second_idx in range(len(triangle[first_idx])):
                if second_idx == 0:
                    min_dp = dp[first_idx - 1][0]
                elif second_idx == first_idx:
                    min_dp = dp[first_idx - 1][second_idx - 1]
                else:
                    min_dp = min(dp[first_idx - 1][second_idx - 1], dp[first_idx - 1][second_idx])
                dp[first_idx].append(min_dp + triangle[first_idx][second_idx])
        return min(dp[-1])


print(Solution().minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))

"""
优化点：
在我们自顶向下的过程中，其实我们只需要使用到上一层中已经累积计算完毕的数据，并且不会再次访问之前的元素数

直接覆盖在传入参数上
"""


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        for first_idx in range(1, len(triangle)):
            for second_idx in range(len(triangle[first_idx])):
                if second_idx == 0:
                    min_dp = triangle[first_idx - 1][0]
                elif second_idx == first_idx:
                    min_dp = triangle[first_idx - 1][second_idx - 1]
                else:
                    min_dp = min(triangle[first_idx - 1][second_idx - 1], triangle[first_idx - 1][second_idx])
                triangle[first_idx][second_idx] = min_dp + triangle[first_idx][second_idx]
        return min(triangle[-1])


print(Solution().minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))

"""
用一个dp一维数组的做法
# dp当前数组如果从左往右遍历，会覆盖之前的。
# 所以我们从后面遍历,覆盖的也不会用到了

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/triangle/solution/san-jiao-xing-zui-xiao-lu-jing-he-by-leetcode-solu/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)
        f = [0] * n
        f[0] = triangle[0][0]

        # !: 简洁明了很多！
        for i in range(1, n):
            # dp当前数组如果从左往右遍历，会覆盖之前的。
            # 所以我们从后面遍历,覆盖的也不会用到了
            f[i] = f[i - 1] + triangle[i][i]
            for j in range(i - 1, 0, -1):
                f[j] = min(f[j - 1], f[j]) + triangle[i][j]
            # 0下标是不在上面的遍历中的
            f[0] += triangle[i][0]
        # 优化，直接覆盖原数组
        return min(f)


print(Solution().minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))
