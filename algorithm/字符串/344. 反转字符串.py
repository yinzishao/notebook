"""
编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。

不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。

你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。



示例 1：

输入：["h","e","l","l","o"]
输出：["o","l","l","e","h"]
示例 2：

输入：["H","a","n","n","a","h"]
输出：["h","a","n","n","a","H"]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
import random
from typing import List


class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        冒泡！超时
        """
        length = len(s)
        for i in range(length):
            for j in range(length - i - 1):
                s[j], s[j + 1] = s[j + 1], s[j]
        return s


input = [random.randint(1, 20) for _ in range(0, 10)]
input = [4, 1, 10, 9, 1, -1, -21, -12]

input = [-1, 2, -8, -10]
print(f"input {input} ,result {Solution().reverseString(input)}")


class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        l = 0
        r = len(s) - 1
        while l < r:
            s[l], s[r] = s[r], s[l]
            l += 1
            r -= 1
        return s


print(f"input {input} ,result {Solution().reverseString(input)}")
