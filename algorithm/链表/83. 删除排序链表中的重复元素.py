"""
存在一个按升序排列的链表，给你这个链表的头节点 head ，请你删除所有重复的元素，使每个元素 只出现一次 。

返回同样按升序排列的结果链表。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list/
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        cur = head
        while cur and cur.next:
            next = cur.next
            while next and next.val == cur.val:
                next = next.next
            cur.next = next
            cur = next
        return head


# head = init_ln([1, 2, 3, 4, 4, 9])
# head = init_ln([1, 2, 3, 3, 4, 4, 5])
head = init_ln([1, 2, 3, 3, 4, 4])

print_ln(Solution().deleteDuplicates(head))

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list/solution/shan-chu-pai-xu-lian-biao-zhong-de-zhong-49v5/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        if not head:
            return head

        cur = head
        while cur.next:
            # 下一个如果跟当前一样，去掉链条关系！cur无须移动
            if cur.val == cur.next.val:
                cur.next = cur.next.next
            else:
                cur = cur.next

        return head
