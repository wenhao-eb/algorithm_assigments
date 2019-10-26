def bm(string, pattern):
    i = 0
    j = 0
    len1 = len(string)
    len2 = len(pattern)
    if len1 == 0 and len2 == 0:
        return 0
    while i < len1:
        j = 0
        while j < len2 and i < len1:
            if string[i] == pattern[j]:
                i += 1
                j += 1
            else:
                i = i - j + 1
                break
        if j == len2:
            return i - j
    return -1