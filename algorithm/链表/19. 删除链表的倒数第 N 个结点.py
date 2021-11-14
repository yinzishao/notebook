"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

进阶：你能尝试使用一趟扫描实现吗？

https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        tmp = head
        h = head
        while n > 0:
            tmp = tmp.next
            n -= 1
        # tmp会达到最后。导致tmp为None，出错
        while tmp.next != None:
            tmp = tmp.next
            head = head.next
        head.next = head.next.next
        return h


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # tmp会达到最后。导致tmp为None，出错
        # 故提前申请一个ListNode。例子: [1] 1
        h = ListNode(next=head)
        tmp, s = h, h
        # 往前走N步
        while n > 0:
            tmp = tmp.next
            n -= 1
        # 如果tmp还没到达最后一个元素。两个游标一起移动
        while tmp.next != None:
            tmp = tmp.next
            h = h.next
        # h.next则是要删除的节点
        h.next = h.next.next
        return s.next


"""
双指针
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/solution/shan-chu-lian-biao-de-dao-shu-di-nge-jie-dian-b-61/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # 因为会删除第一个节点，所以通过一个dummy进行兼容
        dummy = ListNode(0, head)
        first = head
        second = dummy
        for i in range(n):
            first = first.next

        while first:
            first = first.next
            second = second.next

        second.next = second.next.next
        return dummy.next
