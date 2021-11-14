"""
n 皇后问题 研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 n ，返回所有不同的 n 皇后问题 的解决方案。

每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

皇后彼此不能相互攻击，也就是说：任何两个皇后都不能处于同一条横行、纵行或斜线上。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/n-queens
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from copy import deepcopy
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        res = [[0 for _ in range(n)] for _ in range(n)]

        def is_valid(row, col):
            for i in range(n):
                for j in range(n):
                    # 要避免，要先判断再置值
                    if i == row and j == col:
                        continue
                    if i == row or j == col or abs(i - row) == abs(j - col):
                        if res[i][j] == 1:
                            return False
            return True
            # 怎么判断斜的？

        def back(start, row, col):
            if not is_valid(row, col):
                return
            if start == n:
                # 因为传进来start会是n，所以要加判断
                # 题解的是在传进来之前进行判断。也就是该位置是否可以放置
                # 这样的好处就是上面的is_valid也不用略过位置这种操作
                result.append(deepcopy(res))
                return
            for i in range(n):
                res[start][i] = 1
                back(start + 1, start, i)
                res[start][i] = 0

        back(0, 0, 0)
        ans = []
        for one in result:
            one_list = []
            for i in one:
                res = ''
                for j in i:
                    if j == 0:
                        res += '.'
                    else:
                        res += 'Q'
                one_list.append(res)
            ans.append(one_list)
        return ans


check(Solution().solveNQueens, [4], [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']])

"""
执行结果：通过
显示详情
执行用时：576 ms , 在所有 Python3 提交中击败了 5.01% 的用户
内存消耗： 15.9 MB , 在所有 Python3 提交中击败了 5.11% 的用户

"""

print("官方题解")
"""
为了降低总时间复杂度，每次放置皇后时需要快速判断每个位置是否可以放置皇后，显然，最理想的情况是在 O(1) 的时间内判断该位置所在的列和两条斜线上是否已经有皇后。

因此使用行下标与列下标之差即可明确表示每一条方向一的斜线。

因此使用行下标与列下标之和即可明确表示每一条方向二的斜线。

每次放置皇后时，对于每个位置判断其是否在三个集合中，如果三个集合都不包含当前位置，则当前位置是可以放置皇后的位置。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/n-queens/solution/nhuang-hou-by-leetcode-solution/

"""


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        def generateBoard():
            board = list()
            for i in range(n):
                row[queens[i]] = "Q"
                board.append("".join(row))
                row[queens[i]] = "."
            return board

        def backtrack(row: int):
            if row == n:
                board = generateBoard()
                solutions.append(board)
            else:
                for i in range(n):
                    if i in columns or row - i in diagonal1 or row + i in diagonal2:
                        continue
                    queens[row] = i
                    columns.add(i)
                    diagonal1.add(row - i)
                    diagonal2.add(row + i)
                    backtrack(row + 1)
                    columns.remove(i)
                    diagonal1.remove(row - i)
                    diagonal2.remove(row + i)

        solutions = list()
        queens = [-1] * n
        columns = set()
        diagonal1 = set()
        diagonal2 = set()
        row = ["."] * n
        backtrack(0)
        return solutions


"""

这个问题本质上跟全排列问题差不多，决策树的每一层表示棋盘上的每一行；每个节点可以做出的选择是，在该行的任意一列放置一个皇后。

因为是一行行下去操作，可以通过判断左上角和右上角的。无须行下面的判断。

https://leetcode-cn.com/problems/n-queens/solution/nhuang-hou-jing-dian-hui-su-suan-fa-tu-wen-xiang-j/
"""

print("另一种检查")


class Solution:
    def valid(self, chess, row, col, n):
        # 坐标位置垂直列上是否重复
        for i in range(row):
            if chess[i][col] == 'Q':
                return False
        # 坐标右上角是否重复
        for (i, j) in zip(range(row - 1, -1, -1), range(col + 1, n)):
            if chess[i][j] == 'Q':
                return False
        # 坐标左上角是否重复
        for (i, j) in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if chess[i][j] == 'Q':
                return False
        return True

    def construct(self, chess, n):
        newchess = []
        for i in range(n):
            newchess.append(''.join(chess[i]))
        return newchess

    def solveNQueens(self, n: int) -> List[List[str]]:
        chess = [["."] * n for _ in range(n)]
        res = []

        def solve(chess, row):
            if row == n:
                res.append(self.construct(chess, n))
                return
            for col in range(n):
                # 先判断再递归
                if self.valid(chess, row, col, n):
                    chess[row][col] = 'Q'
                    solve(chess, row + 1)
                    chess[row][col] = '.'

        solve(chess, 0)
        return res


check(Solution().solveNQueens, [4], [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']])
