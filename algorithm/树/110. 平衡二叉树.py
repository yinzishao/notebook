from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree

"""递归思路， 优化： 至低向上，类似后序遍历"""


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        if not root:
            return True
        if abs(self.gexMaxDeath(root.left) - self.gexMaxDeath(root.right)) > 1 or self.isBalanced(
            root.left) or self.isBalanced(root.right):
            return False
        return True

    def gexMaxDeath(self, root):
        if not root:
            return 0
        return max(self.gexMaxDeath(root.left), self.gexMaxDeath(root.right)) + 1


def check(r, exc):
    a = init_tree(r)
    res = Solution().isBalanced(a)
    print(res)
    assert res == exc


# check([3, 9, 20, None, None, 15, 7], True)
# check([1, 2, 2, 3, 3, None, None, 4, 4], False)
check([1, 2, 2, 3, None, None, 3, 4, None, None, 4], False)

"""
思路一样
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/balanced-binary-tree/solution/ping-heng-er-cha-shu-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def height(root: TreeNode) -> int:
            if not root:
                return 0
            return max(height(root.left), height(root.right)) + 1

        if not root:
            return True
        return abs(height(root.left) - height(root.right)) <= 1 and self.isBalanced(root.left) and self.isBalanced(
            root.right)


"""

方法一由于是自顶向下递归，因此对于同一个节点，函数 height 会被重复调用，导致时间复杂度较高。如果使用自底向上的做法，则对于每个节点，函数 height 只会被调用一次。

自底向上递归的做法类似于后序遍历，对于当前遍历到的节点，先递归地判断其左右子树是否平衡，再判断以当前节点为根的子树是否平衡。如果一棵子树是平衡的，则返回其高度（高度一定是非负整数），否则返回 −1。如果存在一棵子树不平衡，则整个二叉树一定不平衡。


作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/balanced-binary-tree/solution/ping-heng-er-cha-shu-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def height(root: TreeNode) -> int:
            if not root:
                return 0
            leftHeight = height(root.left)
            rightHeight = height(root.right)
            if leftHeight == -1 or rightHeight == -1 or abs(leftHeight - rightHeight) > 1:
                return -1
            else:
                return max(leftHeight, rightHeight) + 1

        return height(root) >= 0
