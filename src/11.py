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
import aocd

YEAR = 2021
DAY = 11


def step(grid):
    grid += 1
    flash = np.zeros_like(grid, dtype=bool)
    while np.any(grid[~flash] > 9):
        new_flash = (grid > 9) ^ flash
        grid[:-1, :-1] += new_flash[1:, 1:]
        grid[:-1, :] += new_flash[1:, :]
        grid[:-1, 1:] += new_flash[1:, :-1]
        grid[:, :-1] += new_flash[:, 1:]
        grid[:, 1:] += new_flash[:, :-1]
        grid[1:, :-1] += new_flash[:-1, 1:]
        grid[1:, :] += new_flash[:-1, :]
        grid[1:, 1:] += new_flash[:-1, :-1]
        flash |= new_flash
    grid[flash] = 0
    return flash


def main():
    data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([list(map(int, l)) for l in data.split('\n')])
    print(inlist)

    grid = inlist.copy()
    num_flashes = 0
    for i in range(100):
        num_flashes += np.sum(step(grid))
    print(num_flashes)
    answer = num_flashes

    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    grid = inlist.copy()
    for i in itertools.count(1):
        flash = step(grid)
        if np.all(flash):
            answer = i
            break
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
