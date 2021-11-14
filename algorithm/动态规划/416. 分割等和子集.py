"""
给你一个 只包含正整数 的 非空 数组nums 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。



示例 1：

输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
示例 2：

输入：nums = [1,2,3,5]
输出：false
解释：数组不能分割成两个元素和相等的子集。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/partition-equal-subset-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

"""
转换思路：
给一个可装载重量为 sum / 2 的背包和 N 个物品，每个物品的重量为 nums[i]。现在让你装物品，是否存在一种装法，能够恰好将背包装满？

dp[i][j] = x 表示，对于前 i 个物品，当前背包的容量为 j 时，若 x 为 true，则说明可以恰好将背包装满，若 x 为 false，则说明不能恰好将背包装满。

"""


class Solution(object):
    def canPartition(self, nums):
        """
        dp[i][j] = x 表示，对于前 i 个物品，当前背包的容量为 j 时，若 x 为 true，则说明可以(不限制件数)恰好将背包装满，若 x 为 false，则说明不能恰好将背包装满。
        """
        s = sum(nums)
        if s % 2:
            return False
        w = int(s / 2)
        n = len(nums)
        result = []
        for i in range(0, n + 1):
            # 初始化，方便第一个装进的往前兼容。weigh=0为True
            result.append([True])
            for j in range(1, w + 1):
                result[i].append(False)
        for i in range(1, n + 1):
            for j in range(1, w + 1):
                c_w = nums[i - 1]
                # 如果当前物品的重量比背包容量还小，不能装进
                if j - c_w < 0:
                    result[i][j] = result[i - 1][j]
                else:
                    # 不装进或者装进
                    result[i][j] = result[i - 1][j] | result[i - 1][j - c_w]
        return result[n][w]


print(Solution().canPartition([1, 5, 11, 5]))
print(Solution().canPartition(
    [66, 90, 7, 6, 32, 16, 2, 78, 69, 88, 85, 26, 3, 9, 58, 65, 30, 96, 11, 31, 99, 49, 63, 83, 79, 97, 20, 64, 81, 80,
     25, 69, 9, 75, 23, 70, 26, 71, 25, 54, 1, 40, 41, 82, 32, 10, 26, 33, 50, 71, 5, 91, 59, 96, 9, 15, 46, 70, 26, 32,
     49, 35, 80, 21, 34, 95, 51, 66, 17, 71, 28, 88, 46, 21, 31, 71, 42, 2, 98, 96, 40, 65, 92, 43, 68, 14, 98, 38, 13,
     77, 14, 13, 60, 79, 52, 46, 9, 13, 25, 8]))


class SolutionOne(object):
    def canPartition(self, nums):
        """
        dp[i][j] = x 表示，对于前 i 个物品，当前背包的容量为 j 时，若 x 为 true，则说明可以(不限制件数)恰好将背包装满，若 x 为 false，则说明不能恰好将背包装满。
        注意这里是不限制件数的！这里只需要找不到是否能填满的情况就好了。
        """
        s = sum(nums)
        if s % 2:
            return False
        w = int(s / 2)
        n = len(nums)
        result = [True]
        for j in range(1, w + 1):
            result.append(False)
        # 上一个遍历的结果已经放在result里面了，所以可以通过result进行
        for i in range(0, n):
            # 后续遍历进行压缩
            for j in range(1, w + 1)[::-1]:
                c_w = nums[i]
                # 当背包的容量比当前的物品容量要大的时候
                # 结果应该为上一次该容量的结果（不装进）或者减去当前重量上一次物品的结果（装进）。
                if j - c_w >= 0:
                    result[j] = result[j] | result[j - c_w]
        return result[w]


print(SolutionOne().canPartition([1, 5, 11, 5]))
"""
注意： bad case 当背包容量是0的时候应该为true， 当物件为0的时候为false

题解：https://leetcode-cn.com/problems/partition-equal-subset-sum/solution/0-1-bei-bao-wen-ti-xiang-jie-zhen-dui-ben-ti-de-yo/
"""
