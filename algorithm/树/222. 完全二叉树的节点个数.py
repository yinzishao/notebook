"""
给你一棵 完全二叉树 的根节点 root ，求出该树的节点个数。

完全二叉树 的定义如下：在完全二叉树中，除了最底层节点可能没填满外，其余每层节点数都达到最大值，并且最下面一层的节点都集中在该层最左边的若干位置。若最底层为第 h 层，则该层包含 1~2h个节点。

进阶：遍历树来统计节点是一种时间复杂度为 O(n) 的简单解决方案。你可以设计一个更快的算法吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/count-complete-tree-nodes
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        """o(n) 广度优先遍历到最后一层，获取其节点数"""
        if not root:
            return 0
        deq = [root]
        cnt = 0
        while deq:
            cnt += 1
            n = deq.pop(0)
            if n.right:
                deq.append(n.right)
            if n.left:
                deq.append(n.left)
        return cnt


def check(r, exc):
    a = init_tree(r)
    res = Solution().countNodes(a)
    print(res)
    assert res == exc


print("层次遍历")
check([1, 2, 3, 4, 5, 6], 6)

"""递归遍历"""


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        return self.countNodes(root.left) + self.countNodes(root.right) + 1


print("递归遍历")
check([1, 2, 3, 4, 5, 6], 6)

"""优化：
二分搜索。 难点是如何在树上进行二分搜索?
如果第一次往左走，后面都往右走，就是第一次二分。判断节点是否存在。存在则当前节点往右走，否则往左走。下一个节点递归判断。
很难写出来！ 题解用位图来模拟
"""


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        l = 0
        # 第一次往左走
        if root.left:
            l = 2 * l + 1


"""
题解:
因此对于最大层数为 h 的完全二叉树，节点个数一定在 [2^h,2^{h+1}-1]的范围内，可以在该范围内通过二分查找的方式得到完全二叉树的节点个数。

如果第 k 个节点位于第 h 层，则 k 的二进制表示包含 h+1 位，其中最高位是 1，其余各位从高到低表示从根节点到第 k 个节点的路径，0 表示移动到左子节点，1 表示移动到右子节点。通过位运算得到第 k 个节点对应的路径，判断该路径对应的节点是否存在，即可判断第 k 个节点是否存在。

先往左遍历得到层数，例如 4层的树则最后的节点可以以此表示： 1000。后面二分进行路径区分就好

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/count-complete-tree-nodes/solution/wan-quan-er-cha-shu-de-jie-dian-ge-shu-by-leetco-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

print("二分搜索")
"""
class Solution {
    public int countNodes(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int level = 0;
        TreeNode node = root;
        while (node.left != null) {
            level++;
            node = node.left;
        }
        int low = 1 << level, high = (1 << (level + 1)) - 1;
        # 二分搜索！
        while (low < high) {
            int mid = (high - low + 1) / 2 + low;
            if (exists(root, level, mid)) {
                low = mid;
            } else {
                high = mid - 1;
            }
        }
        return low;
    }

    public boolean exists(TreeNode root, int level, int k) {
        int bits = 1 << (level - 1);
        TreeNode node = root;
        # 位运算进行路径移动
        while (node != null && bits > 0) {
            if ((bits & k) == 0) {
                node = node.left;
            } else {
                node = node.right;
            }
            bits >>= 1;
        }
        return node != null;
    }
}

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/count-complete-tree-nodes/solution/wan-quan-er-cha-shu-de-jie-dian-ge-shu-by-leetco-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
check([1, 2, 3, 4, 5, 6], 6)

"""
还可以根据左右子数的深度判断，进行递归遍历

我们看到左子树高度为3，右子树高度为2。说明此时最后一层不满，但倒数第二层已经满了，可以直接得到右子树的节点个数。同理，右子树节点+root节点，总数为2^right，即2^2。再对左子树进行递归查找。
"""
