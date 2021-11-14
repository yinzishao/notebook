class Solution:
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def back(i=0):
            if i == len(nums):
                res.append(nums[::])
            for j in range(i, len(nums)):
                nums[i], nums[j] = nums[j], nums[i]
                back(i + 1)
                nums[j], nums[i] = nums[i], nums[j]
        res = []
        back()
        return res


print(Solution().permute([1, 2, 3]))
