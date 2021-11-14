"""
比较相邻的元素。如果第一个比第二个大，就交换他们两个。

对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。

针对所有的元素重复以上的步骤，除了最后一个。

持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。

"""
import random


def sort(n):
    l = len(n)
    for i in range(l):
        for j in range(l - i - 1):
            if n[j] > n[j + 1]:
                n[j + 1], n[j] = n[j], n[j + 1]
    return n


input = [random.randint(1, 20) for _ in range(0, 10)]
print(f"input {input} ,result {sort(input)}")
# input = [19, 15, 7]
# print(f"input {input} ,result {sort(input)}")

for i in range(0, 50):
    input = [random.randint(1, 10000) for _ in range(0, 1000)]
    o1 = sort(input)
    o2 = sorted(input)
    assert o1 == o2
