"""
给定一个单链表 L 的头节点 head ，单链表 L 表示为：

L0→ L1→ … → Ln-1→ Ln
请将其重新排列后变为：

L0→Ln→L1→Ln-1→L2→Ln-2→ …

不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。


示例 1:

输入: head = [1,2,3,4]
输出: [1,4,2,3]
示例 2:

输入: head = [1,2,3,4,5]
输出: [1,5,2,4,3]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reorder-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

import io
import sys

from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# str = input()
# print(str)
print('hello world!')


class Node:

    def __init__(self, val=None):
        self.val = val
        self.next = None

    def __str__(self):
        return self.val

    def __repr__(self):
        return f"{str(self.val)}"


"""
思路是反转再反转，递归下去。
错误思路： 超出时间限制
"""


def soluction(array):
    dump = Node()
    dump.next = array

    start = dump.next
    while start:
        start.next = reverse(start.next)
        start = start.next
    return dump.next


def reverse(link):
    pre = None
    cur = link
    while cur:
        next = cur.next
        cur.next = pre
        pre = cur
        cur = next
    return pre


def init_link(arr):
    """根据数组转换成链表"""

    dump = Node()
    cur = dump
    for i in arr:
        cur.next = Node(i)
        cur = cur.next
    return dump.next


def transfer_link(link):
    """根据链表转换成数组"""
    result = []
    while link:
        result.append(link.val)
        link = link.next
    return result


def c1():
    inp_ln = init_link([1, 2, 3, 4])

    b = transfer_link(inp_ln)
    print(b)
    result = transfer_link(soluction(inp_ln))
    assert result == [1, 4, 2, 3], result


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: ListNode) -> None:
        """
        应该是找出中间，然后反转后面，最后进行合并链表
        """
        cur = head
        cur_two = head

        while cur_two.next and cur_two.next.next:
            cur = cur.next
            cur_two = cur_two.next.next
        cur.next = self.revers(cur.next)

        # 链表合并
        nex = cur.next
        start = head
        cur.next = None
        while nex:
            pre_next = start.next
            nex_next = nex.next
            start.next = nex
            # 这里死循环了，pre_next.next是等于nex
            nex.next = pre_next
            nex = nex_next
            start = pre_next
        return head

    def revers(self, head):
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre


head1 = init_ln([1, 2, 3, 4, 5])

res = Solution().reorderList(head1)
print_ln(res)

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reorder-list/solution/zhong-pai-lian-biao-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head:
            return

        mid = self.middleNode(head)
        l1 = head
        l2 = mid.next
        mid.next = None
        l2 = self.reverseList(l2)
        self.mergeList(l1, l2)

    def middleNode(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            nextTemp = curr.next
            curr.next = prev
            prev = curr
            curr = nextTemp
        return prev

    def mergeList(self, l1: ListNode, l2: ListNode):
        while l1 and l2:
            l1_tmp = l1.next
            l2_tmp = l2.next

            l1.next = l2
            l1 = l1_tmp

            l2.next = l1
            l2 = l2_tmp
