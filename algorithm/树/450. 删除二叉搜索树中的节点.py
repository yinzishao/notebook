"""
给定一个二叉搜索树的根节点 root 和一个值 key，删除二叉搜索树中的 key 对应的节点，并保证二叉搜索树的性质不变。返回二叉搜索树（有可能被更新）的根节点的引用。

一般来说，删除节点可分为两个步骤：

首先找到需要删除的节点；
如果找到了，删除它。
说明： 要求算法时间复杂度为 O(h)，h 为树的高度。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/delete-node-in-a-bst
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        """yeshila， 思路不对"""
        if not root:
            return None
        pre, opt = None, None
        # 搜索
        dnode = root  # 要删除的节点
        while dnode is not None and dnode.val != key:
            pre = dnode
            if dnode.val > key:
                dnode = dnode.left
                opt = -1
            else:
                dnode = dnode.right
                opt = 1
        if not dnode:
            return root

        next_node = None  # 删除节点要替换的节点
        right_min = dnode.right
        # 若右子树不存在，左子树的根节点直接替换
        if not right_min:
            next_node = dnode.left
        else:
            next_node = right_min
            right_pre = dnode  # 最大右子节点的上一个节点
            # 若右子树存在，找出其右子树的~~最大值~~是最小值！
            while next_node.left:
                right_pre = next_node
                next_node = next_node.left
            if right_pre == dnode:
                right_pre.right = None
            else:
                # 置空最大右子节点的上一个节点
                right_pre.left = None
        # 将最大右子节点替换成要删除的节点
        # next_node会是空？
        if next_node:
            next_node.left = dnode.left
            next_node.right = dnode.right
        if not pre:
            return next_node
        if opt == 1:
            pre.right = next_node
        else:
            pre.left = next_node
        return root


class Solution:
    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        if not root:
            return None
        pre, opt = None, None
        # 搜索
        dnode = root  # 要删除的节点
        while dnode is not None and dnode.val != key:
            pre = dnode
            if dnode.val > key:
                dnode = dnode.left
                opt = -1
            else:
                dnode = dnode.right
                opt = 1
        if not dnode:
            return root
        # 如果左子树存在, 找出左子树的最大节点
        if dnode.left:
            next_node = dnode.left
            if not next_node.right:
                # 如果左子树的最大节点就是自身，也就是没有右子树
                # 最大节点上升到删除节点（右子树改为删除节点的右子树）
                next_node.right = dnode.right
            else:
                # 否则，递归从右子树找出做大的节点替换删除节点
                # （要置空最大节点的父节点、最大节点的左右子树改为删除节点的左右子树）
                left_pre = next_node
                while next_node.right:
                    left_pre = next_node
                    next_node = next_node.right
                left_pre.right = None
                next_node.right = dnode.right
                next_node.left = dnode.left
        else:
            # 否则替换节点为右子树的节点
            next_node = dnode.right  # 会是空
        # 删除节点的父节点的子节点改为该最大节点
        if pre:
            if opt == 1:
                pre.right = next_node
            else:
                pre.left = next_node
        else:
            root = next_node
        return root


a = init_tree([5, 3, 6, 2, 4, None, 7])
res = Solution().deleteNode(a, 3)
res = Solution().deleteNode(a, 0)
a = init_tree([0])
res = Solution().deleteNode(a, 0)
a = init_tree([5, 3, 6, 2, 4, None, 7])
res = Solution().deleteNode(a, 5)
print(res.val)
# fuck you
"""

[1,0,15,null,null,4,35,3,8,25,49,2,null,5,12,22,27,47,null,null,null,null,7,11,13,19,24,26,31,40,48,6,null,9,null,null,14,17,21,23,null,null,null,30,33,39,42,null,null,null,null,null,10,null,null,16,18,20,null,null,null,28,null,32,34,36,null,41,44,null,null,null,null,null,null,null,null,null,29,null,null,null,null,null,37,null,null,43,46,null,null,null,38,null,null,45]
22
输出：
[1,0,15,null,null,4,35,3,8,25,49,2,null,5,12,21,27,47,null,null,null,null,7,11,13,19,24,26,31,40,48,6,null,9,null,null,14,17,null,23,null,null,null,30,33,39,42,null,null,null,null,null,10,null,null,16,18,null,null,28,null,32,34,36,null,41,44,null,null,null,null,null,null,null,29,null,null,null,null,null,37,null,null,43,46,null,null,null,38,null,null,45]
预期结果：
[1,0,15,null,null,4,35,3,8,25,49,2,null,5,12,23,27,47,null,null,null,null,7,11,13,19,24,26,31,40,48,6,null,9,null,null,14,17,21,null,null,null,null,30,33,39,42,null,null,null,null,null,10,null,null,16,18,20,null,28,null,32,34,36,null,41,44,null,null,null,null,null,null,null,null,null,29,null,null,null,null,null,37,null,null,43,46,null,null,null,38,null,null,45]

也没错吧？
"""

"""
题解：递归！

作者：LeetCode
链接：https://leetcode-cn.com/problems/delete-node-in-a-bst/solution/shan-chu-er-cha-sou-suo-shu-zhong-de-jie-dian-by-l/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    """
    注意找前驱和后驱是直接把跟节点传进去。而且是判断至少有一个才进来

    重要的是其然后利用递归的思路，再次找到替换的节点进行删除！

    这样避免了我上面代码里面的各种pre_node的临时变量

    题解跟我写的代码思路不一样的场景是其没有右子树，拿的是左子树的最大节点，而我是直接把子树跟节点往上移
    """

    def successor(self, root):
        """
        One step right and then always left
        """
        root = root.right
        while root.left:
            root = root.left
        return root.val

    def predecessor(self, root):
        """
        One step left and then always right
        """
        root = root.left
        while root.right:
            root = root.right
        return root.val

    def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        if not root:
            return None

        # 递归的思路往下走
        # delete from the right subtree
        if key > root.val:
            root.right = self.deleteNode(root.right, key)
        # delete from the left subtree
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        # delete the current node
        else:
            # the node is a leaf
            if not (root.left or root.right):
                root = None
            # the node is not a leaf and has a right child
            elif root.right:
                # 判断至少有子树才进来。用右子树的最小值替换掉当前节点
                root.val = self.successor(root)
                # 然后利用递归的思路，再次找到替换的节点进行删除！
                root.right = self.deleteNode(root.right, root.val)
            # the node is not a leaf, has no right child, and has a left child
            else:
                root.val = self.predecessor(root)
                root.left = self.deleteNode(root.left, root.val)

        return root
