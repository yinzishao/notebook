"""

给定一个m x n 二维字符网格board 和一个字符串单词word 。如果word 存在于网格中，返回 true ；否则，返回 false 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/word-search
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


"""
from typing import List

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/word-search/solution/dan-ci-sou-suo-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def check(i: int, j: int, k: int) -> bool:
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True

            visited.add((i, j))
            result = False
            for di, dj in directions:
                newi, newj = i + di, j + dj
                if 0 <= newi < len(board) and 0 <= newj < len(board[0]):
                    if (newi, newj) not in visited:
                        if check(newi, newj, k + 1):
                            result = True
                            break
            # 访问过后，都不能找到相应的字符，需要移除访问过的标识，因为可以匹配另外的字序列
            visited.remove((i, j))
            return result

        h, w = len(board), len(board[0])
        visited = set()
        for i in range(h):
            for j in range(w):
                if check(i, j, 0):
                    return True

        return False


"""
https://leetcode-cn.com/problems/word-search/solution/shou-hua-tu-jie-79-dan-ci-sou-suo-dfs-si-lu-de-cha/770471
"""


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        used = [[False] * n for _ in range(m)]

        def dfs(row, col, i):  # 判断当前点是否是目标路径上的点. row col 当前点的坐标，i当前考察的word字符索引
            if i == len(word):  # 递归结束条件 : 找到了单词的最后一个
                return True
            if row < 0 or row >= m or col < 0 or col >= n:  # 越界
                return False
            if used[row][col] or board[row][col] != word[i]:  # 已经访问过,或者不是word里的字母
                return False
            # 排除掉上面的false情况，当前点是合格的，可以继续递归考察
            used[row][col] = True  # 记录一下当前点被访问了
            if dfs(row + 1, col, i + 1) or \
                dfs(row - 1, col, i + 1) or \
                dfs(row, col + 1, i + 1) or \
                dfs(row, col - 1, i + 1):  # 基于当前点[row,col]，可以为剩下的字符找到路径
                return True
            used[row][col] = False  # 不能为剩下字符找到路径，返回false，撤销当前点的访问状态，继续考察别的分支
            return False

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0] and dfs(i, j, 0):
                    return True
        return False
