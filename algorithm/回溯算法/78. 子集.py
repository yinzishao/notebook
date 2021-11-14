"""
给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。

解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。
示例 1：

输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
示例 2：

输入：nums = [0]
输出：[[],[0]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/subsets
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
import copy
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # 全排列的思路，然后就是i的时候添加长度为i的元素，但是要去重
        def back(i=0):
            i_item = nums[:i]
            # 如何去重？
            res.append(i_item)
            for j in range(i, length):
                nums[i], nums[j] = nums[j], nums[i]
                back(i + 1)
                nums[j], nums[i] = nums[i], nums[j]

        res = []
        length = len(nums)
        back()
        return res


print("显而易见：但超出时间限制！")
nums = [1, 2, 3]
# check(Solution().subsetsWithDup, [nums], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]])

"""
可以发现 0/1 序列对应的二进制数正好从 0 到 2^n - 1

我们可以按照这个 0/1 序列在原集合当中取数。当我们枚举完所有 2^n2个mask，我们也就能构造出所有的子集。

golang：

func subsets(nums []int) (ans [][]int) {
    n := len(nums)
    for mask := 0; mask < 1<<n; mask++ {
        set := []int{}
        for i, v := range nums {
            if mask>>i&1 > 0 {
                set = append(set, v)
            }
        }
        ans = append(ans, append([]int(nil), set...))
    }
    return
}

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/subsets/solution/zi-ji-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

pass

print("题解： 回溯")


class Solution:
    """
    https://leetcode-cn.com/problems/subsets/solution/hui-su-suan-fa-by-powcai-5/
    """

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        def back(i, tmp):
            res.append(tmp)
            for j in range(i, length):
                # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
                # 注意是j传递！
                # 遍历到第二个元素的时候，传进去的也就是第二个元素以及后面元素的组合
                back(j + 1, tmp + [nums[j]])

        res = []
        length = len(nums)
        back(0, [])
        return res


nums = [1, 2, 3]

check(Solution().subsetsWithDup, [nums], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]])

print("回溯法的题解")

""""
！！！！
思路上是跟上面一致的，主要还是遍历下标，但是递归的下一层要的是比当前要后的数组组合。题解好像反而不好理解？

[1] [2,3] => [1, 2]+[3] [1, 3]+[]
[2] [3]
[3] []
遍历到第二个元素的时候，传进去的也就是第二个元素以及后面元素的组合

作者：fuxuemingzhu
链接：https://leetcode-cn.com/problems/subsets-ii/solution/hui-su-fa-mo-ban-tao-lu-jian-hua-xie-fa-y4evs/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

也可以看这个。 https://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247485007&idx=1&sn=ceb42ba2f341af34953d158358c61f7c&chksm=9bd7f847aca071517fe0889d2679ead78b40caf6978ebc1d3d8355d6693acc7ec3aca60823f0&scene=21#wechat_redirect

vector<vector<int>> res;

vector<vector<int>> subsets(vector<int>& nums) {
    // 记录走过的路径
    vector<int> track;
    backtrack(nums, 0, track);
    return res;
}

void backtrack(vector<int>& nums, int start, vector<int>& track) {
    res.push_back(track);
    // 注意 i 从 start 开始递增
    for (int i = start; i < nums.size(); i++) {
        // 做选择
        track.push_back(nums[i]);
        // 回溯
        backtrack(nums, i + 1, track);
        // 撤销选择
        track.pop_back();
    }
}
"""


class Solution(object):
    def subsets(self, nums):
        res, path = [], []
        self.dfs(nums, 0, res, path)
        return res

    def dfs(self, nums, index, res, path):
        res.append(copy.deepcopy(path))
        # for 循环的意义是说，从后续元素 nums[index:N-1] 中挑选剩余元素的时候，每个元素都有选和不选两个状态。
        # 个人理解，这个题解的注释不是很好理解。
        for i in range(index, len(nums)):
            # 做选择。选这个元素
            path.append(nums[i])
            # ！： 传递的选择列表相比全排列，是当前下标的后面。
            self.dfs(nums, i + 1, res, path)
            # 撤销选择。不选这个元素
            path.pop()


print("迭代")
"""
维护res为全部子集，new_subsets为每次新加入的子集，注意这里每遇到一个数，就会与之前的res中的每一个构成新子集，也就是说，每次都会翻倍，代码非常简单

作者：quan-zi-dong-dai-ma-ji
链接：https://leetcode-cn.com/problems/subsets-ii/solution/python-yi-ci-bian-li-mo-ni-bu-xu-yao-hui-3149/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

也跟这个一致： https://leetcode-cn.com/problems/subsets/solution/hui-su-suan-fa-by-powcai-5/
"""


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]
        for i in range(len(nums)):
            new_subsets = [subset + [nums[i]] for subset in res]
            res = new_subsets + res
        return res
