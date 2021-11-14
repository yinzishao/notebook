"""
给你一个字符数组 chars ，请使用下述算法压缩：

从一个空字符串 s 开始。对于 chars 中的每组 连续重复字符 ：

如果这一组长度为 1 ，则将字符追加到 s 中。
否则，需要向 s 追加字符，后跟这一组的长度。
压缩后得到的字符串 s 不应该直接返回 ，需要转储到字符数组 chars 中。需要注意的是，如果组长度为 10 或 10 以上，则在 chars 数组中会被拆分为多个字符。

请在 修改完输入数组后 ，返回该数组的新长度。

你必须设计并实现一个只使用常量额外空间的算法来解决此问题。


示例 1：

输入：chars = ["a","a","b","b","c","c","c"]
输出：返回 6 ，输入数组的前 6 个字符应该是：["a","2","b","2","c","3"]
解释：
"aa" 被 "a2" 替代。"bb" 被 "b2" 替代。"ccc" 被 "c3" 替代。
示例 2：

输入：chars = ["a"]
输出：返回 1 ，输入数组的前 1 个字符应该是：["a"]
解释：
没有任何字符串被替代。
示例 3：

输入：chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
输出：返回 4 ，输入数组的前 4 个字符应该是：["a","b","1","2"]。
解释：
由于字符 "a" 不重复，所以不会被压缩。"bbbbbbbbbbbb" 被 “b12” 替代。
注意每个数字在数组中都有它自己的位置。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/string-compression
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List


class Solution:
    def compress(self, chars: List[str]) -> int:
        # 要求： 压缩后得到的字符串 s 不应该直接返回 ，需要转储到字符数组 chars 中。
        length = len(chars)
        start, end, cur = 0, length, 0
        while start < end:
            char = chars[start]
            # 当前值赋予对比窗口的左边
            chars[cur] = char

            # 窗口比较
            left = start + 1
            while left < end and char == chars[left]:
                left += 1

            # 是否有相同值比较
            interval = left - start
            if interval > 1:
                for i in str(interval):
                    cur += 1
                    chars[cur] = i
            cur += 1
            start = left
        return cur


assert 6 == Solution().compress(["a", "a", "b", "b", "c", "c", "c"])
assert 4 == Solution().compress(["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])


"""

# 题解是通过rigth来进行遍历。滑动窗口的右边肯定是需要顺序遍历一遍的！

class Solution {
    public int compress(char[] chars) {     // 数组大小范围： 1 <= chars.length <= 1000
        int left = 0;
        int size = 0;

        // 由于最后一个字符也需要判断，所以将右指针终点放到数组之外一格
        for (int right = 0; right <= chars.length; right++) {
            // 当遍历完成，或右指针元素不等于左指针元素时，更新数组
            if (right == chars.length || chars[right] != chars[left]) {
                chars[size++] = chars[left];    // 更新字符
                if (right - left > 1) {         // 更新计数，当个数大于 1 时才更新
                    for(char c : String.valueOf(right - left).toCharArray()) {
                        chars[size++] = c;
                    }
                }
                left = right;
            }
        }

        return size;
    }
}


作者：hui-fei-de-ma
链接：https://leetcode-cn.com/problems/string-compression/solution/hua-dong-chuang-kou-fa-ya-suo-zi-fu-chuan-java-by-/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
