"""
给你二叉树的根节点root 和一个表示目标和的整数targetSum ，判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和targetSum 。

叶子节点 是指没有子节点的节点。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/path-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


"""
# Definition for a binary tree node.
import collections
from typing import Optional

from notebook.algorithm.树.utils import init_tree


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # 这个不是到叶子节点的！
        if not root:
            return False
        if root.val == targetSum:
            return True
        left = self.hasPathSum(root.left, targetSum - root.val)
        if left:
            return True
        right = self.hasPathSum(root.right, targetSum - root.val)
        if right:
            return True
        return False


a = init_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
res = Solution().hasPathSum(a, 22)
print(res)
assert res == True


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        # 下面的官方题解可以直接优化一下叶子节点提前结束
        if root.val == targetSum and not (root.left or root.right):
            return True
        # 直接or优雅
        left = self.hasPathSum(root.left, targetSum - root.val)
        if left:
            return True
        right = self.hasPathSum(root.right, targetSum - root.val)
        if right:
            return True
        return False


"""
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/path-sum/solution/lu-jing-zong-he-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        if not root.left and not root.right:
            return sum == root.val
        return self.hasPathSum(root.left, sum - root.val) or self.hasPathSum(root.right, sum - root.val)


"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/path-sum/solution/lu-jing-zong-he-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        que_node = collections.deque([root])
        que_val = collections.deque([root.val])
        while que_node:
            now = que_node.popleft()
            temp = que_val.popleft()
            if not now.left and not now.right:
                if temp == sum:
                    return True
                continue
            if now.left:
                que_node.append(now.left)
                que_val.append(now.left.val + temp)
            if now.right:
                que_node.append(now.right)
                que_val.append(now.right.val + temp)
        return False
