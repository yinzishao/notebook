"""
https://leetcode-cn.com/problems/qing-wa-tiao-tai-jie-wen-ti-lcof/


一只青蛙一次可以跳上1级台阶，也可以跳上2级台阶。求该青蛙跳上一个 n级的台阶总共有多少种跳法。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/qing-wa-tiao-tai-jie-wen-ti-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


class Solution:
    def numWays(self, n: int) -> int:
        if n == 1 or n < 1:
            return 1
        if n == 2:
            return 2
        return self.numWays(n - 1) + self.numWays(n - 2)


# print(Solution().numWays(2))


class Solution:
    def numWays(self, n: int) -> int:
        i, j = 0, 1
        while n > 0:
            i, j = j, i + j
            n -= 1
        return j % 1000000007


print(Solution().numWays(44))

"""
可以跳3格呢？
"""
print('--可以跳3格呢？')


class Solution:
    def numWays(self, n: int) -> int:
        # i, j = 0, [1, 2, 3]
        i, j = 0, [1, 2, 4]
        # 注意第3格的跳法是4 = f(0) + f(1) + f(2) 而不是3!
        while n > 0:
            j.append(sum(j))
            i = j.pop(0)
            n -= 1
        return i % 1000000007


print(Solution().numWays(5))

"""
可以跳n格呢？

链接：https://www.nowcoder.com/questionTerminal/22243d016f6b47f2a6928b4313c85387
来源：牛客网

5) n = n时，会有n中跳的方式，1阶、2阶...n阶，得出结论：

    f(n) = f(n-1)+f(n-2)+...+f(n-(n-1)) + f(n-n) => f(0) + f(1) + f(2) + f(3) + ... + f(n-1)


6) 由以上已经是一种结论，但是为了简单，我们可以继续简化：

    f(n-1) = f(0) + f(1)+f(2)+f(3) + ... + f((n-1)-1) = f(0) + f(1) + f(2) + f(3) + ... + f(n-2)

    f(n) = f(0) + f(1) + f(2) + f(3) + ... + f(n-2) + f(n-1) = f(n-1) + f(n-1)

    可以得出：

    f(n) = 2*f(n-1)


7) 得出最终结论,在n阶台阶，一次有1、2、...n阶的跳的方式时，总得跳法为：

          | 1       ,(n=0 )

f(n) =    | 1       ,(n=1 )

          | 2*f(n-1),(n>=2)
"""


class Solution:
    def numWays(self, n: int) -> int:
        i, j = 0, 1
        while n > 1:
            i, j = 1, j * 2
            n -= 1
        return j
        # return 2 ** (n - 1)


print(Solution().numWays(3))

"""
毒蘑菇 最大体力

https://codetop.cc/#/discuss/16

跳台阶 一共n节台阶一次可以跳任意节，每跳一节消耗一点体力，起始体力为m，每节台阶上都有一个蘑菇，当跳到一节台阶上就会吃掉这个台阶上的蘑菇，蘑菇的效果可能是增加体力也可能是减少体力，由一个长度为n的数组array代表每一节上的蘑菇的效果（正数为增加体力， 负数为减少体力）求到达最后的台阶时的最大体力值为多少（如果无法到达最后一节则返回-1）


题解一， 个人感觉是错误的

题是leetcode 55. 跳跃游戏  的变形：https://leetcode-cn.com/problems/jump-game/

https://blog.csdn.net/weixin_39590058/article/details/112607484


题解二，思路和我的一致

作者：牛客AlexYao
链接：https://www.nowcoder.com/discuss/413599?type=1
来源：牛客网

解题思路：
第一步：先举一个简单的例子，初始体力为 m，一个长度为 6 的方块（即长度为 6 的list）：[1, 2, -1, 2, 3, 4]，跳到第一个上面，当前体力为 m+1-1，再跳到第二个上面，体力为 m+1-1+2-1，那么可以得出，只要数字大于等于1，那么都应该往这个方块上跳。
第二步：这个人当前体力为m，离这个人目前位置最近的下一个 >=1 的数字（x）与这个人当前的距离（d），如果d>m+x，则无法到达终点，如果不存在这样的问题，则可以到达终点，最大的体力即所有大于等于1的数字相加，加上初始体力m，再减去方块数量n。因为面试官说是从地上跳上去的，所以跳到第一个上面也需要消耗一个体力，因为总木块数量为n，所以当到达终点时，一共消耗的体力为 n。

"""
