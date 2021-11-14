"""
给你两个有序整数数组 nums1 和 nums2，请你将 nums2 合并到 nums1 中，使 nums1 成为一个有序数组。

初始化 nums1 和 nums2 的元素数量分别为 m 和 n 。你可以假设 nums1 的空间大小等于 m + n，这样它就有足够的空间保存来自 nums2 的元素。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        r_1 = m - 1
        r_2 = n - 1
        lenght = m + n - 1
        # 注意 >= and 还是其他情况！
        while r_1 >= 0 and r_2 >= 0:
            if nums1[r_1] >= nums2[r_2]:
                nums1[lenght] = nums1[r_1]
                r_1 -= 1
            else:
                nums1[lenght] = nums2[r_2]
                r_2 -= 1
            lenght -= 1
        while r_2 >= 0:
            nums1[lenght] = nums2[r_2]
            lenght -= 1
            r_2 -= 1
        return nums1


nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3

check(Solution().merge, [nums1, m, nums2, n], [1, 2, 2, 3, 5, 6])
check(Solution().merge, [[0], 0, [1], 1], [1])
check(Solution().merge, [[2, 0], 1, [1], 1], [1, 2])

"""
https://leetcode-cn.com/problems/merge-sorted-array/solution/he-bing-liang-ge-you-xu-shu-zu-by-leetco-rrb0/
"""


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        r_1 = m - 1
        r_2 = n - 1
        lenght = m + n - 1

        while r_2 >= 0:
            if r_1 < 0 or nums2[r_2] > nums1[r_1]:
                nums1[lenght] = nums2[r_2]
                r_2 -= 1
            else:
                nums1[lenght] = nums1[r_1]
                r_1 -= 1
            lenght -= 1
        return nums1


print('题解！')
nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3
check(Solution().merge, [nums1, m, nums2, n], [1, 2, 2, 3, 5, 6])
check(Solution().merge, [[0], 0, [1], 1], [1])
check(Solution().merge, [[2, 0], 1, [1], 1], [1, 2])
