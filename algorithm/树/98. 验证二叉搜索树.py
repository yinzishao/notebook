"""
给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/validate-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        if not root:
            return False
        mi, ma = self.isValidTree(root)
        if mi is None:
            return False
        return True

    def isValidTree(self, root: TreeNode):
        """一直往下递归，
        返回树的最大与最小值
        当是叶子节点的时候返回自身

        当前节点跟返回的最大最小值比较。
        如果是左子树，则要比左子树最大值要大
        如果是右子树，则要比右子树最小值要小
        """
        if not root.left and not root.right:
            return root.val, root.val
        left_min = rigth_max = root.val
        if root.left:
            left_min, left_max = self.isValidTree(root.left)
            if left_max is None or left_max >= root.val:
                return None, None
        if root.right:
            rigth_min, rigth_max = self.isValidTree(root.right)
            # rigth_min会是子节点的数字
            if rigth_min is None or rigth_min <= root.val:
                return None, None
        return left_min, rigth_max


a = init_tree([5, 1, 4, None, None, 3, 6])
print(Solution().isValidBST(a))
a = init_tree([2, 1, 3])
print(Solution().isValidBST(a))
a = init_tree([1, 1])
res = Solution().isValidBST(a)
print(res)
assert res == False

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/validate-binary-search-tree/solution/yan-zheng-er-cha-sou-suo-shu-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def helper(node, lower=float('-inf'), upper=float('inf')) -> bool:
            if not node:
                return True

            val = node.val

            # 判断某个节点是不是在某个区间范围内的
            if val <= lower or val >= upper:
                return False

            # 当前值应该是右子树的最小值
            if not helper(node.right, val, upper):
                return False

            # 当前值应该是左子树的最大值
            if not helper(node.left, lower, val):
                return False
            # 左子树传最大值，当你的最大值传进去后，也递归成左子树的最大值了
            # 左子树的当前值应该是该树的右子树的最小值，但是该树得到一个最大值的范围，沿用下去。

            return True

        return helper(root)


"""
TODO: 中序遍历
"""


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        res = []

        def helper(r):
            if not r:
                return
            # 直接往上一层判断。判断root为空，减少一次判断。见下
            if not (r.left or r.right):
                res.append(r.val)
                return
            helper(r.left)
            res.append(r.val)
            helper(r.right)

        helper(root)
        print(res)
        tmp = res[0]
        for i in res[1:]:
            if i <= tmp:
                return False
            tmp = i
        return True


print('中序遍历')
# a = init_tree([5, 1, 4, None, None, 3, 6])
# a = init_tree([2, 1, 3])
a = init_tree([1, 1])
res = Solution().isValidBST(a)
print(res)

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/validate-binary-search-tree/solution/yan-zheng-er-cha-sou-suo-shu-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        stack, inorder = [], float('-inf')

        while stack or root:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            # 如果中序遍历得到的节点的值小于等于前一个 inorder，说明不是二叉搜索树
            if root.val <= inorder:
                return False
            inorder = root.val
            root = root.right

        return True


"""


作者：sweetiee
链接：https://leetcode-cn.com/problems/validate-binary-search-tree/solution/zhong-xu-bian-li-qing-song-na-xia-bi-xu-miao-dong-/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    # pre = None
    pre = float('-inf')

    def isValidBST(self, root: TreeNode) -> bool:
        if not root:
            return True

        # 访问左子树
        if not self.isValidBST(root.left):
            return False

        # 访问当前节点：如果当前节点小于等于中序遍历的前一个节点，说明不满足BST，返回 false；否则继续遍历。
        # 前一个值的判断要注意判断是否为None标识跳过第一个
        if root.val <= self.pre:
        # if self.pre is not None and root.val <= self.pre:
            return False
        self.pre = root.val
        return self.isValidBST(root.right)


print('题解中序遍历')
# a = init_tree([5, 1, 4, None, None, 3, 6])
# a = init_tree([2, 1, 3])
a = init_tree([1, 1])
a = init_tree([0, None, -1])
res = Solution().isValidBST(a)
print(res)

"""
返回中序遍历的数组

作者：LeetCode
链接：https://leetcode-cn.com/problems/delete-node-in-a-bst/solution/shan-chu-er-cha-sou-suo-shu-zhong-de-jie-dian-by-l/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []
