def calShiftMat(st):
    dic = {}
    for i in range(len(st) - 1, -1, -1):
        if not dic.get(st[i]):
            dic[st[i]] = len(st) - i
    dic["end"] = len(st) + 1
    return dic

def BM(txt, pat: str):



    if len(pat) > len(txt): return -1
    if pat == "": return 0

    # 偏移表
    dic = calShiftMat(pat)
    idx = 0

    while idx + len(pat) <= len(txt):

        # 待匹配字符串
        str_cut = txt[idx:idx + len(pat)]

        # 判断是否匹配
        if str_cut == pat:
            return idx
        else:
            # 边界处理
            if idx + len(pat) >= len(txt):
                return -1
            # 不匹配情况下，根据下一个字符的偏移，移动idx
            cur_c = txt[idx + len(pat)]
            if dic.get(cur_c):
                idx += dic[cur_c]
            else:
                idx += dic["end"]

    return -1 if idx + len(pat) >= len(txt) else idx

print(BM('laksdjflasdkjfla12312sdfasdfsdjfalsdkf','sdkf'))