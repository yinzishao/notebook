"""
给你一个字符串 s ，仅反转字符串中的所有元音字母，并返回结果字符串。

元音字母包括 'a'、'e'、'i'、'o'、'u'，且可能以大小写两种形式出现。

 

示例 1：

输入：s = "hello"
输出："holle"
示例 2：

输入：s = "leetcode"
输出："leotcede"


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-vowels-of-a-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        s = [i for i in s]
        l = len(s)
        start, end = 0, l - 1
        hit = ['a', 'e', 'i', 'o', 'u']
        while start <= end:
            while start <= end and s[start].lower() not in hit:
                start += 1
            while start <= end and s[end].lower() not in hit:
                end -= 1
            if start < end:
                s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1
        return ''.join(s)


print(Solution().reverseVowels('hello'))
assert 'holle' == Solution().reverseVowels('hello')
print(Solution().reverseVowels('leetcode'))
assert 'leotcede' == Solution().reverseVowels('leetcode')
print(Solution().reverseVowels('""'))

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reverse-vowels-of-a-string/solution/fan-zhuan-zi-fu-chuan-zhong-de-yuan-yin-2bmos/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        def isVowel(ch: str) -> bool:
            return ch in "aeiouAEIOU"

        n = len(s)
        s = list(s)
        i, j = 0, n - 1
        while i < j:
            while i < n and not isVowel(s[i]):
                i += 1
            while j > 0 and not isVowel(s[j]):
                j -= 1
            if i < j:
                s[i], s[j] = s[j], s[i]
                i += 1
                j -= 1

        return "".join(s)
