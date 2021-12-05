#/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2021
DAY = 5

SHAPE = (1000, 1000)


def solve(lines, diag=False):
    field = np.zeros(SHAPE, dtype=int)
    for a, b in lines:
        x, y = a
        z, w = b
        hdir = np.sign(z - x) if x != z else 1
        wdir = np.sign(w - y) if y != w else 1
        if np.any(a == b):
            # In the case x == z, the slice reduces to x:x+1:1 aka just x.
            field[x:z+hdir:hdir, y:w+wdir:wdir] += 1
        elif diag:
            for i, j in zip(range(x, z+hdir, hdir), range(y, w+wdir, wdir)):
                field[i, j] += 1
    return np.sum(field >= 2)


def parse_line(line):
    return [np.array([int(x) for x in a.split(',')]) for a in line.split(' -> ')]


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
    inlines = list(map(parse_line, inlist))

    answer = solve(inlines)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = solve(inlines, True)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
