"""

给你一个有序数组 nums ，请你 原地 删除重复出现的元素，使每个元素 最多出现两次 ，返回删除后数组的新长度。

不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        pre = 0
        cnt = 1
        for i in nums[1:]:
            if i == nums[pre]:
                if cnt > 1:
                    continue
                else:
                    nums[pre + 1] = i
                    pre += 1
                    cnt += 1
            else:
                nums[pre + 1] = i
                pre += 1
                cnt = 1
        return pre + 1


nums = [1, 1, 1, 2, 2, 3]
nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]

res = Solution().removeDuplicates(nums)
print(nums[:res])

print("题解")
"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array-ii/solution/shan-chu-pai-xu-shu-zu-zhong-de-zhong-fu-yec2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 2:
            return n
        j = 2
        # 从第三个元素开始检查
        for i in range(2, n):
            # 注意这里。如果慢指针的前前一个不一样
            # 以此来避免可以重复多少个。
            if nums[i] != nums[j - 2]:
                nums[j] = nums[i]
                j += 1
        return j
