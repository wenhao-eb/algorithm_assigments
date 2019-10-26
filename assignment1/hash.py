
import datetime
import math
# 参考博客： https://blog.csdn.net/every__day/article/details/86644814

# a是否在b中出现  a是模式串

# 设置一个很大的P
P = 26  #哈希映射表的长度


def contain(a, b):
    al = len(a)
    bl = len(b)
    if (al > bl): return -1

    # 计算P的al次方
    t = math.pow(P, al)
    # print(t)

    ah, bh = 0, 0
    # 计算a,b前缀的哈希值
    for i in range(al):
        ah = ah*P+ord(a[i])
        bh = bh*P+ord(b[i])


    # 对 b不断右移一位，更新哈希值并判断
    i = 0
    while i + al <= bl:
        if ah == bh:
            return i
        if i + al < bl:
            bh = bh * P + ord(b[i + al]) - ord(b[i]) * t
        i += 1

    return -1

# s = contain('example', 'this is an simple example')

if __name__ == "__main__":

    # print(strStr('this is an simple example','example'))


    string = str(open('./pai.txt','r',encoding='utf-8').readlines())
    start_time = datetime.datetime.now()

    pattern = "264338327950288419716939937510582097"
    fuben_string = string
    temp = []

    pre_chars = 0
    while len(fuben_string)>0:
        s=pre_chars+contain(fuben_string,pattern)

        if s!=-1:
            temp.append(s)
        pre_chars=s+len(pattern)

        fuben_string = string[pre_chars:]

        if len(temp)>=100:   #最多匹配个数
             break


    print(temp)
    print('匹配到的个数：',len(temp))


    end_time=datetime.datetime.now()
    print((end_time-start_time))