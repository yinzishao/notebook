"""
给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。

k 是一个正整数，它的值小于或等于链表的长度。

如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

进阶：

你可以设计一个只使用常数额外空间的算法来解决此问题吗？
你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-nodes-in-k-group
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

# Definition for singly-linked list.
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val


class Solution:
    """
    思考，如何拆到递归的写法呢？

    先遍历拿到k节点后的节点头
    如果k<i。直接返回，不需要反转。
    否则的化，反转head的topk(1-k -> k-1)，然后k+1节点后面的链表继续递归执行。其返回续在旧的head（1变成反转1-k的最后了）的后面
    """

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        """拆分成反转前k个链表节点"""
        rhead, i = head, k
        tmp = head
        while i > 0 and rhead:
            rhead = rhead.next
            i -= 1
        if i == 0:
            # 返回的是新的头节点
            head = self.reverseTopKGroup(head, k)
            # 旧的节点已经变成最后了，旧的节点的下一个节点，为递归下去的节点的topk反转
            tmp.next = self.reverseKGroup(rhead, k)
        return head

    """
    思路跟反转链表一样。只是会有个标识K。当前k个反转后，head，已经是第k个，
    输入的头节点已经是末尾了，需要将末尾的后面续上K+1的节点。而k+1的节点刚好是k节点(pre)的下一个，也就是cur。
    """

    """
    // 反转前 k 个元素。可以改为传入tail的节点，通过while比较到tail结束
    """

    def reverseTopKGroup(self, head: ListNode, k: int) -> ListNode:
        # 问题： k若是0有问题！
        pre = None
        before_head = head
        cur = head
        while k > 0 and cur:
            next = cur.next
            cur.next = pre
            pre = cur
            cur = next
            k -= 1
        before_head.next = cur
        return pre


"""

递归类似： https://leetcode-cn.com/problems/reverse-nodes-in-k-group/solution/di-gui-java-by-reedfan-2/
"""

head = init_ln([1, 2, 3, 4, 5, 6, 7, 8, 9])
head = init_ln([1, 2, 3, 4, 5])

# print_ln(Solution().reverseTopKGroup(head, 3))
print_ln(Solution().reverseKGroup(head, 3))

"""
题解
迭代：

但是对于一个子链表，除了翻转其本身之外，还需要将子链表的头部与上一个子链表连接，以及子链表的尾部与下一个子链表连接

没有节点，我们就创建一个节点。我们新建一个节点，把它接到链表的头部，让它作为 pre 的初始值，这样 head 前面就有了一个节点，我们就可以避开链表头部的边界条件。

头节点的前面，而无论之后链表有没有翻转，它的 next 指针都会指向正确的头节点。那么我们只要返回它的下一个节点就好了。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reverse-nodes-in-k-group/solution/k-ge-yi-zu-fan-zhuan-lian-biao-by-leetcode-solutio/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    """
    迭代循环，反转k个链表，保存前后节点，后续回。
    注意的是头节点的边界条件、新的头节点
    """

    # 翻转一个子链表，并且返回新的头与尾
    def reverse(self, head: ListNode, tail: ListNode):
        prev = None
        p = head
        while prev != tail:
            nex = p.next
            p.next = prev
            prev = p
            p = nex
        return tail, head

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        hair = ListNode(0)
        hair.next = head
        pre = hair

        while head:
            """pre、head、tail 、nex， 反正head、tail并返回最新的头和尾，然后通过pre的next、新的tail接上 """
            tail = pre
            # 查看剩余部分长度是否大于等于 k
            for i in range(k):
                tail = tail.next
                if not tail:
                    return hair.next
            # 保留旧的下一个节点
            nex = tail.next
            head, tail = self.reverse(head, tail)
            # 把子链表重新接回原链表
            pre.next = head
            tail.next = nex
            # 下一个末尾继续循环
            pre = tail
            head = tail.next

        return hair.next
