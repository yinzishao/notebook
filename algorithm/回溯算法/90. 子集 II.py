"""
给你一个整数数组 nums ，其中可能包含重复元素，请你返回该数组所有可能的子集（幂集）。

解集 不能 包含重复的子集。返回的解集中，子集可以按 任意顺序 排列。



示例 1：

输入：nums = [1,2,2]
输出：[[],[1],[1,2],[1,2,2],[2],[2,2]]
示例 2：

输入：nums = [0]
输出：[[],[0]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/subsets-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # 全排列的思路，然后就是i的时候添加长度为i的元素，但是要去重
        def back(i=0):
            i_item = nums[:i]
            # 显而易见：超出时间限制！
            if tuple(sorted(i_item)) not in res_set:
                res.append(i_item)
                res_set.add(tuple(sorted(i_item)))
            for j in range(i, length):
                nums[i], nums[j] = nums[j], nums[i]
                back(i + 1)
                nums[j], nums[i] = nums[i], nums[j]

        res = []
        length = len(nums)
        res_set = set()
        back()
        return res


print("显而易见：虽然正确，但超出时间限制！")
nums = [1, 2, 2]
check(Solution().subsetsWithDup, [nums], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])

"""
题解： https://leetcode-cn.com/problems/subsets-ii/solution/hui-su-fa-mo-ban-tao-lu-jian-hua-xie-fa-y4evs/
"""

print("参考题解")


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # 跟子集1的问题是同样的思路，只是排序后，[1, 1, 2] 遍历的时候可以比较是否需要添加进去
        nums = sorted(nums)

        def helper(idx, tmp):
            res.append(tmp)
            for i in range(idx, length):
                if (i - idx) > 0 and nums[i - 1] == nums[i]:
                    continue
                helper(i + 1, tmp + [nums[i]])

        res = []
        length = len(nums)
        helper(0, [])
        return res


nums = [1, 2, 2]
check(Solution().subsetsWithDup, [nums], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])

print("迭代")

"""

妙呀！

子集一：维护res为全部子集，new_subsets为每次新加入的子集，注意这里每遇到一个数，就会与之前的res中的每一个构成新子集，也就是说，每次都会翻倍，代码非常简单


子集二： 其实解决方法很简单，考虑如果nums[i] == nums[i-1]nums[i]==nums[i−1],那么我们只能与之前新构成的子集配对.
这时只需要利用new_subsets即可。在刚才的例子中，只需要与newsubset = [[2], [1,2]]配对就行啦。
代码如下，依然十分简单。

作者：quan-zi-dong-dai-ma-ji
链接：https://leetcode-cn.com/problems/subsets-ii/solution/python-yi-ci-bian-li-mo-ni-bu-xu-yao-hui-3149/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution(object):
    def subsetsWithDup(self, nums):
        res = [[]]
        nums.sort()
        for i in range(len(nums)):
            if i >= 1 and nums[i] == nums[i - 1]:
                new_subsets = [subset + [nums[i]] for subset in new_subsets]
            else:
                new_subsets = [subset + [nums[i]] for subset in res]
            res = new_subsets + res
        return res


nums = [1, 2, 2]
# check(Solution().subsetsWithDup, [nums], [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
