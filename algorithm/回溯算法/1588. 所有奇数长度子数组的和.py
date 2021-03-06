"""
给你一个正整数数组arr，请你计算所有可能的奇数长度子数组的和。

子数组 定义为原数组中的一个连续子序列。

请你返回 arr中 所有奇数长度子数组的和 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sum-of-all-odd-length-subarrays
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

from typing import List

"""

与题解不符合，这里是不限顺序的，子序列/子集.题解是子数组（必须相邻）
"""


class SolutionFalse:
    def sumOddLengthSubarrays(self, arr: List[int]) -> int:
        pass

    def sub_array(self, arr):
        result = []
        length = len(arr)

        def s(idx, val):
            if idx == length + 1:
                return
            if len(val) % 2 == 1:
                # result.append(sum(val))
                result.append(val)
            for i in range(idx, length):
                new_val = val[::]
                new_val.append(arr[i])
                s(i + 1, new_val)

        s(0, [])
        # return sum(result)
        return result


class Solution:
    def sumOddLengthSubarrays(self, arr: List[int]) -> int:
        """
        这个题解是在o(n3)的复杂度，一因为sum也是一个循环遍历
        """
        length = len(arr)
        result = 0
        for idx in range(length):
            for interval in range(0, length, 2):
                end = idx + interval + 1
                if end <= length:
                    result += sum(arr[idx:end])
        return result


print(Solution().sumOddLengthSubarrays([1, 4, 2, 5, 3]))


"""

对于此类区间求和问题，我们应当想到使用「前缀和」进行优化：使用 O(n) 的复杂度预处理出前缀和数组，每次查询 [l, r] 区间和可以在 O(1) 返回。

class Solution {
    public int sumOddLengthSubarrays(int[] arr) {
        int n = arr.length;
        int[] sum = new int[n + 1];
        for (int i = 1; i <= n; i++) sum[i] = sum[i - 1] + arr[i - 1];
        int ans = 0;
        for (int len = 1; len <= n; len += 2) {
            for (int l = 0; l + len - 1 < n; l++) {
                int r = l + len - 1;
                ans += sum[r + 1] - sum[l];
            }
        }
        return ans;
    }
}

作者：AC_OIer
链接：https://leetcode-cn.com/problems/sum-of-all-odd-length-subarrays/solution/gong-shui-san-xie-yi-ti-shuang-jie-qian-18jq3/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

"""
O(n) 题解: https://leetcode-cn.com/problems/sum-of-all-odd-length-subarrays/solution/cong-on3-dao-on-de-jie-fa-by-liuyubobobo/599438

* odd奇数，even偶数
* 对于每个元素i(数组中下标为i)来说，要构成奇数长度的子数组
  即 i左边的元素个数left+i本身自己一个+右边元素的个数right=奇数
  即 left+right=偶数
* 满足a+b=偶数就只有两种情况
  1. 奇数+奇数=偶数
  2. 偶数+偶数=偶数
* 1. 所以只需要求得i左边可以选择奇数长度的可能有多少种，即left_odd,同样求右边奇数right_odd
     就可以求出策略1有多少种可能
  2. 所以只需要求得i左边可以选择偶数长度的可能有多少种，即left_odd,同样求右边偶数right_odd
     就可以求出策略1有多少种可能，注意0也算选择的一种可能
* 即元素i在所有奇数长度子数组出现的次数总和是
  left_odd*right_odd+left_even*right_even
* 元素i左边元素共有i个，右边元素共有siz-i-1个

class Solution {
public:
    int sumOddLengthSubarrays(vector<int>& arr) {

        int res = 0;
        for(int i = 0; i < arr.size(); i ++){
            int left = i + 1, right = arr.size() - i,
                left_even = (left + 1) / 2, right_even = (right + 1) / 2,
                left_odd = left / 2, right_odd = right / 2;
            res += (left_even * right_even + left_odd * right_odd) * arr[i];
        }
        return res;
    }
};

作者：liuyubobobo
链接：https://leetcode-cn.com/problems/sum-of-all-odd-length-subarrays/solution/cong-on3-dao-on-de-jie-fa-by-liuyubobobo/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
