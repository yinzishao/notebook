"""
给定一个m x n 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。

进阶：

一个直观的解决方案是使用 O(mn)的额外空间，但这并不是一个好的解决方案。
一个简单的改进方案是使用 O(m+n) 的额外空间，但这仍然不是最好的解决方案。
你能想出一个仅使用常量空间的解决方案吗？


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/set-matrix-zeroes
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # 一个简单的改进方案是使用 O(m + n) 的额外空间，但这仍然不是最好的解决方案。
        col_set = row_set = set()
        for col, col_val in enumerate(matrix):
            for row, row_val in enumerate(col_val):
                if row_val == 0:
                    col_set.add(col)
                    row_set.add(row)
        for col, col_val in enumerate(matrix):
            for row, row_val in enumerate(col_val):
                if col in col_set or row in row_set:
                    matrix[col][row] = 0


a = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
Solution().setZeroes(a)
assert a == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]


# 你能想出一个仅使用常量空间的解决方案吗？
# 位图？位运算不是O(1)的，因为如果标记数组大小还是跟矩阵大小有关的。注意位图的长度
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        bm = 0
        col_length = len(matrix)
        for col, col_val in enumerate(matrix):
            for row, row_val in enumerate(col_val):
                if row_val == 0:
                    bm |= 1 << (row + col_length)
                    bm |= 1 << col
        for col, col_val in enumerate(matrix):
            for row, row_val in enumerate(col_val):
                if bm & 1 << col or bm & 1 << (row + col_length):
                    matrix[col][row] = 0


a = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
Solution().setZeroes(a)
print(a)
assert a == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

"""
我们可以用矩阵的第一行和第一列代替方法一中的两个标记数组，以达到 O(1)O(1) 的额外空间。但这样会导致原数组的第一行和第一列被修改，无法记录它们是否原本包含 00。因此我们需要额外使用两个标记变量分别记录第一行和第一列是否原本包含 00。

在实际代码中，我们首先预处理出两个标记变量，接着使用其他行与列去处理第一行与第一列，然后反过来使用第一行与第一列去更新其他行与列，最后使用两个标记变量更新第一行与第一列即可。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/set-matrix-zeroes/solution/ju-zhen-zhi-ling-by-leetcode-solution-9ll7/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        # 将行列是否有0，存放在第一行与第一列中。
        m, n = len(matrix), len(matrix[0])
        # 判断第一行或者第一列本身是否有0
        flag_col0 = any(matrix[i][0] == 0 for i in range(m))
        flag_row0 = any(matrix[0][j] == 0 for j in range(n))

        for i in range(1, m):
            for j in range(1, n):
                # 从第二行第二列遍历
                if matrix[i][j] == 0:
                    # 将0的情况放到第一行与第一列中。会改变原来的值，无法判断第一行第一列是否需要改变。所以才有上面的flag_col
                    matrix[i][0] = matrix[0][j] = 0

        # 置空要改变的值
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # 按需置空行列
        if flag_col0:
            for i in range(m):
                matrix[i][0] = 0

        if flag_row0:
            for j in range(n):
                matrix[0][j] = 0


"""
方法三：使用一个标记变量
思路和算法

我们可以对方法二进一步优化，只使用一个标记变量记录第一列是否原本存在 00。这样，第一列的第一个元素即可以标记第一行是否出现 00。但为了防止第一列的第一个元素被提前更新，我们需要从最后一行开始，倒序地处理矩阵元素。

应该把这句话 "为了防止第一列的第一个元素被提前更新，我们需要从最后一行开始，倒序地处理矩阵元素。" 改成"为了防止每一列的第一个(行)元素被提前更新，我们需要从最后一行开始，倒序地处理矩阵元素。例子：
[0,1,2,0],   [0,0,0,0],
[3,4,5,2],   [3,4,5,2],
[1,3,1,5]   [1,3,1,5]
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/set-matrix-zeroes/solution/ju-zhen-zhi-ling-by-leetcode-solution-9ll7/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        flag_col0 = False

        for i in range(m):
            if matrix[i][0] == 0:
                # 第一列判断是否有0
                flag_col0 = True
            # 每行从第二列开始遍历
            for j in range(1, n):
                if matrix[i][j] == 0:
                    # 置空第一行第一列的值作为标识
                    matrix[i][0] = matrix[0][j] = 0

        # 从最后一行进行遍历。避免第一行遍历的时候将第一行的元素都置为0（因为第一列为0）。让第二行下面的遍历收到影响
        # 从最后一行进行遍历，不会影响第一行的数据。
        # 注意第一行的遍历是跟自己和第一列是否为0判断
        for i in range(m - 1, -1, -1):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
            if flag_col0:
                matrix[i][0] = 0

# 为什么行列都这样处理呢？因为行列都这样处理，到最后无法区分究竟第一行第一列是不是有0。而
