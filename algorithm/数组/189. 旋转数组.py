"""
给定一个数组，将数组中的元素向右移动 k 个位置，其中 k 是非负数。



进阶：

尽可能想出更多的解决方案，至少有三种不同的方法可以解决这个问题。
你可以使用空间复杂度为 O(1) 的 原地 算法解决这个问题吗？


示例 1:

输入: nums = [1,2,3,4,5,6,7], k = 3
输出: [5,6,7,1,2,3,4]
解释:
向右旋转 1 步: [7,1,2,3,4,5,6]
向右旋转 2 步: [6,7,1,2,3,4,5]
向右旋转 3 步: [5,6,7,1,2,3,4]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/rotate-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        length = len(nums)
        if k > length:
            # 右移会超过长度，取模
            k = k % length
        revert(nums, 0, length - 1)
        revert(nums, 0, k - 1)
        revert(nums, k, length - 1)


def revert(nums, l, r):
    """反转数组: 344"""
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1


n = [1, 2, 3, 4, 5, 6, 7]
Solution().rotate(n, 3)
print(n)

"""

我们从位置 00 开始，最初令 temp=nums[0]。根据规则，位置 00 的元素会放至 n(0+k) mod n 的位置，令 x=(0+k)modn，此时交换 temp 和 nums[x]，完成位置 xx 的更新。然后，我们考察位置 xx，并交换 temp 和 nums[(x+k) mod n]，从而完成下一个位置的更新。不断进行上述过程，直至回到初始位置 00。

容易发现，当回到初始位置 00 时，有些数字可能还没有遍历到，此时我们应该从下一个数字开始重复的过程，可是这个时候怎么才算遍历结束呢？

最大公约数

如果读者对上面的数学推导的理解有一定困难，也可以使用另外一种方式完成代码：使用单独的变量 count 跟踪当前已经访问的元素数量，当 count=n 时，结束遍历过程。


作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/rotate-array/solution/xuan-zhuan-shu-zu-by-leetcode-solution-nipk/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""
