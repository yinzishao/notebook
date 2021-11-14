"""
给定二叉搜索树（BST）的根节点和一个值。 你需要在BST中找到节点值等于给定值的节点。 返回以该节点为根的子树。 如果节点不存在，则返回 NULL。

例如，

给定二叉搜索树:

        4
       / \
      2   7
     / \
    1   3

和值: 2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/search-in-a-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        if not root:
            return None
        if root.val == val:
            return root
        if root.val < val:
            return self.searchBST(root.right, val)
        return self.searchBST(root.left, val)


a = init_tree([4, 2, 7, 1, 3])
res = Solution().searchBST(a, 2)
print(res.val)

"""迭代"""


class Solution:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        while root is not None and root.val != val:
            root = root.left if root.val > val else root.right
        return root


print("迭代")
a = init_tree([4, 2, 7, 1, 3])
res = Solution().searchBST(a, 2)
print(res.val)
