"""

给定一个非负整数，你至多可以交换一次数字中的任意两位。返回你能得到的最大值。

示例 1 :

输入: 2736
输出: 7236
解释: 交换数字2和数字7。
示例 2 :

输入: 9973
输出: 9973
解释: 不需要交换。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-swap
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class Solution:
    def maximumSwap(self, num: int) -> int:
        """
        需要把最大值跟第一位交换：
            如果最大值和第一位的数字一样，需要递归？
            如果存在多个最大值，需要优先将最大值的右边交换
        """
        num_str = list(str(num))


class Solution:
    def maximumSwap(self, num: int) -> int:
        num_str = list(str(num))
        char_2_idx = {}
        for idx, char in enumerate(num_str):
            char_2_idx[char] = idx
        for idx, char in enumerate(num_str):
            for n in range(9, 0, -1):
                c = str(n)
                if c in char_2_idx and char_2_idx[c] > idx and n > int(char):
                    num_str[char_2_idx[c]], num_str[idx] = num_str[idx], num_str[char_2_idx[c]]
                    return int(''.join(num_str))
        return int(''.join(num_str))


print(Solution().maximumSwap(2736))
print(Solution().maximumSwap(9973))
print(Solution().maximumSwap(21))

"""
方法二：贪心算法
算法：

我们将计算 last[d]=i，最后一次出现的数字 d（如果存在）的索引 i。
然后，从左到右扫描数字时，如果将来有较大的数字，我们将用最大的数字交换；如果有多个这样的数字，我们将用最开始遇到的数字交换。

作者：LeetCode
链接：https://leetcode-cn.com/problems/maximum-swap/solution/zui-da-jiao-huan-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""

"""
https://leetcode-cn.com/problems/maximum-swap/solution/zui-da-jiao-huan-by-leetcode/165716
方法二的Python3实现，beats 100%（转str空间复杂度还是O(1)吗？？？）
"""


class Solution:
    def maximumSwap(self, num: int) -> int:
        # 先将int转为str，方便遍历
        num_str = str(num)

        # digit_last_index[i] 表示最后出现的索引
        digit_last_index = [None for _ in range(10)]

        # 统计每个数字出现的最后的位置
        for i, digit in enumerate(num_str):
            digit_last_index[int(digit)] = i

        # 从最高位开始，往后面寻找有没有比他大的最大元素
        for i, digit in enumerate(num_str):
            # 从最低位开始寻找
            for index in range(9, int(digit), -1):
                if digit_last_index[index] != None and digit_last_index[index] > i:
                    # digit_last_index[index] 和 i 位置的元素交换(字符串不能修改太坑了...)
                    return num_str[: i] + num_str[digit_last_index[index]] + num_str[i + 1: digit_last_index[index]] + \
                           num_str[i] + num_str[digit_last_index[index] + 1:]
        # 已是最大值就返回原数字
        return num
