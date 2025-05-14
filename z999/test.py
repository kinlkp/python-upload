def removeDuplicates(nums):
    """
    Given an integer array nums sorted in non-decreasing order, 
    remove the duplicates in-place such that each unique element 
    appears only once. The relative order of the elements should 
    be kept the same. Then return the number of unique elements in nums.
    """
    if not nums:
        return 0

    k = 1  # Start with the first element as unique
            # k = 0 no menaing (unique or duplicate)
    print(nums)
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            nums[k] = nums[i]
            print(i, nums)
            k += 1
    return k

def removeElement(nums):
    """
    Given an integer array nums and an integer val, 
    remove all occurrences of val in nums in-place. 
    The order of the elements may be changed. 
    Then return the number of elements in nums which are not equal to val.
    """
    k = 0  # Initialize the counter for elements not equal to val
    val = 3
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k
    # t = 3
    # i = 0
    # while True:
    #     print(nums, i)
    #     if i > len(nums) - 1:
    #         break
    #     if nums[i] == t:
    #         del nums[i]
    #         i = 0
    #     else:
    #         i += 1
    # return len(nums)
    

def majorityElement(nums):
    """
    Given an array nums of size n, return the majority element.
    The majority element is the element that appears more than ⌊n / 2⌋ times.
    You may assume that the majority element always exists in the array.
    """
    # count = 0
    # candidate = None
    # for num in nums:
    #     if count == 0:
    #         candidate = num
    #     count += (1 if num == candidate else -1)
    #     print(candidate, count)
    # return candidate
    from collections import Counter
    c = Counter(nums)
    max = 0
    o = None
    for i in c.most_common():
        if i[1] > max:
            max = i[1]
            o = i[0]

    return o


def maxProfit(prices):
    """
    You are given an array prices where prices[i] is the price of a given 
    stock on the ith day. You want to maximize your profit by choosing a 
    single day to buy one stock and choosing a different day in the future to sell that stock.
    Return the maximum profit you can achieve from this transaction. 
    If you cannot achieve any profit, return 0.
    """
    # if not prices:
    #     return 0
    # m = nums.index(min(nums))
    # max = 0
    # for i in range(m, len(nums)):
    #     if nums[i] > nums[m]:
    #         d = nums[i] - nums[m]
    #         if d > max:
    #             max = d
    # return max
    # if not prices:
    #     return 0

    min_price = float('inf')
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
            # print(min_price)
        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit


def lengthOfLastWord(str1):
    """
    Given a string s consisting of words and spaces, return the length of the last word in the string.
    """
    a = str1.split(" ")
    i = -1
    while True:
        if len(a[i])  == 0:
            i -= 1
        else:
            return len(a[i])


def romanToInt(str1):
    a = list(str1)
    m = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    for k, v in enumerate(a):
        a[k] = m[v]

    for i in range(0, len(a) - 1):
        # if a[i] == 1 and a[i+1] == 5:
        #     a[i] = -abs(a[i])
        # elif a[i] == 1 and a[i+1] == 10:
        #     a[i] = -abs(a[i])
        # elif a[i] == 10 and a[i+1] == 50:
        #     a[i] = -abs(a[i])
        # elif a[i] == 10 and a[i+1] == 100:
        #     a[i] = -abs(a[i])
        # elif a[i] == 100 and a[i+1] == 500:
        #     a[i] = -abs(a[i])
        # elif a[i] == 100 and a[i+1] == 1000:
        #     a[i] = -abs(a[i])    
        r = a[i+1] / a[i]
        if r == 5 or r == 10:
            a[i] = -abs(a[i])            

    sum = 0
    for i in range(0, len(a)):
        sum += a[i]

    print(sum)


def longestCommonPrefix(strs: list[str]):
    short = 999999999
    for x in strs:
        if len(x) == 0:
            return ""
        if len(x) < short:
            short = len(x)

    for i in range(1, len(strs)):
        if strs[i -1][0] != strs[i][0]:
            return ""
    count = 1 
    if short >= 1:
        j = None
        for j in range(1, short):
            b = False
            for i in range(1, len(strs)):
                if strs[i-1][j] != strs[i][j]:
                    b = True
                    break
                
            if b:
                break
            else:
                count += 1
    return strs[0][0:count]
                

def strStr(haystack, needle):
    r = haystack.split(needle)
    if len(r) == 1:
        return -1
    else:
        for k, v in enumerate(r):
            if v == '':
                return k
            else:
                return len(r[0])
"""
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.
"""
def merge(nums1, m, nums2, n):
    for k, v in enumerate(nums1):
        if v == 0 and len(nums2) > 0:
            nums1[k] = nums2.pop()

    nums1.sort()


def isPalindrome(s: str):
    import re
    s = re.sub('[^0-9a-zA-Z]', '', s)
    s = s.lower()
    a = list(s)
    j = -1
    for i in range(0, len(a)):
        if a[i] != a[j]:
            return False
        j -= 1
    return True


def beautifulWord(s: str):
    count = 0 
    for i in range(1, len(s)):
        if s[i-1] == s[i]:
            count += 1
            continue
        if ord(s[i-1]) == ord(s[i]) - 1:
            count += 1
            continue
    if count > 1:
        print(count-1)
    else:
        print(count)


def removeChar(s: str):
    w = "v"
    s = list(s)
    while w in s:
        s.remove(w)
    print(''.join(s))


def isSubsequence(sub: str, whole: str) -> bool:
    if len(sub) == 0:
        return True
    if len(sub) == len(whole):
        return sub == whole
    if len(sub) > len(whole):
        return False
    last = 0
    for s in sub:
        res = whole.split(s)
        print(res)
        if len(res[0]) == len(whole):
            return False
        if len(res[0]) >= last:
            last = len(res[0])
            continue
        else:
            return False

    return True


if __name__ == '__main__':
    x = isSubsequence("aaaaaa", "bbaaaa")
    print(x)
