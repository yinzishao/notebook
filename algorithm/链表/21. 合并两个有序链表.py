"""

将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。


"""
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1

        if l1.val > l2.val:
            head, ln = l2, l1
        else:
            head, ln = l1, l2
        result = head
        while ln and head:
            if head.val < ln.val:
                head = head.next
            else:
                # head的下一个节点置为另一个链条的节点，导致head本来的下一个节点失效
                head.next = ln
                ln = ln.next
                head = head.next
        head.next = ln
        return result


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        dump = ListNode()
        tmp = dump
        while l1 and l2:
            if l1.val < l2.val:
                dump.next = l1
                l1 = l1.next
            else:
                dump.next = l2
                l2 = l2.next
            dump = dump.next
        if l1:
            dump.next = l1
        else:
            dump.next = l2
        return tmp.next


head1 = init_ln([1, 3, 5, 7, 9])
head2 = init_ln([1, 2, 3, 4, 5, 6, 7, 8, 9])

print_ln(Solution().mergeTwoLists(head1, head2))

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/merge-two-sorted-lists/solution/he-bing-liang-ge-you-xu-lian-biao-by-leetcode-solu/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


# 迭代
class Solution:
    def mergeTwoLists(self, l1, l2):
        prehead = ListNode(-1)

        prev = prehead
        while l1 and l2:
            if l1.val <= l2.val:
                prev.next = l1
                l1 = l1.next
            else:
                prev.next = l2
                l2 = l2.next
            prev = prev.next

        # 合并后 l1 和 l2 最多只有一个还未被合并完，我们直接将链表末尾指向未合并完的链表即可
        prev.next = l1 if l1 is not None else l2

        return prehead.next


"""
递归的思路: 有点意思。很直观
"""


class Solution:
    def mergeTwoLists(self, l1, l2):
        if not l1:
            return l2
        if not l2:
            return l1
        if l1.val < l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            # 直接返回了
            return l1
        else:
            # 直接返回了
            l2.next = self.mergeTwoLists(l2.next, l1)
            return l2


head1 = init_ln([1, 3, 5, 7, 9])
head2 = init_ln([1, 2, 3, 4, 5, 6, 7, 8, 9])

print_ln(Solution().mergeTwoLists(head1, head2))
