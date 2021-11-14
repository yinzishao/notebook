"""
给定两个字符串, A 和 B。

A 的旋转操作就是将 A 最左边的字符移动到最右边。 例如, 若 A = 'abcde'，在移动一次之后结果就是'bcdea' 。如果在若干次旋转操作之后，A 能变成B，那么返回True。

示例 1:
输入: A = 'abcde', B = 'cdeab'
输出: true

示例 2:
输入: A = 'abcde', B = 'abced'
输出: false

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/rotate-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


class Solution:
    def rotateString(self, A: str, B: str) -> bool:
        if len(A) != len(B):
            return False
        if not A and not B:
            return True
        # 第一个开头的字符不一定就是旋转后的首个字符
        # a = "bbbacddceeb"
        # b = "ceebbbbacdd"
        start_idx = A.find(B[0])
        if start_idx < 0:
            return False
        length = len(B)
        for idx, val in enumerate(B):
            # 找出开头
            if A[(start_idx + idx) % length] != val:
                return False
        return True


print(Solution().rotateString("abcde", "cdeab"))
a = "bbbacddceeb"
b = "ceebbbbacdd"
print(Solution().rotateString(a, b))

"""
问题转变为b是不是A*2的子串匹配！

那我们就可以引申答出 KMP，SUNDAY，BF 等字符串匹配策略。
"""


class Solution:
    def rotateString(self, A: str, B: str) -> bool:
        if len(A) != len(B):
            return False
        A = A * 2
        if A.find(B) >= 0:
            return True
        return False


print('-------')
print(Solution().rotateString("abcde", "cdeab"))
a = "bbbacddceeb"
b = "ceebbbbacdd"
print(Solution().rotateString(a, b))

"""
这道题目最容易想到的解法，其实就是跟着题意来。每次将旋转后的A和目标串对比
"""
