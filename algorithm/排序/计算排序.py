"""
找出原数组中元素值最大的，记为max。

创建一个新数组count，其长度是max加1，其元素默认值都为0。

遍历原数组中的元素，以原数组中的元素作为count数组的索引，以原数组中的元素出现次数作为count数组的元素值。

创建结果数组result，起始索引index。

遍历count数组，找出其中元素值大于0的元素，将其对应的索引作为元素值填充到result数组中去，每处理一次，count中的该元素值减1，直到该元素值不大于0，依次处理count中剩下的元素。

返回结果数组result
"""
import random


def sort(n):
    m = max(n)
    # a = [0 for _ in range(m+1)]
    a = [0] * (m + 1)
    for i in n:
        a[i] += 1
    result = []
    for i, v in enumerate(a):
        while v > 0:
            result.append(i)
            v -= 1
    return result


input = [random.randint(1, 20) for _ in range(0, 10)]
print(f"input {input} ,result {sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 10000) for _ in range(0, 1000)]
    o1 = sort(input)
    o2 = sorted(input)
    assert o1 == o2
