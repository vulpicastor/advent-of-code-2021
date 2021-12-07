#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2021
DAY = 7


def l1_norm(pos):
    return lambda x: np.sum(np.abs(pos - x), axis=-1)


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
    loss_a = l1_norm(inlist)
    loss_b = arith_norm(inlist)
    guesses = np.atleast_2d(np.arange(np.min(inlist), np.max(inlist)+1)).T

    answer = np.min(loss_a(guesses))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = np.min(loss_b(guesses))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
