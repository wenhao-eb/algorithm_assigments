import time
import matplotlib.pyplot as plt
from random import randint
from bm import bm
from naive import naive
from kmp import kmp
from kmp_nextval import kmp_next_val
from sunday import sun


def random_with_n_digits(n):
    if n < 1:
        n = 1
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def show_runtime(*algorithms):
    datasize = [i + 1 for i in range(0, 10)]
    string = get_string()
    plt.xlabel('datasize(10k)')
    plt.ylabel('runtime(ms)')
    for algorithm in algorithms:
        runtime = []
        for i in datasize:
            start_time = time.time()
            sub_string = string[:i * 100000]
            algorithm(sub_string, sub_string[len(sub_string) - 1001:len(sub_string) - 1])
            end_time = time.time()
            runtime.append((end_time - start_time))
        plt.plot(datasize, runtime, label=algorithm.__name__)
    plt.legend()
    plt.show()


def get_string():
    string = []
    file = open("pai.txt", "r")
    for line in file:
        if not line.startswith('>'):
            string.append(line.replace('\n', ''))
    string = ''.join(string)
    file.close()
    return string


show_runtime(bm, naive, kmp_next_val, kmp, sun)
