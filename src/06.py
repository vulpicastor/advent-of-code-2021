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
DAY = 6



def evolve(inlist):
    outlist = []
    for i in inlist:
        if i == 0:
            outlist.append(6)
            outlist.append(8)
        else:
            outlist.append(i-1)
    return outlist

def evolve2(counts):
    outlist = [0]*9
    outlist[8] = counts[0]
    outlist[6] = counts[0]
    for i in range(1, 9):
        outlist[i-1] += counts[i]
    return outlist


def main():
    data = "3,4,3,1,2"
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = list(map(int, data.split(',')))
    counts = [0] * 9
    for i in inlist:
        counts[i] += 1

    outlist = inlist
    for _ in range(80):
        outlist = evolve(outlist)
        # print(outlist)
    print(outlist)
    answer = len(outlist)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    outcount = counts
    for _ in range(256):
        outcount = evolve2(outcount)
        print(outcount)
    answer = sum(outcount)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
