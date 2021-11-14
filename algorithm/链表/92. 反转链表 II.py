"""
给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。请你反转从位置 left 到位置 right 的链表节点，返回 反转后的链表 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-linked-list-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        tmp = head
        pre = None
        interval = right - left
        # 如果是left=1说明是直接反转topk
        # 如何优化？left=1, pre就是空的
        if not left > 1:
            return self.reverseTopK(tmp, interval)
        # 找出要反转的左边头节点
        while left > 1:
            left -= 1
            pre = tmp
            tmp = tmp.next
        # 续回反转后的节点
        pre.next = self.reverseTopK(tmp, interval)
        return head

    def reverseTopK(self, head: ListNode, k):
        # 反转topk写了两次还是写得不顺手
        # 递归也可以
        tmp = head

        # 当前节点的前一个节点
        pre = None
        # 保留下一个节点
        nxt = head.next
        while head.next and k > 0:
            # 当前节点反转到前一个节点
            head.next = pre
            # 顺序下去
            pre = head
            head = nxt
            # 下个节点的下个节点
            nxt = nxt.next
            k -= 1
        # 当前节点已经下一个节点还未连上
        head.next = pre
        # 记录之前的头，作为非反转的头
        tmp.next = nxt
        return head

    def reverseTopK2(self, head: ListNode, k):
        """
        pre上一个节点，head当前节点、next下一个节点

        当当前节点仍然有下一个节点的时候。将当前节点的方向反转, 移动到下一个节点继续操作。

        """
        tmp = head

        # 当前节点的前一个节点
        # 保留反转后的下一个节点
        pre = nxt = None
        # 保留下一个节点
        while head and k + 1 > 0:
            # 当前节点反转到前一个节点
            nxt = head.next
            head.next = pre
            # 顺序下去
            pre = head
            head = nxt
            k -= 1
        # 记录之前的头，作为非反转的头
        tmp.next = nxt
        return pre


head1 = init_ln([1, 2, 3, 4, 5])
print_ln(Solution().reverseTopK2(head1, 2))
# print_ln(Solution().reverseBetween(head1, 2, 4))
# print_ln(Solution().reverseBetween(init_ln([5]), 1, 1))
# print_ln(Solution().reverseBetween(init_ln([3, 5]), 1, 2))


"""
整体思想是：在需要反转的区间里，每遍历到一个节点，让这个新节点来到反转部分的起始位置。

下面我们具体解释如何实现。使用三个指针变量 pre、curr、next 来记录反转的过程中需要的变量，它们的意义如下：

curr：指向待反转区域的第一个节点 left；
next：永远指向 curr 的下一个节点，循环过程中，curr 变化以后 next 会变化；
pre：永远指向待反转区域的第一个节点 left 的前一个节点，在循环过程中不变。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reverse-linked-list-ii/solution/fan-zhuan-lian-biao-ii-by-leetcode-solut-teyq/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        # 设置 dummyNode 是这一类问题的一般做法
        dummy_node = ListNode(-1)
        dummy_node.next = head
        pre = dummy_node
        for _ in range(left - 1):
            pre = pre.next

        cur = pre.next
        for _ in range(right - left):
            # 整体思想是：在需要反转的区间里，每遍历到一个节点，让这个新节点来到反转部分的起始位置。
            next = cur.next
            # 当前节点（一开始的头节点）连接下下一个节点
            cur.next = next.next
            # 将下一个节点移动到头节点。
            # 下一个节点往前插入
            next.next = pre.next
            # 注意头结点是pre.next，pre定位的，而不是当前cur
            pre.next = next
        return dummy_node.next
