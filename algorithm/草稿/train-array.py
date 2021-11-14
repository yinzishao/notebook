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
