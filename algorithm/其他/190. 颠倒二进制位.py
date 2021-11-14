"""
颠倒给定的 32 位无符号整数的二进制位。
"""

from notebook.algorithm.utils import check


class Solution:
    def reverseBits(self, n: int) -> int:
        # 注意32位
        b = list('{:032b}'.format(n))
        l = 0
        r = len(b) - 1
        while l < r:
            b[l], b[r] = b[r], b[l]
            l += 1
            r -= 1
        return int(''.join(b), 2)


# int('11111111111111111111111111111101',2)
check(Solution().reverseBits, [4294967293], 3221225471)

"""
题解：位运算
将 n 视作一个长为 32 的二进制串，从低位往高位枚举 n 的每一位，将其倒序添加到翻转结果 \textit{rev}rev 中。

代码实现中，每枚举一位就将 n 右移一位，这样当前 n 的最低位就是我们要枚举的比特位。当 n 为 0 时即可结束循环。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reverse-bits/solution/dian-dao-er-jin-zhi-wei-by-leetcode-solu-yhxz/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

print("位运算")


class Solution:
    def reverseBits(self, n: int) -> int:
        # 注意32位
        res = 0
        for i in range(0, 32):
            # 错误，注意运算顺序
            # res |= n & 1 << (31 - i)
            res |= (n & 1) << (31 - i)
            n >>= 1
        return res


# int('11111111111111111111111111111101',2)
check(Solution().reverseBits, [4294967293], 3221225471)


class Solution:
    def reverseBits(self, n: int) -> int:
        # 注意32位
        res = 0
        for i in range(0, 32):
            res = (res << 1) | (n >> i & 1)
        return res


# int('11111111111111111111111111111101',2)
check(Solution().reverseBits, [4294967293], 3221225471)

"""

32位无符号整数，如 1111 1111 1111 1111 1111 1111 1111 1111
表示成16进制        f    f    f    f    f    f    f   f

"""

print("分治法")
"""

作者：fuxuemingzhu
链接：https://leetcode-cn.com/problems/reverse-bits/solution/fu-xue-ming-zhu-xun-huan-yu-fen-zhi-jie-hoakf/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。"""


class Solution:
    # @param n, an integer
    # @return an integer
    def reverseBits(self, n):
        n = (n >> 16) | (n << 16)
        n = ((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8)
        n = ((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4)
        n = ((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2)
        n = ((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1)
        return n


# int('11111111111111111111111111111101',2)
check(Solution().reverseBits, [4294967293], 3221225471)
