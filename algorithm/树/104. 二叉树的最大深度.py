"""
给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

说明: 叶子节点是指没有子节点的节点。

示例：
给定二叉树 [3,9,20,null,null,15,7]，

    3
   / \
  9  20
    /  \
   15   7
返回它的最大深度 3 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-depth-of-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree

"""递归思路"""


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        cur_depth = 0
        if root.left:
            cur_depth = self.maxDepth(root.left) + 1
        if root.right:
            right_depth = self.maxDepth(root.right) + 1
            cur_depth = right_depth if right_depth > cur_depth else cur_depth
        return cur_depth


a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().maxDepth(a))

"""优雅很多"""


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1


a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().maxDepth(a))

"""递归很多能通过栈实现

为什么需要先右后左压入数据？是因为我们需要将先访问的数据，后压入栈（请思考栈的特点）。
"""

"""迭代思路

队列的形式广度遍历
"""


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        root_list = [root]
        depth = 0
        while root_list:
            tmp = []
            depth += 1
            # 出队列
            for i in root_list:
                if i.left:
                    tmp.append(i.left)
                if i.right:
                    tmp.append(i.right)
            root_list = tmp
        return depth


print("深度优先搜索算法（Depth First Search）")
a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().maxDepth(a))
