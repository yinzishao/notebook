"""
给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回滑动窗口中的最大值。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sliding-window-maximum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
import collections
from typing import List

from notebook.algorithm.树.utils import check

"""
题解思路：

遍历该数组，同时**在双端队列的头去维护当前窗口的最大值（在遍历过程中，发现当前元素比队列中的元素大，就将原来队列中的元素祭天），在整个遍历的过程中我们再记录下每一个窗口的最大值到结果数组中。**最终结果数组就是我们想要的，整体图解如下。

注意： 队头是最大的。而且单调队列的 push 方法依然在队尾添加元素，但是要把前面比新元素小的元素都删掉。
以此使得队头的下标超出窗口范围也进行移除后的，窗口也能找到最大值
"""


# 队头是最大的
# 单调队列的 push 方法依然在队尾添加元素，但是要把前面比新元素小的元素都删掉
# 如果队头的下标超出窗口范围也进行移除
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums:
            return []
        res = []
        # deq = []
        deq = collections.deque()
        for i in range(len(nums)):
            if not deq:
                deq.append(i)
            else:
                if deq[0] < (i - k + 1):
                    # deq.pop(0)
                    deq.popleft()
                while deq and nums[i] > nums[deq[-1]]:
                    # deq.pop(-1)
                    # 队尾移除，使得队列递减，能至少维护一个值
                    deq.pop()
                # 不管如何deq还是会加上当前值的
                deq.append(i)
            if i + 1 >= k:
                res.append(nums[deq[0]])
        return res


# check(Solution().maxSlidingWindow, [[1, 3, -1, -3, 5, 3, 6, 7], 3], [3, 3, 5, 5, 6, 7])
# check(Solution().maxSlidingWindow, [[1], 1], [1])
check(Solution().maxSlidingWindow, [[7, 2, 4], 2], [7, 4])

"""
上面自己写的：几秒前	通过	432 ms	26.7 MB
题解写的： 几秒前	通过	396 ms	26.8 MB 差别在少了判断if i + 1 >= k:?

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/sliding-window-maximum/solution/hua-dong-chuang-kou-zui-da-zhi-by-leetco-ki6m/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        q = collections.deque()
        for i in range(k):
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)

        ans = [nums[q[0]]]
        for i in range(k, n):
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)
            if q[0] <= i - k:
                # while q[0] <= i - k:
                q.popleft()
            ans.append(nums[q[0]])

        return ans
