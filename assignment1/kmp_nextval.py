def get_next_val(sub):
    _next = [0] * len(sub)
    _next[0] = -1
    i = 0
    j = -1
    while i < len(sub) - 1:
        if j == -1 or sub[i] == sub[j]:
            i += 1
            j += 1
            if sub[i] != sub[j]:
                _next[i] = j
            else:
                _next[i] = _next[j]
        else:
            j = _next[j]
    return _next


def kmp_next_val(txt, sub):
    _next = get_next_val(sub)
    i = 0
    j = 0
    while i < len(txt) and j < len(sub):
        if j == -1 or txt[i] == sub[j]:
            i += 1
            j += 1
        else:
            j = _next[j]
    if j == len(sub):
        return i - j
    return -1
