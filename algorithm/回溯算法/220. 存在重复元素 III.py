"""
给你一个整数数组 nums 和两个整数k 和 t 。请你判断是否存在 两个不同下标 i 和 j，使得abs(nums[i] - nums[j]) <= t ，同时又满足 abs(i - j) <= k 。

如果存在则返回 true，不存在返回 false。


示例1：

输入：nums = [1,2,3,1], k = 3, t = 0
输出：true
示例 2：

输入：nums = [1,0,1,1], k = 1, t = 2
输出：true
示例 3：

输入：nums = [1,5,9,1,5,9], k = 2, t = 3
输出：false

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/contains-duplicate-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        """超出时间限制"""
        length = len(nums)

        res = []

        def dig(start):
            if len(res) == 2:
                print(res)
                if abs(res[0] - res[1]) <= k and abs(nums[res[0]] - nums[res[1]]) <= t:
                    return True
                return

            for i in range(start, length):
                res.append(i)
                result = dig(i + 1)
                if result:
                    return True
                res.pop()
            return False

        return dig(0)


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        length = len(nums)

        res = []

        def dig(start):
            if len(res) == 2:
                print(res)
                if abs(res[0] - res[1]) <= k and abs(nums[res[0]] - nums[res[1]]) <= t:
                    return True
                return

            for i in range(start, length):
                # 添加剪枝还是超时
                if res:
                    if abs(i - res[0]) > k:
                        break
                res.append(i)
                result = dig(i + 1)
                if result:
                    return True
                res.pop()
            return False

        return dig(0)


check(Solution().containsNearbyAlmostDuplicate, [[1, 5, 9, 1, 5, 9], 2, 3], False)
nums = [1, 0, 1, 1]
k = 1
t = 2
check(Solution().containsNearbyAlmostDuplicate, [nums, k, t], True)

"""
回溯跟暴力没啥区别！

作者：fe-lucifer
链接：https://leetcode-cn.com/problems/contains-duplicate-iii/solution/220-cun-zai-zhong-fu-yuan-su-iii-cong-on2-dao-on-p/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, min(len(nums), i + k + 1)):
                if abs(nums[i] - nums[j]) <= t:
                    return True
        return False


print("题解")
"""

方法一：滑动窗口 + 有序集合
思路及算法

对于序列中每一个元素 xx 左侧的至多 kk 个元素，如果这 kk 个元素中存在一个元素落在区间 [x - t, x + t][x−t,x+t] 中，我们就找到了一对符合条件的元素。注意到对于两个相邻的元素，它们各自的左侧的 kk 个元素中有 k - 1k−1 个是重合的。于是我们可以使用滑动窗口的思路，维护一个大小为 kk 的滑动窗口，每次遍历到元素 xx 时，滑动窗口中包含元素 xx 前面的最多 kk 个元素，我们检查窗口中是否存在元素落在区间 [x - t, x + t][x−t,x+t] 中即可。

如果使用队列维护滑动窗口内的元素，由于元素是无序的，我们只能对于每个元素都遍历一次队列来检查是否有元素符合条件。如果数组的长度为 nn，则使用队列的时间复杂度为 O(nk)O(nk)，会超出时间限制。

因此我们希望能够找到一个数据结构维护滑动窗口内的元素，该数据结构需要满足以下操作：

支持添加和删除指定元素的操作，否则我们无法维护滑动窗口；

内部元素有序，支持二分查找的操作，这样我们可以快速判断滑动窗口中是否存在元素满足条件，具体而言，对于元素 xx，当我们希望判断滑动窗口中是否存在某个数 yy 落在区间 [x - t, x + t][x−t,x+t] 中，只需要判断滑动窗口中所有大于等于 x - tx−t 的元素中的最小元素是否小于等于 x + tx+t 即可。

我们可以使用有序集合来支持这些操作。

实现方面，我们在有序集合中查找大于等于 x - tx−t 的最小的元素 yy，如果 yy 存在，且 y \leq x + ty≤x+t，我们就找到了一对符合条件的元素。完成检查后，我们将 xx 插入到有序集合中，如果有序集合中元素数量超过了 kk，我们将有序集合中最早被插入的元素删除即可。

注意

如果当前有序集合中存在相同元素，那么此时程序将直接返回 true。因此本题中的有序集合无需处理相同元素的情况。

为防止整型 int 溢出，我们既可以使用长整型 long，也可以对查找区间 [x - t, x + t][x−t,x+t] 进行限制，使其落在 int 范围内。


作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/contains-duplicate-iii/solution/cun-zai-zhong-fu-yuan-su-iii-by-leetcode-bbkt/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

> 主要还是要维护好窗口的数据结构！支持增删，也支持快速查找。treeset的实现!python3有序集合？但要实现ceilingKey方法
> 窗口内只保留符合步长的集合
> treeset使用？treemap和hashmap的区别？
"""

print("桶题解")
"""

首先，定义桶的大小是t+1, nums[i]//(t+1)决定放入几号桶,这样在一个桶里面的任意两个的绝对值差值都<=t
例如t=3, nums=[0 ,5, 1, 9, 3,4],那么0号桶就有[0,1,3],1号桶就有[4,5],2号桶就有[9]

先不考虑索引差值最大为K的限制，那么遍历nums每一个元素，并把他们放入相应的桶中，有两种情况会返回True

要放入的桶中已经有其他元素了，这时将nums[i]放进去满足差值<=t
可能存在前面一个桶的元素并且与nums[i]的差值<=t 或者 存在后面一个桶的元素并且与nums[i]的差值<=t
根据返回True的第一个条件，可以知道前后桶的元素最多也只能有一个。

接着考虑限制桶中的索引差最大为K,当i>=k的时候：
我们就要去删除存放着nums[i-k]的那个桶(编号为nums[i-k]//(t+1))
这样就能保证遍历到第i+1个元素时，全部桶中元素的索引最小值是i-k+1，就满足题目对索引的限制了

作者：zhou-pen-cheng
链接：https://leetcode-cn.com/problems/contains-duplicate-iii/solution/li-yong-tong-de-yuan-li-onpython3-by-zhou-pen-chen/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

通过取模，发现一样的桶则符合题意。如果桶不一样，需要跟前一个与后一个比较。然后遍历到大于步长的位置，需要把前一个不符合步长的元素给干掉！

空间获取时间、而且要动态维护好空间。

"""


class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        if t < 0 or k < 0:
            return False
        all_buckets = {}
        bucket_size = t + 1  # 桶的大小设成t+1更加方便
        for i in range(len(nums)):
            bucket_num = nums[i] // bucket_size  # 放入哪个桶

            if bucket_num in all_buckets:  # 桶中已经有元素了
                return True

            all_buckets[bucket_num] = nums[i]  # 把nums[i]放入桶中

            if (bucket_num - 1) in all_buckets and abs(all_buckets[bucket_num - 1] - nums[i]) <= t:  # 检查前一个桶
                return True

            if (bucket_num + 1) in all_buckets and abs(all_buckets[bucket_num + 1] - nums[i]) <= t:  # 检查后一个桶
                return True

            # 如果不构成返回条件，那么当i >= k 的时候就要删除旧桶了，以维持桶中的元素索引跟下一个i+1索引只差不超过k
            if i >= k:
                all_buckets.pop(nums[i - k] // bucket_size)

        return False
