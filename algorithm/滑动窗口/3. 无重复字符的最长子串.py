"""
给定一个字符串，请你找出其中不含有重复字符的最长子串的长度。

示例1:

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是"wke"，所以其长度为 3。
    请注意，你的答案必须是 子串 的长度，"pwke"是一个子序列，不是子串。
示例 4:

输入: s = ""
输出: 0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from notebook.algorithm.树.utils import check

"""注意是子串！而不是子序列，子序列直接遍历set的长度就是了"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 通过字典维护窗口的重复字符信息
        length = len(s)
        l, r = 0, 0
        info = {}
        flat = True
        res = 0
        while r < length:
            # 向右滑动，直到发现重复
            while flat and r < length:
                key = s[r]
                if key not in info:
                    info[key] = 1
                    # 正常移动记录最大值
                    res = max(len(info), res)
                else:
                    info[key] += 1
                    flat = False
                r += 1
            # 当发现重复，而且左边界往右滑动，收缩窗口。直到无重复。
            # 结束场景： r达到最后发现重复了。一种情况是左边一样，最大长度已经计算了。另一种情况是在中间一样，最大长度肯定比去重后多。
            # 所以可以加上 and r < length
            while not flat and l < length and r < length:
                key = s[l]
                cnt = info.pop(key)
                cnt -= 1
                if cnt == 1:
                    flat = True
                if cnt > 0:
                    info[key] = cnt
                l += 1
        return res


check(Solution().lengthOfLongestSubstring, ["pwwkew"], 3)

"""
题解： 是没有将下一个右窗口放进去，而是发现右窗口的值重复了，进行左窗口的移除。而且左窗口和右窗口都会去到末尾。

同样的思路，可以优化一下自己写的版本的代码。for 遍历的是右边的。而左窗口通过while进行移动。结束条件则是右窗口到末尾就可以了。
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/solution/wu-zhong-fu-zi-fu-de-zui-chang-zi-chuan-by-leetc-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 哈希集合，记录每个字符是否出现过
        occ = set()
        n = len(s)
        # 右指针，初始值为 -1，相当于我们在字符串的左边界的左侧，还没有开始移动
        rk, ans = -1, 0
        for i in range(n):
            if i != 0:
                # 左指针向右移动一格，移除一个字符
                occ.remove(s[i - 1])
            while rk + 1 < n and s[rk + 1] not in occ:
                # 不断地移动右指针
                occ.add(s[rk + 1])
                rk += 1
            # 第 i 到 rk 个字符是一个极长的无重复字符子串
            ans = max(ans, rk - i + 1)
        return ans


"""
一个更优的解，左窗口是可以跳跃的！不用一步一步进行收缩

字典记录的上一个出现字符的下标。当发现重复，直接将左窗口设为当前的上一个重复的下一个。

很取巧的是，这个重复下一个的游标，可以当成右窗口的上一个重复字符的分割线。很独特的维护了一个窗口的范围。

https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/solution/wu-zhong-fu-zi-fu-de-zui-chang-zi-chuan-by-leetc-2/376956
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # k是左窗口下标(不包含)、c_dict是遍历过程中，子母出现的最大下标。
        k, res, c_dict = -1, 0, {}
        # 每次遍历找出该字母是否已经存在，且是在窗口内。
        # 如果在窗口内，则将左边的窗口收缩到当前字母的最大下标处！
        # 否则计算长度。
        # i是右窗口下标。
        for i, c in enumerate(s):
            if c in c_dict and c_dict[c] > k:  # 字符c在字典中 且 上次出现的下标大于当前长度的起始下标
                k = c_dict[c]
                c_dict[c] = i
            else:
                c_dict[c] = i
                res = max(res, i - k)
        return res
