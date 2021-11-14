#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速排序的最坏运行情况是 O(n²)，比如说顺序数列的快排。但它的平摊期望时间是 O(nlogn)，且 O(nlogn) 记号中隐含的常数因子很小，比复杂度稳定等于 O(nlogn) 的归并排序要小很多。所以，对绝大多数顺序性较弱的随机数列而言，快速排序总是优于归并排序。

从数列中挑出一个元素，称为 “基准”（pivot）;

重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作；

递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序；

递归的最底部情形，是数列的大小是零或一，也就是永远都已经被排序好了。虽然一直递归下去，但是这个算法总会退出，因为在每次的迭代（iteration）中，它至少会把一个元素摆到它最后的位置去。


- https://blog.csdn.net/liuyi1207164339/article/details/50827608

方法1 固定基准元
如果输入序列是随机的，处理时间是可以接受的。如果数组已经有序时，此时的分割就是一个非常不好的分割。因为每次划分只能使待排序序列减一（无论是顺序还是倒序比较都是o(n^2), 区别只是移动而已），此时为最坏情况，快速排序沦为冒泡排序，时间复杂度为Θ(n^2)。而且，输入的数据是有序或部分有序的情况是相当常见的。因此，使用第一个元素作为基准元是非常糟糕的，应该立即放弃这种想法。

方法2 随机基准元
这是一种相对安全的策略。由于基准元的位置是随机的，那么产生的分割也不会总是会出现劣质的分割。在整个数组数字全相等时，仍然是最坏情况，时间复杂度是O(n^2）。实际上，随机化快速排序得到理论最坏情况的可能性仅为1/(2^n）。所以随机化快速排序可以对于绝大多数输入数据达到O(nlogn）的期望时间复杂度。


方法3 三数取中
引入的原因：虽然随机选取基准时，减少出现不好分割的几率，但是还是最坏情况下还是O(n^2），要缓解这种情况，就引入了三数取中选取基准。

"""


def quick_sort(arr, left=None, right=None):
    left = 0 if not isinstance(left, (int, float)) else left
    right = len(arr) - 1 if not isinstance(right, (int, float)) else right
    if left < right:
        partition_index = partition(arr, left, right)
        # 分治法
        quick_sort(arr, left, partition_index - 1)
        quick_sort(arr, partition_index + 1, right)
    return arr


def partition(arr, left, right):
    """对数组的左右范围进行排序"""
    pivot = left
    index = pivot + 1
    i = index
    # pivot的下标不会改变，通过移动后面的数值进行排序，最后结束后，通过移动pivot和index进行移动。
    while i <= right:
        # 通过i来进行递增遍历所有的参数，如果发现数值小于基准的数值，则移动index和i的位置（第一次都是相同的值不移动）
        # index： **index记录的是比基准值要大数字的下标位置， 比基准值要小的数字都在index的左边。所以遇到大于基准值的不移动，以作下次的交换。**
        if arr[i] < arr[pivot]:
            # 跟下面的算法导论版本一致
            swap(arr, i, index)
            index += 1
        i += 1
    swap(arr, pivot, index - 1)
    return index - 1


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


print(quick_sort([5, 3, 2, 4, 7, 8, 1]))


def quick_sort(data):
    """快速排序"""
    if len(data) >= 2:  # 递归入口及出口
        mid = data[len(data) // 2]  # 选取基准值，也可以选取第一个或最后一个元素
        left, right = [], []  # 定义基准值左右两侧的列表
        data.remove(mid)  # 从原始数组中移除基准值
        for num in data:
            if num >= mid:
                right.append(num)
            else:
                left.append(num)
        return quick_sort(left) + [mid] + quick_sort(right)
    else:
        return data


"""算法导论版本"""


class Solution:
    def sortArray(self, array):
        self.quick_sort(array, 0, len(array) - 1)
        return array

    def quick_sort(self, array, l, r):
        if l < r:
            q = self.partition(array, l, r)
            self.quick_sort(array, l, q - 1)
            self.quick_sort(array, q + 1, r)

    def partition(self, array, l, r):
        x = array[r]  # 最后一个元素作为基准值
        i = l  # 存放比基准值要大的游标
        for j in range(l, r):
            # i指向的是比基准要大的窗口的首个元素的下标
            # 如果发现比基准值的数值要大，则停止i下标，用作下一次的交换
            # 从左往右进行遍历，说是进行交换。但是如果都是有序的话，就交换一个寂寞。
            # 交换的场景：当某个数比基准值要大，这时候i停止移动，但是j继续移动。
            # 所以下次发现比基准值小的时候，i和j会进行交换，以达到小值都放在交换后的i+1的左边。
            if array[j] <= x:
                array[i], array[j] = array[j], array[i]
                i += 1
        # 结束的时候，index是会比基准值要大的
        array[i], array[r] = array[r], array[i]
        return i

    def partition_2(self, array, l, r):
        """另一种排序方式"""


arr = [5, 3, 2, 4, 7, 8, 1]
print('--2', Solution().sortArray(arr))


# 严蔚敏《数据结构》
def quick(nums, l, r):
    if l >= r:
        return
    s = l
    e = r
    while s < e:
        # 从后面先遍历就可以了？
        while s < e and nums[e] > nums[l]:
            e -= 1
        # 该遍历放前面会造成s会停留在比基准大的位置
        # 而从后面遍历则会让s停留在比基准小的位置
        while s < e and nums[s] <= nums[l]:
            s += 1
        nums[s], nums[e] = nums[e], nums[s]
    # s停留在比基准小的位置，所有还得把基准移到s的位置上
    nums[s], nums[l] = nums[l], nums[s]
    quick(nums, l, s - 1)
    quick(nums, s + 1, r)


def quick_sort(nums):
    length = len(nums)
    quick(nums, 0, length - 1)
    return nums
