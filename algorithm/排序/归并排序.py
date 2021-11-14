"""
申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列；

设定两个指针，最初位置分别为两个已经排序序列的起始位置；

比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置；

重复步骤 3 直到某一指针达到序列尾；

将另一序列剩下的所有元素直接复制到合并序列尾。

"""
import random


def sort(n):
    l = len(n)
    if l < 2:
        return n

    mid = int(l / 2)
    left, right = n[:mid], n[mid:]
    # 递归
    return merge(sort(left), sort(right))


def merge(left, right):
    """合并两个数组"""
    result = []
    r_i = 0
    for i in left:
        while r_i < len(right) and right[r_i] < i:
            result.append(right[r_i])
            r_i += 1
        result.append(i)
    while r_i < len(right):
        result.append(right[r_i])
        r_i += 1
    return result


# print(merge([1, 3, 5, 7, 9], [2, 4, 6, 12, 14]))
input = [random.randint(1, 20) for _ in range(0, 10)]
print(f"input {input} ,result {sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 10000) for _ in range(0, 1000)]
    o1 = sort(input)
    o2 = sorted(input)
    assert o1 == o2
