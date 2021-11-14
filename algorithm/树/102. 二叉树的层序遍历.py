"""
给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。



示例：
二叉树：[3,9,20,null,null,15,7],

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

层序遍历需要区分每一层，如果是队列的形式，需要每次进入队列前，进行操作。获取队列的长度。

深度遍历的应用场景：最短路径
"""
from typing import List

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        result = [[root.val]]
        deq = [root]
        while deq:
            tmp = []
            res_tmp = []
            for i in deq:
                if i.left:
                    tmp.append(i.left)
                    res_tmp.append(i.left.val)
                if i.right:
                    tmp.append(i.right)
                    res_tmp.append(i.right.val)
            deq = tmp
            # result置为加当前root的值
            if res_tmp:
                result.append(res_tmp)
        return result


"""
记树上所有节点的个数为 nn。

时间复杂度：每个点进队出队各一次，故渐进时间复杂度为 O(n)O(n)。
空间复杂度：队列中元素的个数不超过 nn 个，故渐进空间复杂度为 O(n)O(n)。

"""


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        result = []
        deq = [root]
        while deq:
            tmp = []
            res_tmp = []
            for i in deq:
                res_tmp.append(i.val)
                if i.left:
                    tmp.append(i.left)
                if i.right:
                    tmp.append(i.right)
            deq = tmp
            # result置为加当前root的值
            result.append(res_tmp)
        return result


a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().levelOrder(a))

"""
https://leetcode-cn.com/problems/binary-tree-level-order-traversal/solution/bfs-de-shi-yong-chang-jing-zong-jie-ceng-xu-bian-l/470197
"""
from collections import deque


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        res = []
        d = deque()
        d.append(root)
        while d:
            length = len(d)
            level = []
            for i in range(length):
                node = d.popleft()
                level.append(node.val)
                if node.left:
                    d.append(node.left)
                if node.right:
                    d.append(node.right)
            res.append(level)
        return res


"""
https://leetcode-cn.com/problems/binary-tree-level-order-traversal/solution/tao-mo-ban-bfs-he-dfs-du-ke-yi-jie-jue-by-fuxuemin/： 模板

DFS 做本题的主要问题是： DFS 不是按照层次遍历的。为了让递归的过程中同一层的节点放到同一个列表中，在递归时要记录每个节点的深度 level。递归到新节点要把该节点放入 level 对应列表的末尾。
当遍历到一个新的深度 level，而最终结果 res 中还没有创建 level 对应的列表时，应该在 res 中新建一个列表用来保存该 level 的所有节点。

作者：fuxuemingzhu
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal/solution/tao-mo-ban-bfs-he-dfs-du-ke-yi-jie-jue-by-fuxuemin/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""
print("递归！")


class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        res = []
        # 列表是作为指针进行传递的
        self.level(root, 0, res)
        return res

    def level(self, root, level, res):
        if not root: return
        if len(res) == level: res.append([])
        res[level].append(root.val)
        if root.left: self.level(root.left, level + 1, res)
        if root.right: self.level(root.right, level + 1, res)


a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().levelOrder(a))
