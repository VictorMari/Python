def find_pairs(nums, Sum):
    if len(nums) <= 1 and nums[0] != Sum:
        return None

    table = dict()
    for num in nums:
        table[hash(num)] = num
    for num in nums:
        target = Sum - num
        if target in table:
            return (num, target) 
    return None


if __name__ == "__main__":
    tuple = find_pairs(range(1, 20), 10)
    print(tuple)

    tuple2 = find_pairs([2,2], 4)
    print(tuple2)

    tuple3 = find_pairs([2], 4)
    print(tuple3)

    tuple4 = find_pairs([], 3)
    print(tuple4)