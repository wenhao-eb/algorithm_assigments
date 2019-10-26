def get_bmbc(pattern):
    # 预生成坏字符表
    bmbc = dict()
    for i in range(len(pattern) - 1):
        char = pattern[i]
        # 记录坏字符最右位置（不包括模式串最右侧字符）
        bmbc[char] = i + 1
    return bmbc


def get_bmgs(pattern):
    # 预生成好后缀表
    bmgs = dict()

    # 无后缀仅根据坏字移位符规则
    bmgs[''] = 0

    for i in range(len(pattern)):

        # 好后缀
        GS = pattern[len(pattern) - i - 1:]

        for j in range(len(pattern) - i - 1):

            # 匹配部分
            NGS = pattern[j:j + i + 1]

            # 记录模式串中好后缀最靠右位置（除结尾处）
            if GS == NGS:
                bmgs[GS] = len(pattern) - j - i - 1
    return bmgs


def bm(string, pattern):
    """
    Boyer-Moore算法实现字符串查找
    """
    m = len(pattern)  # 子串
    n = len(string)  # 父串
    i = 0
    j = m
    indies = []
    bmbc = get_bmbc(pattern=pattern)  # 坏字符表
    bmgs = get_bmgs(pattern=pattern)  # 好后缀表
    while i < n:
        while (j > 0):
            if i + j - 1 >= n:  # 当无法继续向下搜索就返回值
                return indies

            # 主串判断匹配部分
            a = string[i + j - 1:i + m]

            # 模式串判断匹配部分
            b = pattern[j - 1:]

            # 当前位匹配成功则继续匹配
            if a == b:
                j = j - 1

            # 当前位匹配失败根据规则移位
            else:
                i = i + max(bmgs.setdefault(b[1:], m), j - bmbc.setdefault(string[i + j - 1], 0))
                j = m

            # 匹配成功返回匹配位置
            if j == 0:
                indies.append(i)
                i += 1
                j = len(pattern)
