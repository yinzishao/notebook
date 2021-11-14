"""
给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

示例:

输入: n = 4, k = 2
输出:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/combinations
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result = []

        def backtrack(start, path):

            if len(path) == k:
                result.append(path[::])
                return
            for j in range(start, n):
                # j+1 是因为数值是从一开始
                path.append(j + 1)
                # j+1 是因为递归的路径只能往后面拿
                # 达到去重复的目的
                backtrack(j + 1, path)
                path.pop()

        backtrack(0, [])
        return result


check(Solution().combine, [4, 2], [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])

print("题解")
"""
题解： https://leetcode-cn.com/problems/combinations/solution/hui-su-suan-fa-jian-zhi-python-dai-ma-java-dai-ma-/
上面还可以加入剪枝
if n-start+1<level:return #如果start->n的数不够组合数的话，则这条路径没有答案

也不需要每次都判断长度
"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result = []

        def backtrack(start, path, level):
            # 如果start->n的数不够组合数的话，则这条路径没有答案
            if n - start + 1 < level:
                return
            if level == 0:
                result.append(path[::])
                return
            for j in range(start, n):
                # j+1 是因为数值是从一开始
                path.append(j + 1)
                # j+1 是因为递归的路径只能往后面拿
                # 达到去重复的目的
                backtrack(j + 1, path, level - 1)
                path.pop()

        backtrack(0, [], k)
        return result


check(Solution().combine, [4, 2], [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
