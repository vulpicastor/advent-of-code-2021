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
DAY = 13


PAPER_FMT = ['.', '#']
def paper_str(p):
    real_p = p.T
    lines = []
    for row in real_p:
        lines.append(''.join(PAPER_FMT[int(i)] for i in row))
    return '\n'.join(lines)

def index(s, axis):
    out = [slice(None, None, None)] * 2
    out[axis] = s
    return tuple(out)

def origami(a, axis, fold):
    # print(a.shape, axis)
    len_edge = a.shape[axis]
    recto_end = fold
    verso_start = fold + 1

    len_recto = fold
    len_verso = len_edge - verso_start

    if len_recto >= len_verso:
        out = a[index(slice(0, recto_end), axis)].copy()
        # print(paper_str(out[index(slice(-len_verso, None), axis)]))
        out[index(slice(-len_verso, None), axis)] |= a[
            index(slice(len_edge, verso_start-1, -1), axis)]
    else:
        out = a[index(slice(verso_start, None), axis)].copy()
        out[index(slice(len_recto), axis)] |= a[
            index(slice(len_recto, -1, -1), axis)]

    # if pos >= len_verso:
    #     slice_recto_part = slice(fold-1, len_fold-1, -1)
    #     out[index(slice_recto_part, axis)] |= a[index(slice_verso, axis)]
    # else:
    #     slice_verso_part = slice(len_verso-1, -1, -1)
    #     out = a[index(slice_verso, axis)].copy()
    #     out[index(slice_verso_part, axis)] |= a[index(slice_verso, axis)]
    return out

AXIS_MAP = {'x': 0, 'y': 1}

def main():
    data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
    data = aocd.get_data(day=DAY, year=YEAR)
    coords_str, instr_str = data.split('\n\n')
    coords = np.array([list(map(int, l.split(','))) for l in coords_str.split()])
    paper_size = np.max(coords, axis=0) + 1
    paper = np.zeros(paper_size, dtype=bool)
    paper[coords[:, 0], coords[:, 1]] = True

    arg_list = []
    for l in instr_str.split('\n'):
        _, _, s = l.split()
        a, p = s.split('=')
        arg_list.append((AXIS_MAP[a], int(p)))

    # print(paper_str(paper))
    # print()
    out = origami(paper, *arg_list[0])
    answer = np.sum(out)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)


    out = paper
    for args in arg_list:
        out = origami(out, *args)

    print(paper_str(out), '\n')


    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
