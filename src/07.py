#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import scipy.optimize as optimize
import aocd

YEAR = 2021
DAY = 7


def l1_norm(pos):
    return (
        lambda x: np.sum(np.abs(pos - x), axis=-1),
        lambda x: np.sum((x > pos).astype(np.int) - (x < pos).astype(np.int), axis=0),
    )

def arith_norm(pos):
    def loss(x):
        absdev = np.abs(pos - x)
        summa = absdev * (1 + absdev) // 2
        return np.sum(summa, axis=-1)
    return loss


def main():
    data = "16,1,2,0,4,2,7,1,2,14"
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array(list(map(int, data.split(','))))
    # loss, grad = l1_norm(inlist)
    loss = arith_norm(inlist)
    # print((inlist > 12).astype(np.int) - (inlist < 12).astype(np.int))
    # result = optimize.minimize_scalar(loss, bounds=(np.min(inlist), np.max(inlist)))
    # print(result)
    # center = round(result.x)
    # guess = [center-1, center, center+1]
    # print(list(map(loss, guess)))
    # answer = guess[np.argmin(map(loss, guess))]

    # brutal  = optimize.brute(
        # loss, (np.min(inlist), np.max())
    # )
    guesses = np.atleast_2d(np.arange(np.min(inlist), np.max(inlist)+1)).T
    # print(np.abs(inlist - guesses))
    print(loss(guesses))
    print(guesses.T)
    answer = np.min(loss(guesses))
    
    print(inlist)
    print(answer)
    

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
