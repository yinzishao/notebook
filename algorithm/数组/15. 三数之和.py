"""
给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

四数之和思路一样：

 使用四个指针(a<b<c<d)。固定最小的a和b在左边，c=b+1,d=_size-1 移动两个指针包夹求解。
 保存使得nums[a]+nums[b]+nums[c]+nums[d]==target的解。偏大时d左移，偏小时c右移。c和d相遇时，表示以当前的a和b为最小值的解已经全部求得。b++,进入下一轮循环b循环，当b循环结束后。
 a++，进入下一轮a循环。 即(a在最外层循环，里面嵌套b循环，再嵌套双指针c,d包夹求解)。

https://leetcode-cn.com/problems/4sum/solution/si-shu-zhi-he-by-leetcode-solution/

"""


def sort(nums):
    length = len(nums)
    for i in range(length):
        while i - 1 >= 0 and nums[i - 1] > nums[i]:
            nums[i - 1], nums[i] = nums[i], nums[i - 1]
            i -= 1
    return nums


def three_sum(nums):
    nums = sort(nums)
    result = []
    for idx in range(len(nums)):
        # // 第一个数大于 0，后面的数都比它大，肯定不成立了
        if nums[idx] > 0:
            return result
        # // 去掉重复情况
        if idx - 1 >= 0 and nums[idx - 1] == nums[idx]:
            continue
        target = - nums[idx]
        s = idx + 1
        e = len(nums) - 1
        while s < e:
            if (nums[s] + nums[e]) > target:
                e -= 1
            elif (nums[s] + nums[e]) < target:
                s += 1
            else:
                # 现在要增加 left，减小 right，但是不能重复，
                # 比如: [-2, -1, -1, -1, 3, 3, 3], i = 0, left = 1, right = 6, [-2, -1, 3] 的答案加入后，需要排除重复的 -1 和 3
                result.append([nums[idx], nums[s], nums[e]])
                while s < e and nums[s + 1] == nums[s]:
                    s += 1
                s += 1
                while s < e and nums[e - 1] == nums[e]:
                    e -= 1
                e -= 1
    return result


input = [-1, 0, 1, 2, -1, -4]
# input = [-1, 2, -8, -10]
print(f"input {input} ,result {three_sum(input)}")

input = [0, 0, 0, 0]
print(f"input {input} ,result {three_sum(input)}")
input = [-2, 0, 0, 2, 2]
print(f"input {input} ,result {three_sum(input)}")
input = [0, 0, 0]
print(f"input {input} ,result {three_sum(input)}")
