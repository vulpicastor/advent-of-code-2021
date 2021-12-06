#!/usr/bin/env python3

import numpy as np


def ba2int(ba):
    basis = np.array([2**i for i in range(len(ba)-1, -1, -1)])
    return ba @ basis

def calc_mask(ba):
    most_common = np.sum(ba, axis=0) >= (len(ba) / 2)
    least_common = np.logical_not(most_common)
    return most_common, least_common

def filterba(ba, flag=0):
    whittle = ba
    for i in range(ba.shape[1]):
        mask = calc_mask(whittle)[flag]
        whittle = whittle[whittle[:, i] == mask[i]]
        if whittle.shape[0] == 1:
            break
    return whittle.flatten()


def main():
    with open('input/03.txt') as f:
        inlist = [[int(i) for i in l.strip()] for l in f.readlines()]
    inarray = np.array(inlist)
    # Part 1.
    most_common, least_common = calc_mask(inarray)
    a = ba2int(most_common)
    b = ba2int(least_common)
    print(a, b, a*b)
    # Part 2.
    a = ba2int(filterba(inarray))
    b = ba2int(filterba(inarray, 1))
    print(a, b, a*b)


if __name__ == '__main__':
    main()
