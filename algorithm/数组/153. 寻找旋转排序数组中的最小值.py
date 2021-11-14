"""
已知一个长度为 n 的数组，预先按照升序排列，经由 1 到 n 次 旋转 后，得到输入数组。例如，原数组 nums = [0,1,2,4,5,6,7] 在变化后可能得到：
若旋转 4 次，则可以得到 [4,5,6,7,0,1,2]
若旋转 7 次，则可以得到 [0,1,2,4,5,6,7]
注意，数组 [a[0], a[1], a[2], ..., a[n-1]] 旋转一次 的结果为数组 [a[n-1], a[0], a[1], a[2], ..., a[n-2]] 。

给你一个元素值 互不相同 的数组 nums ，它原来是一个升序排列的数组，并按上述情形进行了多次旋转。请你找出并返回数组中的 最小元素 。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def findMin(self, nums: List[int]) -> int:
        length = len(nums)
        l = 0
        r = length - 1
        while l <= r:
            mid = int((l + r) / 2)
            # 怎么判断结束，拿到最小的值
            if nums[mid] >= nums[l] and nums[mid] > nums[r]:
                l = mid + 1
            # elif nums[mid] < nums[l] and nums[mid] < nums[r]:
            #     l = mid + 1
            else:
                r = mid - 1
        return nums[mid]


# ！：错误答案，没写出来
# check(Solution().findMin, [[3, 4, 5, 1, 2]], 1)
# check(Solution().findMin, [[4, 5, 6, 7, 0, 1, 2]], 0)
# check(Solution().findMin, [[2, 1]], 1)

print("题解")
"""
如果只比较左值与中值，不能确定最小值的位置范围。

作者：armeria-program
链接：https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/solution/er-fen-cha-zhao-wei-shi-yao-zuo-you-bu-dui-cheng-z/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。"""


class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        # 不用相等，最终回归到答案
        while left < right:
            mid = (left + right) >> 1
            # 同右边的比较！
            # 如果中间比右边大，肯定结果在右边！
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                # 否则的化，可能中间就可能是答案！
                right = mid
        return nums[left]


class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right + 1) >> 1  # 先加一再除，mid更靠近右边的right
            if nums[left] < nums[mid]:
                # > 这里不能加1是因为mid可能就是正确答案
                left = mid  # 向右移动左边界
            elif nums[left] > nums[mid]:
                right = mid - 1  # 向左移动右边界
        return nums[(right + 1) % len(nums)]  # 最大值向右移动一位就是最小值了（需要考虑最大值在最右边的情况，右移一位后对数组长度取余）
