"""
给你一个字符串 S、一个字符串 T，请在字符串 S 里面找出：包含 T 所有字符的最小子串。

示例：

输入: S = "ADOBECODEBANC", T = "ABC"
输出: "BANC"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-window-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
import collections


class Solution(object):
    def minWindow(self, s, t):
        """
        错误版本：
        如何判断窗口符合字符的数据。set不能，因为会有去重， 没有重复的字数的限制了。反例：aa aa   bba baa
        """
        left = 0
        right = len(t)
        s_l = len(s)
        if s_l < right:
            return ''
        result = s
        t_s = set(t)
        flag = False
        while left < right:
            w = s[left:right]
            windows = set(s[left:right])
            if not t_s.issubset(windows):
                if right == s_l:
                    left += 1
                else:
                    right += 1
            else:
                if len(windows) <= len(result) and len(w) >= len(t):
                    result = w
                    flag = True
                left += 1
        return result if flag else ''


S = "ADOBECODEBANC"
T = "ABC"


# print(Solution().minWindow(S, T))
# print(Solution().minWindow('a', 'a'))
# print(Solution().minWindow('a', 'aa'))
# print(Solution().minWindow('a', 'b'))
# print(Solution().minWindow('ab', 'A'))
# print(Solution().minWindow('aa', 'aa'))
# print(Solution().minWindow('bbaa', 'aba'))  # bba or baa


class Solution2:
    """
    用Counter进行比较。
    判断窗口的k和频次是否对得上:
    all(map(lambda x: lookup[x] >= t[x], t.keys()))
    滑动的时候，开头的k的频次-=1
    """

    def minWindow(self, s, t):
        from collections import Counter
        t = Counter(t)
        lookup = Counter()
        start = 0
        end = 0
        min_len = float("inf")
        res = ""
        while end < len(s):
            lookup[s[end]] += 1
            end += 1
            # print(start, end)
            while all(map(lambda x: lookup[x] >= t[x], t.keys())):
                if end - start < min_len:
                    res = s[start:end]
                    min_len = end - start
                lookup[s[start]] -= 1
                start += 1
        return res


# print(Solution2().minWindow('bbaa', 'aba'))  # bba or baa

"""
作者：powcai
链接：https://leetcode-cn.com/problems/minimum-window-substring/solution/hua-dong-chuang-kou-by-powcai-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution3:
    def minWindow(self, s: str, t: str) -> str:
        # 需要一个存储字符与出现次数的结构
        # 难点如何判断窗口内是否满足覆盖子串？
        # 要对比t的counter与窗口的counter一致？时间复杂度是？
        # 如果是直接遍历hash的key比较，时间复杂度是o(c*n)
        # 两个hash
        res = ''
        l = 0

        for i in s:
            # 如果字符存在于t，并且使得窗口内满足的字符覆盖子串
            # 窗口左边界进行滑动，达到最后一个使窗口无法满足条件的新边界
            # 并且比较是否是最短的结果
            # 否则往右滑动
            pass
        return res


class Solution3:
    """
    通过一个need_dict存储需要匹配的字符次数。可以是负数
    然后通过一个need_length来判断覆盖是否完成。只有

    但覆盖完成时候，需要滑动左边窗口，让其不能满足覆盖为止。



    """
    def minWindow(self, s: str, t: str) -> str:
        # 需要一个存储字符与出现次数的结构
        res = ''
        l = 0
        need_dict = collections.defaultdict(int)
        need_length = len(t)
        for i in t:
            need_dict[i] += 1
        for idx, i in enumerate(s):
            if need_dict[i] > 0:
                need_length -= 1
            need_dict[i] -= 1
            # 如何判断need_dict[i]==0的情况下是否是覆盖字串呢？需要一个长度判断
            # if need_dict[i] == 0:
            if need_length == 0:
                # 左边滑动，并且让窗口不能满足覆盖字串
                while True and l <= idx:
                    # 左边滑动的字符需要加1
                    need_dict[s[l]] += 1
                    # 如果长度比结果小，则是替换。
                    # 优化点是如题解那样，先跳到要失效的左边窗口
                    if len(res) == 0 or (idx - l + 1) < len(res):
                        res = s[l:idx + 1]
                    # 是匹配的字符，并且需要匹配了，则结束循环
                    if s[l] in t and need_dict[s[l]] > 0:
                        l += 1
                        need_length += 1
                        break
                    l += 1
        return res


print('Solution3')
S = "ADOBECODEBANC"
T = "ABC"
a = Solution3().minWindow(S, T)
print(a)
assert a == "BANC"
print(Solution3().minWindow('bbaa', 'aba'))  # bba or baa

"""

作者：Mcdull0921
链接：https://leetcode-cn.com/problems/minimum-window-substring/solution/tong-su-qie-xiang-xi-de-miao-shu-hua-dong-chuang-k/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


def minWindow(self, s: str, t: str) -> str:
    need = collections.defaultdict(int)
    for c in t:
        need[c] += 1
    needCnt = len(t)
    i = 0
    res = (0, float('inf'))
    for j, c in enumerate(s):
        if need[c] > 0:
            needCnt -= 1
        need[c] -= 1
        if needCnt == 0:  # 步骤一：滑动窗口包含了所有T元素
            while True:  # 步骤二：增加i，排除多余元素
                c = s[i]
                # 直接通过==0就能判断是因为没有+1前，不是t的总不能达到0。只有t里面的元素才能是0。而且当其等于0的时候，才是最短的时候。
                if need[c] == 0:
                    break
                need[c] += 1
                i += 1
            if j - i < res[1] - res[0]:  # 记录结果
                res = (i, j)
            need[s[i]] += 1  # 步骤三：i增加一个位置，寻找新的满足条件滑动窗口
            needCnt += 1
            i += 1
    return '' if res[1] > len(s) else s[res[0]:res[1] + 1]  # 如果res始终没被更新过，代表无满足条件的结果
