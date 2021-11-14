import random


def deep(nums, i, length):
    l = 2 * i + 1
    r = 2 * i + 2
    max_idx = i
    tmp = nums[i]
    if l < length and nums[max_idx] < nums[l]:
        max_idx = l
    if r < length and nums[max_idx] < nums[r]:
        max_idx = r
    if max_idx != i:
        nums[i], nums[max_idx] = nums[max_idx], tmp
        deep(nums, max_idx, length)


def heap_sort(nums):
    # 构造最大堆
    length = len(nums)
    for i in range(int(length / 2))[::-1]:
        deep(nums, i, length)
    # 遍历获取最大值
    for i in range(length)[::-1]:
        nums[0], nums[i] = nums[i], nums[0]
        length -= 1
        deep(nums, 0, length)
    return nums


input = [random.randint(1, 20) for _ in range(0, 10)]
# 无法处理有负数的例子， 注意负数取于取模问题， 注意有负数查找最大位数的长度逻辑
input = [4, 1, 10, 9, 1, -1, -21, -12]
# input = [-1, 2, -8, -10]
print(f"input {input} ,result {heap_sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 100) for _ in range(-20, 20)]
    o1 = heap_sort(input)
    o2 = sorted(input)
    assert o1 == o2
