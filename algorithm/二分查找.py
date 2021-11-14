"""
给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-search
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


**如何注意这些条件细节？**
- https://labuladong.github.io/ebook/%E7%AE%97%E6%B3%95%E6%80%9D%E7%BB%B4%E7%B3%BB%E5%88%97/%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E8%AF%A6%E8%A7%A3.html

"""


class Solution(object):
    def search(self, nums, target):
        left, right = 0, len(nums) - 1
        result = -1
        if not nums:
            return result

        # 判断是相等？因为收束会回到一样进行判断, 场景： [2, 5], 5
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                result = mid
                break
        return result


print(Solution().search([-1, 0, 3, 5, 9, 12], 9))
print(Solution().search([-1, 0, 3, 5, 9, 12], 11))
print(Solution().search([-1, 0, 3, 5, 9, 12], 13))
print(Solution().search([2, 5], 5))
