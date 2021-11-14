# - [leetcode排序数组](https://leetcode-cn.com/problems/sort-an-array/)

import random


def charu_sort(nums):
    length = len(nums)
    for i in range(1, length):
        while (i - 1) >= 0 and nums[i - 1] > nums[i]:
            # 可以不用每次交换两个，等到最后在交换。但需要判断nums[i - 1] > nums[i]才执行。见《数据结构》一书。
            nums[i - 1], nums[i] = nums[i], nums[i - 1]
            i -= 1
    return nums


# 还可以通过折半优化
def xier_sort(nums):
    length = len(nums)
    interval = int(length / 2)
    while interval > 0:
        for i in range(interval, length):
            while i - interval >= 0 and nums[i - interval] > nums[i]:
                nums[i], nums[i - interval] = nums[i - interval], nums[i]
                i -= interval
        interval = int(interval / 2)
    return nums


def xuanze_sort(nums):
    length = len(nums)
    for i in range(length):
        min_idx = i
        for j in range(i, length):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return nums


def guibing(n1, n2):
    if len(n1) > 1:
        n1 = guibing(n1[:int(len(n1) / 2)], n1[int(len(n1) / 2):])
    if len(n2) > 1:
        n2 = guibing(n2[:int(len(n2) / 2)], n2[int(len(n2) / 2):])
    s = 0
    n3 = []
    for i in n1:
        while s < len(n2) and n2[s] < i:
            n3.append(n2[s])
            s += 1
        n3.append(i)
    while s < len(n2):
        n3.append(n2[s])
        s += 1
    return n3


def guibing_sort(nums):
    length = len(nums)
    half = int(length / 2)
    nums = guibing(nums[:half], nums[half:])
    return nums


sort = guibing_sort

input = [random.randint(1, 20) for _ in range(0, 10)]
# 无法处理有负数的例子， 注意负数取于取模问题， 注意有负数查找最大位数的长度逻辑
input = [4, 1, 10, 9, 1, -1, -21, -12]
# input = [-1, 2, -8, -10]
print(f"input {input} ,result {sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 100) for _ in range(-20, 20)]
    o1 = sort(input)
    o2 = sorted(input)
    assert o1 == o2
