#/usr/bin/env python3

import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import scipy.stats as stats


def ba2int(ba):
    basis = np.array([2**(i) for i in range(len(ba)-1, -1, -1)])
    print(basis)
    return ba @ basis

def calc_mask(ba):
    # most_common, _ = stats.mode(ba, axis=0)
    most_common = np.sum(ba, axis=0) >= (len(ba) / 2)
    # most_common = most_common.flatten()
    least_common = np.sum(ba, axis=0) < (len(ba) / 2)
    # least_common = np.logical_not(most_common)
    return most_common, least_common

def filterba(ba, flag=0):
    whittle = ba
    for i in range(ba.shape[1]):
        mask = calc_mask(whittle)[flag]
        print(mask)
        print(whittle[:, i])
        whittle = whittle[whittle[:, i] == mask[i]]
        # new_mask = calc_mask(whittle)
        # mask = new_mask[flag]
        print(whittle)
        if whittle.shape[0] == 1:
            break
    return whittle.flatten()

def main():
    with open('input/03.txt') as f:
        inlist = [[int(i) for i in l.strip()] for l in f.readlines()]
    inarray = np.array(inlist, dtype=bool)
    most_common, _ = stats.mode(inarray, axis=0)
    most_common = most_common.flatten()
    least_common = np.logical_not(most_common)
    print(most_common)
    print(ba2int(most_common) * ba2int(least_common))
    a = ba2int(filterba(inarray))
    b = ba2int(filterba(inarray, 1))
    print(
        a, b, a*b
    )
    

    


if __name__ == '__main__':
    main()
