import time
import matplotlib.pyplot as plt
from random import randint
from bm import bm
from simple import strStr


def random_with_n_digits(n):
    if n < 1:
        n = 1
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def show_runtime(pattern, *algorithms):
    datasize = [i+1 for i in range(0, 10)]
    plt.xlabel('datasize(10k)')
    plt.ylabel('runtime(ms)')
    for algorithm in algorithms:
        runtime = []
        for i in datasize:
            start_time = time.time() * 100000
            algorithm(get_string(i), pattern)
            end_time = time.time() * 100000
            runtime.append(end_time - start_time)
        plt.plot(datasize, runtime)
    plt.show()



def get_string(n):
    string = []
    file = open("assignment1/pai.txt", "r")
    count = 0
    for line in file:
        if count < n:
            string.append(line.replace('\n', ''))
            count += 1
        else:
            break
    file.close()
    return string


if __name__ == '__main__':
    pattern = str(random_with_n_digits(10))
    show_runtime(pattern, bm, strStr)

