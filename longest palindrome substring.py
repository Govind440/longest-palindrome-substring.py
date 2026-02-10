def longestPalindrome(s):
    start, max_len = 0, 0
    for i in range(len(s)):
        # Odd length
        left, right = i, i
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                start, max_len = left, right - left + 1
            left -= 1
            right += 1
        # Even length (similar for even)
    return s[start:start+max_len]