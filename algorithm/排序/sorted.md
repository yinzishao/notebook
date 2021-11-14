
- [leetcode排序数组](https://leetcode-cn.com/problems/sort-an-array/)


![](./lADPBGKocQu6oKTNC9DND8A_4032_3024.jpg)

# python思想

完善的基本工作过程是：
1. 扫描数组，确定其中的单调上升段和严格单调下降段，将严格下降段反转。我们将这样的段称之为run。
2. 定义最小run长度，短于此的run通过插入排序合并为长度高于最小run长度；
3. 反复归并一些相邻run，过程中需要避免归并长度相差很大的run，直至整个排序完成；
4. 如何避免归并长度相差很大run呢， 依次将run压入栈中，若栈顶run X，run Y，run Z 的长度违反了X>Y+Z 或 Y>Z 则Y run与较小长度的run合并，并再次放入栈中。 依据这个法则，能够尽量使得大小相同的run合并，以提高性能。注意Timsort是稳定排序故只有相邻的run才能归并。
5. Merge操作还可以辅之以galloping（下面提供代码没有使用此优化），具体细节可以自行研究。

总之，timsort是工业级算法，其混用插入排序与归并排序，二分搜索等算法，亮点是充分利用待排序数据可能部分有序的事实，并且依据待排序数据内容动态改变排序策略——选择性进行归并以及galloping。

- [什么是Timsort排序方法？ - Ron Tang的回答 - 知乎](https://www.zhihu.com/question/23928138/answer/562890458)
- [Python sort 的实现 - Timsort 算法](https://juejin.im/entry/6844903480931385358)
- https://github.com/python/cpython/blob/master/Objects/listobject.c
- [除了冒泡排序，你知道Python内建的排序算法吗？](https://www.infoq.cn/article/Vmz6H4iwMR5tWWBp4OYZ)
- **这篇文章讲述得比较详细**: [timsort](https://sikasjc.github.io/2018/07/25/timsort/)
