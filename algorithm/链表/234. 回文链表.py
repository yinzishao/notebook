"""
请判断一个链表是否为回文链表。

示例 1:

输入: 1->2
输出: false
示例 2:

输入: 1->2->2->1
输出: true
进阶：
你能否用 O(n) 时间复杂度和 O(1) 空间复杂度解决此题？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/palindrome-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from notebook.algorithm.utils import check
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln


class Solution:
    def isPalindromeWrong(self, head: ListNode) -> bool:
        cur = head
        quick = cur
        while quick.next and quick.next.next:
            quick = quick.next.next
            cur = cur.next
        cur = cur.next
        """错误的时候：一半后的顺序跟开头的顺序对比，这不是回文！"""
        while cur:
            if cur.val != head.val:
                return False
            cur = cur.next
            head = head.next
        return True

    def isPalindrome(self, head: ListNode) -> bool:
        # 遍历到一半后进行反转？然后进行遍历判断？
        cur = head
        quick = head
        while quick.next and quick.next.next:
            quick = quick.next.next
            cur = cur.next
        first_half_end = cur
        second_half_start = self.reverse(first_half_end.next)
        tail = second_half_start
        # 反转后的一半，跟链表重新遍历比较
        nhead = head
        while tail:
            if tail.val != nhead.val:
                # 如果要复原结果，不能提前return
                return False
            tail = tail.next
            nhead = nhead.next
        # ！
        # 还原链表并返回结果
        first_half_end.next = self.reverse(second_half_start)
        return True

    def reverse(self, head: ListNode):
        pre = None
        while head:
            nxt = head.next
            head.next = pre
            pre = head
            head = nxt
        return pre
        # 还是错了！
        # return head


# head1 = init_ln([1, 2, 2, 1])
# check(Solution().isPalindrome, [head1], True)
head1 = init_ln([1, 2, 5, 2, 1])
check(Solution().isPalindrome, [head1], True)
head1 = init_ln([1, 2, 5, 6, 2, 1])
check(Solution().isPalindrome, [head1], False)

"""

O(1)的空间，不考虑链表复原，快慢指针在寻找中间节点的过程中直接反转链表前半部分，找到中间节点之后直接从中间向两边开始比较

class Solution {
    public boolean isPalindrome(ListNode head) {
        ListNode pre = null;
        ListNode slow = head;
        ListNode fast = head;
        while(fast != null && fast.next != null){
            ListNode temp = slow.next;
            if(pre != null) {
                slow.next = pre;
            }
            pre = slow;
            fast = fast.next.next;
            slow = temp;
        }
        // 双数情况
        if(fast != null) slow = slow.next;
        while(slow != null){
            if(slow.val != pre.val) return false;
            slow = slow.next;
            pre = pre.next;
        }
        return true;
    }
}

"""

"""
其实，借助二叉树后序遍历的思路，不需要显式反转原始链表也可以倒序遍历链表，下面来具体聊聊。

链表兼具递归结构，树结构不过是链表的衍生。那么，链表其实也可以有前序遍历和后序遍历
"""
