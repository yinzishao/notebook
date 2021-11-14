"""
峰值元素是指其值大于左右相邻值的元素。

给你一个输入数组nums，找到峰值元素并返回其索引。数组可能包含多个峰值，在这种情况下，返回 任何一个峰值 所在位置即可。

你可以假设nums[-1] = nums[n] = -∞ 。



示例 1：

输入：nums = [1,2,3,1]
输出：2
解释：3 是峰值元素，你的函数应该返回其索引 2。
示例2：

输入：nums = [1,2,1,3,5,6,4]
输出：1 或 5
解释：你的函数可以返回索引 1，其峰值元素为 2；
    或者返回索引 5， 其峰值元素为 6。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-peak-element
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

提示：
1 <= nums.length <= 1000
-231 <= nums[i] <= 231 - 1
对于所有有效的 i 都有 nums[i] != nums[i + 1]

"""
from typing import List


class Solution:
    """太复杂了，错误思路和代码"""

    def findPeakElement(self, nums: List[int]) -> int:
        return self.parti(nums, 0, len(nums) - 1)

    def parti(self, nums, start, end):
        if start > end:
            return end
        # TODO：越界问题
        mid = (start + end) // 2
        # 相等的情况？ 根据提示不存在该情况
        if (
            mid - 1 < start or nums[mid - 1] < nums[mid]
        ) and (
            mid + 1 > end or nums[mid] < nums[mid + 1]
        ):
            return self.parti(nums, mid + 1, end)
        elif (
            mid - 1 < start or nums[mid - 1] > nums[mid]
        ) and (
            mid + 1 > end or nums[mid] > nums[mid + 1]
        ):
            return self.parti(nums, start, mid - 1)
        else:
            return mid


# 失败
# res = Solution().findPeakElement([1, 2, 3, 1])
# assert res == 2, res
#
# res = Solution().findPeakElement([1, 2])
# assert res == 1, res

"""
方法二：递归二分查找
题解：

因为总会有一个峰值的，我们判断判断的时候，无须立刻比较左右两边，立刻得到峰值，而是通过递归的思路，化为相同的子问题，让递归结束后，自然而然成为结果

而越界问题，[0, 1] ， 中间值拿的是下标1, 当上升的时候，直接mid赋值为开始，而下降的时候，要让mid-1, 这样才能避免死循环

public class Solution {
    public int findPeakElement(int[] nums) {
        return search(nums, 0, nums.length - 1);
    }
    public int search(int[] nums, int l, int r) {
        if (l == r)
            return l;
        int mid = (l + r) / 2;
        if (nums[mid] > nums[mid + 1])
            return search(nums, l, mid);
        return search(nums, mid + 1, r);
    }
}

作者：LeetCode
链接：https://leetcode-cn.com/problems/find-peak-element/solution/xun-zhao-feng-zhi-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""


class Solution:

    def findPeakElement(self, nums: List[int]) -> int:
        return self.search(nums, 0, len(nums) - 1)

    def search(self, nums, start, end):
        if start == end:
            return start
        mid = int((start + end) / 2) + 1
        if nums[mid] > nums[mid - 1]:
            # 上升趋势
            return self.search(nums, mid, end)
        else:
            return self.search(nums, start, mid - 1)


res = Solution().findPeakElement([1, 2, 3, 1])
assert res == 2, res

res = Solution().findPeakElement([1, 2])
assert res == 1, res

"""
方法三：迭代二分查找

"""


class Solution:

    def findPeakElement(self, nums: List[int]) -> int:
        s, e = 0, len(nums) - 1,
        while s < e:
            # mid，偶数的时候往左边靠
            mid = int((s + e) / 2)
            if nums[mid] > nums[mid + 1]:
                # 下降
                e = mid
            else:
                # 上升， mid不可能是峰值
                s = mid + 1
        return s


res = Solution().findPeakElement([1, 2, 3, 1])
assert res == 2, res

res = Solution().findPeakElement([1, 2])
assert res == 1, res
