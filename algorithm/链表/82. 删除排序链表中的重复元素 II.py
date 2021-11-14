"""
存在一个按升序排列的链表，给你这个链表的头节点 head ，请你删除链表中所有存在数字重复情况的节点，只保留原始链表中 没有重复出现 的数字。

返回同样按升序排列的结果链表。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        if not head:
            return head
        pre = ListNode()
        tmp = pre
        cur = head
        while cur:
            dup = False
            while cur.next and cur.next.val == cur.val:
                cur = cur.next
                dup = True
            if dup:
                pre.next = cur.next
            else:
                # 因为pre为空节点，没有对下一个节点进行关联
                # 省下这一步的话，会导致tmp找不到下一个节点
                pre.next = cur
                pre = cur
            cur = cur.next
        return tmp.next


# head = init_ln([1, 2, 3, 4, 4, 9])
head = init_ln([1, 2, 3, 3, 4, 4, 5])

print_ln(Solution().deleteDuplicates(head))

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list-ii/solution/shan-chu-pai-xu-lian-biao-zhong-de-zhong-oayn/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        if not head:
            return head

        dummy = ListNode(0, head)

        cur = dummy
        # 从最前面空节点开始
        while cur.next and cur.next.next:
            # 如果下一个节点、下下一个节点值一样
            if cur.next.val == cur.next.next.val:
                x = cur.next.val
                # 遍历找到下一个节点不是重复节点的节点！
                # 新增x变量作为遍历结束条件
                # cur的好处，直接让链条关系正常。cur并没有移到，再次以cur出发开始重复寻找
                while cur.next and cur.next.val == x:
                    cur.next = cur.next.next
            else:
                cur = cur.next

        return dummy.next


print("我非要用递归写")


class Solution:
    def deleteDuplicates(self, head, val=None) -> ListNode:
        if not head: return head
        # 情况一（第一行）：我和之前重复了
        # 情况二（第二行）：我和之后重复了(当一开始的时候)
        # 则跳过当前节点，直接进下一个的递归。否则就当前节点是一个没有重复的数据，下一个为递归值
        # 妙在这个递归的判断！前后都判断，以此能进行正常删除！
        if (val is not None and head.val == val) or \
            (head.next and head.val == head.next.val):
            return self.deleteDuplicates(head.next, head.val)
        head.next = self.deleteDuplicates(head.next, head.val)
        return head


head = init_ln([1, 1, 3, 3, 4, 4, 5])

print_ln(Solution().deleteDuplicates(head))
