"""
给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现了三次。找出那个只出现了一次的元素。

说明：

你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？

示例 1:

输入: [2,2,3,2]
输出: 3
示例 2:

输入: [0,1,0,1,0,1,99]
输出: 99


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/single-number-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        s = set()
        sum_nums = 0
        for i in nums:
            sum_nums += i
            s.add(i)
        return int((sum(s) * 3 - sum_nums) / 2)


check(Solution().singleNumber, [[0, 1, 0, 1, 0, 1, 99]], 99)

"""
真正的挑战在于 Google 面试官要求使用**常数空间**解决该问题（最近 6 个月该问题在 Google 上非常流行），测试应聘者是否熟练位操作。

只有某个位置的数字出现奇数次时，该位的掩码才不为 0。

因此，可以检测出出现一次的位和出现三次的位，但是要注意区分这两种情况。

AND 和 NOT

为了区分出现一次的数字和出现三次的数字，使用两个位掩码：seen_once 和 seen_twice。

思路是：

仅当 seen_twice 未变时，改变 seen_once。

仅当 seen_once 未变时，改变seen_twice。

作者：LeetCode
链接：https://leetcode-cn.com/problems/single-number-ii/solution/zhi-chu-xian-yi-ci-de-shu-zi-ii-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        seen_once = seen_twice = 0
        for i in nums:
            # 第一次发生如果是仅仅如此，第三次无法清理。所以会要跟第二次出现的发生关系
            # seen_once = seen_once ^ i
            # 既不在出现一次的b1，也不在出现两次的b2里面，我们就记录下来，出现了一次，再次出现则会抵消
            seen_once = ~seen_twice & (seen_once ^ i)
            # 既不在出现两次的b2里面，也不再出现一次的b1里面(不止一次了)，记录出现两次，第三次则会抵消
            seen_twice = ~seen_once & (seen_twice ^ i)
        return seen_once


check(Solution().singleNumber, [[0, 1, 0, 1, 0, 1, 99]], 99)
