#/usr/bin/env python3

import numpy as np


def count_inc(a):
    n = 0
    for i, j in zip(a[:-1], a[1:]):
        if j > i:
            n += 1
    return n

def sum_win(a):
    return a[:-2] + a[1:-1] + a[2:]


def main():
    with open("input/01.txt") as f:
        in_num = list(map(int, f.readlines()))
    print(count_inc(in_num))
    print(sum_win(np.array(in_num))[:10])
    print(count_inc(sum_win(np.array(in_num))))


if __name__ == '__main__':
    main()
