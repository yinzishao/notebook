"""

给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

请你设计并实现时间复杂度为O(n) 的算法解决此问题。



示例 1：

输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
示例 2：

输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-consecutive-sequence
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        d = {i: -1 for i in nums}
        result = 0
        for i in nums:
            leng = 1
            if d[i] == -1:
                # 向左遍历找出最前的递增起始
                left = i
                while left - 1 in d:
                    leng += 1
                    left -= 1
                    d[left] = 1
                right = i
                while right + 1 in d:
                    leng += 1
                    right += 1
                    d[right] = 1
                result = max(leng, result)
        return result


n = [100, 4, 200, 1, 3, 2]

assert Solution().longestConsecutive(n) == 4
n = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
assert Solution().longestConsecutive(n) == 9

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/longest-consecutive-sequence/solution/zui-chang-lian-xu-xu-lie-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

不需要字典，一个set 就可以了

题解的意思是直接找出第一个开头，然后遍历到最后，这样就不需要上面我的思路做标识和左右遍历了!

"""


class Solution:
    def longestConsecutive(self, nums):
        longest_streak = 0
        num_set = set(nums)

        for num in num_set:
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                longest_streak = max(longest_streak, current_streak)

        return longest_streak
