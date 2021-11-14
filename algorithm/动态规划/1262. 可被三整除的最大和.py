"""
给你一个整数数组nums，请你找出并返回能被三整除的元素最大和。



示例 1：

输入：nums = [3,6,5,1,8]
输出：18
解释：选出数字 3, 6, 1 和 8，它们的和是 18（可被 3 整除的最大和）。
示例 2：

输入：nums = [4]
输出：0
解释：4 不能被 3 整除，所以无法选出数字，返回 0。
示例 3：

输入：nums = [1,2,3,4,4]
输出：12
解释：选出数字 1, 3, 4 以及 4，它们的和是 12（可被 3 整除的最大和）。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/greatest-sum-divisible-by-three
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


"""
remainder分别为余数0，1，2时的最大值


class Solution {
public:
    int maxSumDivThree(vector<int>& nums) {
         int N = nums.size();
        int remainder[3] = {0};
        for(int i = 0; i < N; i++){
            int a,b,c;
            a = remainder[0] + nums[i];
            b = remainder[1] + nums[i];
            c = remainder[2] + nums[i];
            remainder[a%3] = max(remainder[a%3], a);
            remainder[b%3] = max(remainder[b%3], b);
            remainder[c%3] = max(remainder[c%3], c);
        }
        return remainder[0];
    }
};

作者：ming-jun
链接：https://leetcode-cn.com/problems/greatest-sum-divisible-by-three/solution/20xing-dai-ma-qing-song-shuang-bai-yi-ka-hc1k/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
