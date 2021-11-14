"""
https://leetcode-cn.com/problems/zigzag-conversion/

将一个给定字符串根据给定的行数，以从上往下、从左到右进行 Z 字形排列。

比如输入字符串为 "LEETCODEISHIRING" 行数为 3 时，排列如下：

L   C   I   R
E T O E S I I G
E   D   H   N
之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如："LCIRETOESIIGEDHN"。

请你实现这个将字符串进行指定行数变换的函数：

string convert(string s, int numRows);

"""


class Solution:
    def convert(self, s: str, num_rows: int) -> str:
        l, s_l = len(s), list(s)
        result = []
        for i in range(num_rows):
            idx = i
            if i in [0, num_rows-1]:
                while idx < l:
                    result.append(s_l[idx])
                    # 需要注意num_rows少于3的场景，因为-2不是正数，会导致循环。
                    idx += num_rows + max((num_rows - 2), 0)
            else:
                while idx < l:
                    result.append(s_l[idx])
                    idx += num_rows + (num_rows - 2)
                    if (idx - 2 * i) < l:
                        result.append(s_l[idx - 2 * i])
        return ''.join(result)


s = "LEETCODEISHIRING"
num_rows = 4
assert "LDREOEIIECIHNTSG" == Solution().convert(s, num_rows)
num_rows = 3
assert "LCIRETOESIIGEDHN" == Solution().convert(s, num_rows)
s = "A"
num_rows = 1
assert "A" == Solution().convert(s, num_rows)
num_rows = 1
s = "AB"
assert "AB" == Solution().convert(s, num_rows)
