"""
堆排序的基本思想是：将待排序序列构造成一个大顶堆，此时，整个序列的最大值就是堆顶的根节点。将其与末尾元素进行交换，此时末尾就为最大值。然后将剩余n-1个元素重新构造成一个堆，这样会得到n个元素的次小值。如此反复执行，便能得到一个有序序列了

https://www.cnblogs.com/chengxiao/p/6129630.html
"""
import random


def heapify(n, i, l):
    """对堆里面的某个元素进行重建堆"""
    # 注意下一层左右的计算
    left = 2 * i + 1
    right = 2 * i + 2
    tmp = i
    # 堆化先找出节点的三个元素的最大值
    if left < l and n[left] > n[i]:
        tmp = left
    if right < l and n[right] > n[tmp]:
        tmp = right
    if tmp != i:
        # 最大值进行交换
        n[tmp], n[i] = n[i], n[tmp]
        # 交换后的元素的这个节点需要下沉，
        # 以便能符合堆的规则。方便移动堆头元素后的下一次的比较能快速完成。
        heapify(n, tmp, l)


def heap_sort(n):
    # print(f'input: {input}')
    # 构建堆。从中间的元素往前开始。
    for i in range(int(len(n) / 2))[::-1]:
        # 遍历各个节点完成堆化。
        heapify(n, i, len(n))
    # 完成初始堆的构建
    l = len(n) - 1
    for i in range(len(n)):
        # print(n, l)
        # 移动堆头，收缩减1,。上面已经减一了。
        n[0], n[l] = n[l], n[0]
        # 从移动的堆头开始。重新下沉
        heapify(n, 0, l)
        l -= 1
    return n


input = [random.randint(1, 20) for _ in range(0, 10)]
# input = [4, 1, 10, 9, 1]
print(f"input {input} ,result {heap_sort(input)}")
#
# for i in range(0, 50):
#     input = [random.randint(1, 1000) for _ in range(0, 50)]
#     print(f'{input}')
#     o1 = heap_sort(input)
#     o2 = sorted(input)
#     assert o1 == o2
