"""
首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置

再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。

重复第二步，直到所有元素均排序完毕
"""
import random


def sort(n):
    l = len(n)
    for i in range(l):
        tmp = i
        for j in range(i + 1, l):
            if n[j] < n[tmp]:
                tmp = j
        n[tmp], n[i] = n[i], n[tmp]
    return n


input = [random.randint(1, 20) for _ in range(0, 10)]
print(f"input {input} ,result {sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 10000) for _ in range(0, 1000)]
    o1 = sort(input)
    o2 = sorted(input)
    assert o1 == o2
