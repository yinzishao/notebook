"""
转一个单链表。

示例:

输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
进阶:
你可以迭代或递归地反转链表。你能否用两种方法解决这道题？



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

# Definition for singly-linked list.
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head:
            return head

        tmp = head.next
        # 第一个节点置空，防止死循环
        head.next = None

        while tmp is not None:
            # 保留下下节点
            nn = tmp.next
            # 反转节点
            tmp.next = head
            head = tmp
            tmp = nn
        return head


"""
题解： https://leetcode-cn.com/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-by-leetcode/

迭代： 当前节点的下一个节点，暂存。当前节点的下个节点变成前一个节点。
进入下一次迭代： 当前节点变成前一个节点，暂存的下一个节点变成当前节点。
"""


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        # 判断的是当前
        while curr is not None:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
        # 返回的是prev
        return prev


"""
递归

返回末尾，倒数第二个（当前）指向末尾，所以当前（倒数第二个）的下一个（末尾）的下一个指向当前，然后将当前置空，返回末尾。

"""


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or head.next is None:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
        # 返回的是prev


head = init_ln([1, 2, 3, 4, 5, 6, 7, 8, 9])

print_ln(Solution().reverseList(head))
