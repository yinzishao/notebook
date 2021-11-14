from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln

"""
K 包含当前节点?
不包含： k=1, [1,2,3] => [2,1,3]
包含： k=1, [1,2,3] => [1,2,3]

题解类似看这个： https://leetcode-cn.com/problems/reverse-linked-list-ii/solution/fan-zhuan-lian-biao-ii-by-leetcode-solut-teyq/

"""

print("非递归的思路")

"""
最终的非递归更简洁的办法会好些？
"""


def reverseN(head, k):
    """
    pre上一个节点，head当前节点、next下一个节点
    当当前节点仍然有下一个节点的时候。将当前节点的方向反转, 移动到下一个节点继续操作。

    其他题解的思路是：想遍历获取到第k个节点。然后反转的结束条件是直到遇到k节点。虽然方便和理解，但还是觉得遍历了两遍不好。
    """
    # 如果k是包含则k+1，否则要特殊判断k==0的情况立刻返回
    if k < 1:
        return head
    cur = head
    # 当前节点的前一个节点
    # 保留反转后的下一个节点
    pre = nxt = None
    # k是包含的话。因为k+1了，所以k=0也是可以满足的(将头节点断开，后又连到下一个),虽然其实不需要操作！k<0的也就需要特殊判断了
    while cur and k > 0:
        # 当前节点反转到前一个节点
        nxt = cur.next
        cur.next = pre
        # 顺序下去
        pre = cur
        cur = nxt
        k -= 1
    # 记录之前的头，作为非反转的头
    head.next = nxt
    return pre


head1 = init_ln([1, 2, 3, 4, 5])
# print_ln(reverseN(head1, 2))
print_ln(reverseN(head1, 6))

print("非递归先获取第k个节点")


def reverseN(head, N):
    nhead = head
    # +1 让即使是0也能正常返回
    for _ in range(N + 1):
        nhead = nhead.next

    # 至少执行一遍
    pre = None
    cur = head
    while cur != nhead:
        next = cur.next
        cur.next = pre
        pre = cur
        cur = next
    head.next = nhead
    return pre


head1 = init_ln([1, 2, 3, 4, 5])
print_ln(reverseN(head1, 2))

print("非递归更简洁的办法!!")
"""
作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/reverse-linked-list-ii/solution/fan-zhuan-lian-biao-ii-by-leetcode-solut-teyq/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


def reverseN(head, N):
    """其实跟上面一样，只是通过range让代码看起来简洁些，但是无法判断k超出长度的异常"""
    if N == 1:
        # 包含关系的话，只能判断了吗？
        return head
    pre = None
    cur = head
    for _ in range(N):
        # 有需要的话
        if not cur:
            break
            # raise Exception("长度超出限制")
        # 判断异常
        next = cur.next
        cur.next = pre
        pre = cur
        cur = next
    head.next = cur
    return pre


head1 = init_ln([1, 2, 3, 4, 5])
print_ln(reverseN(head1, 6))  # 3, 2, 1, 4, 5

"""
递归思路

"""
print("labuladong的递归")


class Solution():
    successor = None

    def reverseN(self, head, N):
        if N == 1:
            self.successor = head.next
            return head
        nhead = self.reverseN(head.next, N - 1)
        # 递归中能成立的规则：
        # 当前节点的下一个节点已经变成递归子问题的末尾了
        # 让末尾连上当前节点，实现反转
        head.next.next = head
        # 末尾连上n节点后的后驱
        head.next = self.successor
        return nhead


head1 = init_ln([1, 2, 3, 4, 5])
print_ln(Solution().reverseN(head1, 3))

print("一个更简洁的递归")


def reverseN(head, N):
    if N == 1:
        return head  # Base case
    last = reverseN(head.next, N - 1)  # 这一步获取了最后要返回的第N个节点，原文中的successor在此步后已变成head.next.next，不需要单独使用N==1时去获得
    # 这一步是关键head.next无论什么场景都已经变成是要反转的最后节点了！其下一个节点就是后驱
    successor = head.next.next
    head.next.next = head
    head.next = successor
    return last


head1 = init_ln([1, 2, 3, 4, 5])
print_ln(reverseN(head1, 3))


def reverseBetween(head, M, N):
    if M == 1:
        return reverseN(head, N)
    head.next = reverseBetween(head.next, M - 1, N - 1)
    return head


print("reverseBetween")
head1 = init_ln([1, 2, 3, 4, 5])
print_ln(reverseBetween(head1, 3, 4))
