"""
用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 appendTail 和 deleteHead ，分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，deleteHead操作返回 -1 )

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class CQueue:

    def __init__(self):
        self.stack_1 = []
        self.stack_2 = []

    def appendTail(self, value: int) -> None:
        while self.stack_2:
            self.stack_1.append(self.stack_2.pop())
        self.stack_1.append(value)

    def deleteHead(self) -> int:
        if not (self.stack_1 or self.stack_2):
            return -1
        while self.stack_1:
            self.stack_2.append(self.stack_1.pop())

        return self.stack_2.pop()


a = CQueue()
a.appendTail(1)
a.appendTail(2)
a.appendTail(3)
print(a.deleteHead())
print(a.deleteHead())
a.appendTail(4)
print(a.deleteHead())
print(a.deleteHead())
print(a.deleteHead())

"""

题解的 append 更精简了

作者：jyd
链接：https://leetcode-cn.com/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/solution/mian-shi-ti-09-yong-liang-ge-zhan-shi-xian-dui-l-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class CQueue:
    def __init__(self):
        self.A, self.B = [], []

    def appendTail(self, value: int) -> None:
        self.A.append(value)

    def deleteHead(self) -> int:
        if self.B: return self.B.pop()
        if not self.A: return -1
        while self.A:
            self.B.append(self.A.pop())
        return self.B.pop()
