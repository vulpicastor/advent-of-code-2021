#/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

YEAR = 2021
DAY = 5



def part_a(lines):
    field = np.zeros((1000, 1000), dtype=int)
    for a, b in lines:
        if not np.any(a == b):
            continue
        x, y = a
        z, w = b
        hlo = min(x, z)
        hhi = max(x, z)
        wlo = min(y, w)
        whi = max(y, w)
        field[hlo:hhi+1, wlo:whi+1] += 1
    print(field)
    return np.sum(field >= 2)

def part_b(lines):
    field = np.zeros((1000, 1000), dtype=int)
    for a, b in lines:
        x, y = a
        z, w = b
        if np.any(a == b):
            hlo = min(x, z)
            hhi = max(x, z)
            wlo = min(y, w)
            whi = max(y, w)
            field[hlo:hhi+1, wlo:whi+1] += 1
        # elif abs(x-z) == abs(y-w):
        else:
            hdir = (z - x) // abs(z - x)
            wdir = (w - y) // abs(w - y)
            print(x, y, z, w, hdir, wdir)
            for i, j in zip(range(x, z+hdir, hdir), range(y, w+wdir, wdir)):
                field[i, j] += 1
    print(field)
    return np.sum(field >= 2)

def parse_line(line):
    a, b = line.split(' -> ')
    x, y = a.split(',')
    z, w = b.split(',')
    return [
        np.array([int(x), int(y)]),
        np.array([int(z), int(w)]),
    ]

def main():
    data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = data.split('\n')
    indata = list(map(parse_line, inlist))

    answer = part_b(indata)
    print(answer)

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
