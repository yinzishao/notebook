"""
给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

 

示例 1：

输入：grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
输出：1
示例 2：

输入：grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
输出：3

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-islands
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
import collections
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """错误的题解"""
        nums = 0
        for w, i in enumerate(grid):
            for l, j in enumerate(i):
                if j == '1':
                    # 这里的遍历有误，因为只会往左边和上边拿，但是右边可能也会让岛屿连成
                    if not ((w - 1 >= 0 and grid[w - 1][l] == '1') or (l - 1 >= 0 and grid[w][l - 1] == '1')):
                        nums += 1
        return nums


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """错误的题解"""
        nums = 0
        for w, i in enumerate(grid):
            for l, j in enumerate(i):
                if j == '1':
                    # 这里的遍历有误，因为只会往左边和上边拿，但是右边可能也会让岛屿连成
                    if not ((w - 1 >= 0 and grid[w - 1][l] == '1') or (l - 1 >= 0 and grid[w][l - 1] == '1')):
                        # 如果左边和上边都没有1，那么应该可以独立成岛屿
                        nums += 1
                    # 广度遍历： 但是如果左边是独立的岛屿，应该要合在一起，减一? 如何区分？
                    if l - 1 >= 0 and nums[w][l] == '1':
                        pass

        return nums


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        width = len(grid)
        length = len(grid[0])
        visited = [[0] * length for _ in range(width)]

        def check(i, j):
            if i < 0 or j < 0 or i >= width or j >= length or visited[i][j]:
                return 0
            visited[i][j] = 1
            if grid[i][j] == '1':
                # 深度遍历：递归找出所有的该片该岛屿的所有节点
                check(i - 1, j)
                check(i + 1, j)
                check(i, j + 1)
                check(i, j - 1)
                return 1
            return 0

        result = 0

        for w in range(width):
            for l in range(length):
                if grid[w][l] == '1':
                    # 深度遍历：递归找出所有的该片该岛屿的所有节点
                    # 题解的思路，是直接result += check(w, l) 可以直接简单些，如果不符合返回0
                    result += check(w, l)
                    # if not visited[w][l]:
                    #     result += 1
                    # check(w, l)
        return result


inp = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]

result = Solution().numIslands(inp)
assert result == 3, result

inp = [["1"]]
result = Solution().numIslands(inp)
assert result == 1, result
inp = [
    ["1", "1", "1"],
    ["0", "1", "0"],
    ["1", "1", "1"]
]
result = Solution().numIslands(inp)
assert result == 1, result


class Solution:

    def numIslands(self, grid: List[List[str]]) -> int:
        count = 0
        for r in range(0, len(grid), 1):
            for c in range(0, len(grid[0]), 1):
                if grid[r][c] == '1':
                    count += self.dfs(grid, r, c)
        return count

    def dfs(self, grid, r, c):
        # 不在格子中,岛屿边界
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
            return 0
        # 该格子不是1陆地
        if grid[r][c] != '1':
            return 0

        # 将格子标记为「已遍历过」
        grid[r][c] = '2'
        # 访问上、下、左、右四个相邻结点
        self.dfs(grid, r - 1, c)
        self.dfs(grid, r + 1, c)
        self.dfs(grid, r, c - 1)
        self.dfs(grid, r, c + 1)
        return 1


"""
同样地，我们也可以使用广度优先搜索代替深度优先搜索。

为了求出岛屿的数量，我们可以扫描整个二维网格。如果一个位置为 1，则将其加入队列，开始进行广度优先搜索。在广度优先搜索的过程中，每个搜索到的 1 都会被重新标记为 0。直到队列为空，搜索结束。

最终岛屿的数量就是我们进行广度优先搜索的次数。

作者：LeetCode
链接：https://leetcode-cn.com/problems/number-of-islands/solution/dao-yu-shu-liang-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        nr = len(grid)
        if nr == 0:
            return 0
        nc = len(grid[0])

        num_islands = 0
        for r in range(nr):
            for c in range(nc):
                if grid[r][c] == "1":
                    num_islands += 1
                    grid[r][c] = "0"
                    neighbors = collections.deque([(r, c)])
                    while neighbors:
                        row, col = neighbors.popleft()
                        for x, y in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                            if 0 <= x < nr and 0 <= y < nc and grid[x][y] == "1":
                                neighbors.append((x, y))
                                grid[x][y] = "0"

        return num_islands
