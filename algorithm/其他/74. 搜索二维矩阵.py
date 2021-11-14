"""
编写一个高效的算法来判断 m x n 矩阵中，是否存在一个目标值。该矩阵具有如下特性：

每行中的整数从左到右按升序排列。
每行的第一个整数大于前一行的最后一个整数。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/search-a-2d-matrix
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

剑指offer
ref: notebook/algorithm/剑指offer/3_search-a-2d-matrix/__init__.py:6
"""
from typing import List

from notebook.algorithm.utils import check


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        res = []
        length = 0
        # !: 这里进行了遍历不就是o(n)了么!直接判断就得了--
        # 二分是要o(log(n))
        for i in matrix:
            for j in i:
                res.append(j)
                length += 1
        l = 0
        r = length - 1
        # 二分的结束条件是什么？
        while l <= r:
            mid = int((r + l) / 2)
            if res[mid] == target:
                return True
            if res[mid] > target:
                r = mid - 1
            else:
                l = mid + 1
        return False


matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
target = 20

check(Solution().searchMatrix, [matrix, target], True)


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row_len = len(matrix)
        col_len = len(matrix[0])
        l = 0
        r = col_len * row_len - 1
        while l <= r:
            mid = int((l + r) / 2)
            row = mid // col_len
            col = mid % col_len
            if matrix[row][col] == target:
                return True
            if matrix[row][col] > target:
                r = mid - 1
            else:
                l = mid + 1
        return False


matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
target = 203

check(Solution().searchMatrix, [matrix, target], True)

"""

作者：AC_OIer
链接：https://leetcode-cn.com/problems/search-a-2d-matrix/solution/gong-shui-san-xie-yi-ti-shuang-jie-er-fe-l0pq/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) >> 1
            x, y = mid // n, mid % n
            if matrix[x][y] > target:
                r = mid - 1
            elif matrix[x][y] < target:
                l = mid + 1
            else:
                return True
        return False


"""

那么我们可以从根（右上角）开始搜索，如果当前的节点不等于目标值，可以按照树的搜索顺序进行：

当前节点「大于」目标值，搜索当前节点的「左子树」，也就是当前矩阵位置的「左方格子」，即 y--
当前节点「小于」目标值，搜索当前节点的「右子树」，也就是当前矩阵位置的「下方格子」，即 x++

时间复杂度：O(m+n)
空间复杂度：O(1)

作者：AC_OIer
链接：https://leetcode-cn.com/problems/search-a-2d-matrix/solution/gong-shui-san-xie-yi-ti-shuang-jie-er-fe-l0pq/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        x, y = 0, n - 1
        while x < m and y >= 0:
            if matrix[x][y] > target:
                y -= 1
            elif matrix[x][y] < target:
                x += 1
            else:
                return True
        return False
