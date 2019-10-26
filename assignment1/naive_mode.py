import datetime


def strStr(haystack, needle):
    n1 = len(haystack)
    n2 = len(needle)
    if n1 < n2: return -1

    def helper(i):
        haystack_p = i
        needle_q = 0
        while needle_q < n2:
            if haystack[haystack_p] != needle[needle_q]:
                return False
            else:
                haystack_p += 1
                needle_q += 1
        return True

    for i in range(n1 - n2 + 1):
        if helper(i):
            return i
    return -1


if __name__ == "__main__":

    # print(strStr('this is an simple example','example'))

    string = str(open('./pai.txt', 'r', encoding='utf-8').readlines())
    start_time = datetime.datetime.now()

    pattern = "264338327950288419716939937510582097"
    fuben_string = string
    temp = []

    pre_chars = 0
    while len(fuben_string) > 0:
        s = pre_chars + strStr(fuben_string, pattern)

        if s != -1:
            temp.append(s)
        pre_chars = s + len(pattern)

        fuben_string = string[pre_chars:]

        if len(temp) >= 100:  # 最多匹配个数
            break

    print(temp)
    print('匹配到的个数：', len(temp))

    end_time = datetime.datetime.now()
    print((end_time - start_time))
