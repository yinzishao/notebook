"""
给定一个单链表，把所有的奇数节点和偶数节点分别排在一起。请注意，这里的奇数节点和偶数节点指的是节点编号的奇偶性，而不是节点的值的奇偶性。

请尝试使用原地算法完成。你的算法的空间复杂度应为 O(1)，时间复杂度应为 O(nodes)，nodes 为节点总数。

示例 1:

输入: 1->2->3->4->5->NULL
输出: 1->3->5->2->4->NULL
示例 2:

输入: 2->1->3->5->6->4->7->NULL
输出: 2->3->6->7->1->5->4->NULL
说明:

应当保持奇数节点和偶数节点的相对顺序。
链表的第一个节点视为奇数节点，第二个节点视为偶数节点，以此类推

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/odd-even-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

# Definition for singly-linked list.
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class SolutionF:
    def oddEvenList(self, head: ListNode) -> ListNode:
        # 这个代码只是后面的两个数依次移动，与题目不符
        tmp = head
        while tmp.next and tmp.next.next:
            next = tmp.next
            nn = next.next
            tmp.next = next.next
            next.next = nn.next
            nn.next = next
            tmp = tmp.next.next
        return head


"""
当偶数的后面还存在：
则将下一个基数暂存，

插入偶数节点：
然后下一个基数的偶数放到当前偶数后面

插入基数节点：
将下个基数的下一个节点设为当前基数的下一个
当前基数的下个节点设为下一个基数，完成插入

迭代奇偶节点

"""


class Solution:
    def oddEvenList(self, head: ListNode) -> ListNode:
        if not head:
            return head
        ji_ln = head
        ou_ln = head.next
        # 将下一个基数移到前一个基数的后面，最后的偶数的next为该移动基数的next
        while ou_ln is not None and ou_ln.next:

            nextji_ln = ou_ln.next

            # 偶数节点关联
            ou_ln.next = nextji_ln.next
            # 基数节点插入到基数节点和偶数节点之间
            nextji_ln.next = ji_ln.next
            ji_ln.next = nextji_ln

            ji_ln = ji_ln.next
            ou_ln = ou_ln.next

        return head


"""
官方题解： 都看懂了吧，先一个左正蹬，把奇数节点串一块儿，再一个右鞭腿，把偶数节点串一起，然后啪，很快啊，把两个连成一条链表，可以说是训练有素，有bear来了。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/odd-even-linked-list/solution/qi-ou-lian-biao-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""


class Solution:
    def oddEvenList(self, head: ListNode) -> ListNode:
        """比自己想得移动简单. 偶节点的头不移动，最后再补回来"""
        if not head:
            return head

        evenHead = head.next
        odd, even = head, evenHead
        # 都看懂了吧，先一个左正蹬，把奇数节点串一块儿，再一个右鞭腿，把偶数节点串一起，然后啪，很快啊，把两个连成一条链表，可以说是训练有素，有bear来了。
        while even and even.next:
            # 奇数节点关联下一个奇数节点（偶数节点的下一个）
            odd.next = even.next
            # 把当前奇数节点下移
            odd = odd.next
            # 偶数节点变成基数节点的下一位，也就是下一个偶数节点
            even.next = odd.next
            even = even.next
        # 基数节点的下一个节点断开，最后补充成首个偶数节点
        odd.next = evenHead
        return head


head = init_ln([1, 2, 3, 4, 5, 6, 7, 8, 9])

print_ln(Solution().oddEvenList(head))
