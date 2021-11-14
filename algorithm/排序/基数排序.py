"""

基数排序：
先从个位数进行排序，得到个位数的顺序列表
后进行十位数进行排序，因为个位数是有序的，所以十位数有序后，后面的位数也就有序了
以此类推。

最高位优先法与最低位优先法

时间复杂度 o(rd)

"""
import random


def radix_sort(nums):
    max_value = max(nums)
    # 找出最大值的位数。注意负数的问题!
    max_digit = max(len(str(max(nums))), len(str(abs(min(nums)))))
    # print(max_digit)

    # # 其他方法获取最大位数， 无法解决负数的问题
    # max_digit = 1
    # # 注意是<=
    # while 10**max_digit <= max_value:
    #     max_digit = max_digit + 1

    i = 0
    # 从个位出发开始进行排序
    while i < max_digit:
        # 声明20个数字的数组, 包含负数的情况
        res = [[] for _ in range(20)]
        # 获取位数上面的数
        for one in nums:
            if one > 0:
                idx = one // (10 ** i) % 10 + 10
            else:
                # 注意负数的情况。 负数 //有问题。直接/取整得到
                # -10的模得到其真正的位数值（负数），然后加上10，让越小的数的位置越左。而不是取正数
                # int( -173 / 10) % -10 = -7
                idx = int(one / (10 ** i)) % -10 + 10
                # 也可以通过取正后计算
                # idx = 10 - (abs(one) // (10 ** i) % 10)
            # 依次添加到位数上
            res[idx].append(one)
        new_num = []
        # 遍历最外层数组，保证了低位的顺序性，然后新一轮的高位数任务，低位数教小的会先放进去的
        # 所以直接按顺序遍历就能够得到有序
        for a in res:
            for b in a:
                new_num.append(b)
        nums = new_num
        i += 1
    return nums


input = [random.randint(1, 20) for _ in range(0, 10)]
# 无法处理有负数的例子， 注意负数取于取模问题， 注意有负数查找最大位数的长度逻辑
input = [4, 1, 10, 9, 1, -1, -21, -12]

input = [-1, 2, -8, -10]
print(f"input {input} ,result {radix_sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 100) for _ in range(-20, 20)]
    o1 = radix_sort(input)
    o2 = sorted(input)
    assert o1 == o2
