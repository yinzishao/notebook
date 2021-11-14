#
# https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):

    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: TreeNode
        """
        if not preorder:
            return None

        return self.t(preorder, inorder)

    def t(self, preorder, inorder):
        if len(preorder) == 1:
            return TreeNode(preorder[0])
        else:
            first = preorder[0]
            result = TreeNode(first)
            n_pre = None
            n_in = None
            r_pre = None
            r_in = None
            for idx, val in enumerate(inorder):
                if val == first:
                    n_pre = preorder[1:1+idx]
                    n_in = inorder[0:idx]
                    r_pre = preorder[1+idx:]
                    r_in = inorder[idx+1:]
                    break
            result.left = self.t(n_pre, n_in) if n_pre else None
            result.right = self.t(r_pre, r_in) if r_pre else None
        return result


# a = [3,9,20,15,7]
# b = [9,3,15,20,7]
#
# c = Solution().buildTree(a, b)
# print(c)

a = [1,2]
b = [2,1]

c = Solution().buildTree(a, b)
print(c)

