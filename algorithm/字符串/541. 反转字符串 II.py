"""
给定一个字符串 s 和一个整数 k，从字符串开头算起，每 2k 个字符反转前 k 个字符。

如果剩余字符少于 k 个，则将剩余字符全部反转。
如果剩余字符小于 2k 但大于或等于 k 个，则反转前 k 个字符，其余字符保持原样。


示例 1：

输入：s = "abcdefg", k = 2
输出："bacdfeg"
示例 2：

输入：s = "abcd", k = 2
输出："bacd"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-string-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        s = list(s)

        start = 0
        end = len(s)
        while start < end:
            self.reverse(start, min(start + k - 1, end - 1), s)
            start += 2 * k
        return ''.join(s)

    def reverse(self, start, end, s):
        while start < end:
            s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1


res = Solution().reverseStr('abcdefg', 2)
assert 'bacdfeg' == res, res
res = Solution().reverseStr('abcd', 2)
assert 'bacd' == res, res
res = Solution().reverseStr('abcd', 4)
assert 'dcba' == res, res
res = Solution().reverseStr("abcdefg", 8)
assert 'gfedcba' == res, res

"""


作者：AC_OIer
链接：https://leetcode-cn.com/problems/reverse-string-ii/solution/gong-shui-san-xie-jian-dan-zi-fu-chuan-m-p88f/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        n = len(s)
        s = list(s)
        for l in range(0, n, 2 * k):
            r = l + k - 1
            s = self.swap(l, min(r, n - 1), s)
        return ''.join(s)

    def swap(self, left, right, s):
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
        return s
