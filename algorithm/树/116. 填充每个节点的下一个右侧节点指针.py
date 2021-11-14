"""
给定一个 完美二叉树 ，其所有叶子节点都在同一层，每个父节点都有两个子节点。二叉树定义如下：

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL。

初始状态下，所有 next 指针都被设置为 NULL。



**进阶**：

你只能使用常量级额外空间。o(1)!!
使用递归解题也符合要求，本题中递归程序占用的栈空间不算做额外的空间复杂度。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


print('层次遍历，列表')


class Solution:
    def connect(self, root: 'Node') -> 'Node':
        """层序遍历"""
        if not root:
            return root
        deq = [root]
        pre = None
        while deq:
            tmp = []
            for i in deq:
                if pre:
                    pre.next = i
                if i.left:
                    tmp.append(i.left)
                if i.right:
                    tmp.append(i.right)
                pre = i
            deq = tmp
            pre = None
        return root


"""
题解：

复杂度分析

时间复杂度：O(N)O(N)。每个节点会被访问一次且只会被访问一次，即从队列中弹出，并建立 \text{next}next 指针。
空间复杂度：O(N)O(N)。这是一棵完美二叉树，它的最后一个层级包含 N/2N/2 个节点。广度优先遍历的复杂度取决于一个层级上的最大元素数量。这种情况下空间复杂度为 O(N)O(N)。

O(1)就称为常量级如果是O(n)就称为线性级 不符合题意！

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/solution/tian-chong-mei-ge-jie-dian-de-xia-yi-ge-you-ce-2-4/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""
import collections

print('collections.deque')


class Solution:
    def connect(self, root: 'Node') -> 'Node':

        if not root:
            return root

        # 初始化队列同时将第一层节点加入队列中，即根节点
        Q = collections.deque([root])

        # 外层的 while 循环迭代的是层数
        while Q:

            # 记录当前队列大小
            size = len(Q)

            # 遍历这一层的所有节点
            for i in range(size):

                # 从队首取出元素
                node = Q.popleft()

                # 连接
                if i < size - 1:
                    node.next = Q[0]

                # 拓展下一层节点
                if node.left:
                    Q.append(node.left)
                if node.right:
                    Q.append(node.right)

        # 返回根节点
        return root


"""
https://labuladong.github.io/algo/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E7%B3%BB%E5%88%97/%E4%BA%8C%E5%8F%89%E6%A0%91%E7%B3%BB%E5%88%971.html

二叉树的问题难点在于，如何把题目的要求细化成每个节点需要做的事情，但是如果只依赖一个节点的话，肯定是没办法连接「跨父节点」的两个相邻节点的。

递归！
"""
print("labuladong递归")


class Solution:
    def connect(self, root: 'Node') -> 'Node':
        """层序遍历"""
        if not root:
            return root
        self.connectTwoNode(root.left, root.right)

    def connectTwoNode(self, left: 'Node', right: 'Node'):
        if not (left and right):
            return
        # 前序遍历位置
        # 将传入的两个节点连接
        left.next = right
        # 递归
        self.connectTwoNode(left.left, left.right)
        self.connectTwoNode(right.left, right.right)
        self.connectTwoNode(left.right, right.left)


"""
妙呀！

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/solution/tian-chong-mei-ge-jie-dian-de-xia-yi-ge-you-ce-2-4/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
print("秒呀！o(1) 空间的解法！")


class Solution:
    def connect(self, root: 'Node') -> 'Node':

        if not root:
            return root

        # 从根节点开始
        leftmost = root

        while leftmost.left:

            # 遍历这一层节点组织成的链表，为下一层的节点更新 next 指针
            head = leftmost
            while head:

                # CONNECTION 1
                head.left.next = head.right

                # CONNECTION 2
                if head.next:
                    head.right.next = head.next.left

                # 指针向后移动
                head = head.next

            # 去下一层的最左的节点
            leftmost = leftmost.left

        return root


"""
另一种递归思想！秒呀！
作者：wang_ni_ma
链接：https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/solution/dong-hua-yan-shi-san-chong-shi-xian-116-tian-chong/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
print('另一种递归思想！秒呀！以root为起点，将整个纵深这段串联起来 ')


class Solution(object):
    def connect(self, root):
        """
        :type root: Node
        :rtype: Node
        """

        def dfs(root):
            if not root:
                return
            left = root.left
            right = root.right
            # 配合动画演示理解这段，以root为起点，将整个纵深这段串联起来
            while left:
                left.next = right
                left = left.right
                right = right.left
            # 递归的调用左右节点，完成同样的纵深串联
            dfs(root.left)
            dfs(root.right)

        dfs(root)
        return root
