def generateBadChar(needle):
    badchar = []

    for i in range(256):
        badchar.append(-1)
    for i in range(len(needle)):
        badchar[ord(needle[i])] = i
    return badchar


def generateGS(needle):
    suffix = []
    prefix = []
    m = len(needle)
    for i in range(m):
        suffix.append(-1)
        prefix.append(False)
    for i in range(m - 1):
        j = i
        k = 0

        while (j >= 0 and needle[j] == needle[m - 1 - k]):
            j -= 1
            k += 1
            suffix[k] = j + 1
        if (j == -1):
            prefix[k] = True
    return suffix, prefix


def moveByGS(j, m, suffix, prefix):
    k = m - 1 - j
    if (suffix[k] != -1):
        return j - suffix[k] + 1
    r = j + 2
    while (r < m):
        if (prefix[m - r] == True):
            return r
        r += 1
    return m


def bm(haystack, needle):
    badchar = generateBadChar(needle)
    suffix, prefix = generateGS(needle)
    i = 0
    n = len(haystack)
    m = len(needle)
    while (i < n - m + 1):
        j = m - 1
        while (j >= 0):
            if (haystack[i + j] != needle[j]):
                break
            j -= 1
        if j < 0:
            return i

        moveLen1 = j - badchar[ord(haystack[i + j])]
        moveLen2 = 0
        if j < m - 1:
            moveLen2 = moveByGS(j, m, suffix, prefix)
        i = i + max(moveLen1, moveLen2)

    return -1
