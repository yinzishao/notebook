"""
给定两个数组，编写一个函数来计算它们的交集。



示例 1：

输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2,2]
示例 2:

输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[4,9]


说明：

输出结果中每个元素出现的次数，应与元素在两个数组中出现次数的最小值一致。
我们可以不考虑输出结果的顺序。
进阶：

如果给定的数组已经排好序呢？你将如何优化你的算法？
如果 nums1 的大小比 nums2 小很多，哪种方法更优？
如果 nums2 的元素存储在磁盘上，内存是有限的，并且你不能一次加载所有的元素到内存中，你该怎么办？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/intersection-of-two-arrays-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from collections import defaultdict
from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        a, b = defaultdict(int), defaultdict(int)
        for i in nums1:
            a[i] += 1
        for i in nums2:
            b[i] += 1
        result = []
        for k, v in a.items():
            if b[k] > 0 and a[k] > 0:
                n = min(a[k], b[k])
                while n > 0:
                    result.append(k)
                    n -= 1
        return result


print(Solution().intersect([4, 9, 5], [9, 4, 9, 8, 4]))

"""

优化上面版本的思路

只需要初始化一个数组的字典，另一个数组只需要进行遍历，然遍历发现存在则-1。

也不需要初始化结果，方法是遍历第二个数组的时候，顺序替换进数组前面。达到节省空间
"""


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        a = defaultdict(int)
        for i in nums1:
            a[i] += 1
        idx = 0
        for i in nums2:
            if a.get(i, 0) > 0:
                nums2[idx] = i
                idx += 1
                a[i] -= 1
        return nums2[:idx]


print(Solution().intersect([4, 9, 5], [9, 4, 9, 8, 4]))

"""
如果给定的数组已经排好序呢？你将如何优化你的算法？

设定两个为0的指针，比较两个指针的元素是否相等。 如果指针的元素相等，我们将两个指针一起向后移动，并且将相等的元素放入空白数组。

如果两个指针的元素不相等，我们将小的一个指针后移。 图中我们指针移到下一个元素，判断不相等之后，将元素小的指针向后移动，继续进行判断。

"""


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1 = sorted(nums1)
        nums2 = sorted(nums2)
        s1, s2, idx = 0, 0, 0
        e1, e2 = len(nums1), len(nums2)
        while s1 < e1 and s2 < e2:
            if nums1[s1] == nums2[s2]:
                nums1[idx] = nums1[s1]
                s1 += 1
                s2 += 1
                idx += 1
            elif nums1[s1] > nums2[s2]:
                s2 += 1
            else:
                s1 += 1
        return nums1[:idx]


print(Solution().intersect([4, 9, 5], [9, 4, 9, 8, 4]))

"""
Q:如果 nums1 的大小比 nums2 小很多，哪种方法更优？
Q: 如果 nums2 的元素存储在磁盘上，内存是有限的，并且你不能一次加载所有的元素到内存中，你该怎么办？
A: 如果 nums2  的元素存储在磁盘上，磁盘内存是有限的，并且你不能一次加载所有的元素到内存中。那么就无法高效地对 nums2  进行排序，因此推荐使用方法一而不是方法二。在方法一中，nums2  只关系到查询操作，因此每次读取 nums2  中的一部分数据，并进行处理即可。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/intersection-of-two-arrays-ii/solution/liang-ge-shu-zu-de-jiao-ji-ii-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

Q: 如果都很大的情况下?
但是解法一中需要改造，一般说排序算法都是针对于内部排序，一旦涉及到跟磁盘打交道（外部排序），则需要特殊的考虑。归并排序是天然适合外部排序的算法，可以将分割后的子数组写到单个文件中，归并时将小文件合并为更大的文件。当两个数组均排序完成生成两个大文件后，即可使用双指针遍历两个文件，如此可以使空间复杂度最低。

作者：Alien-Leon
链接：https://leetcode-cn.com/problems/intersection-of-two-arrays-ii/solution/jin-jie-san-wen-by-user5707f/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
