#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2021
DAY = 13

AXIS_MAP = {'x': 0, 'y': 1}
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
    len_edge = a.shape[axis]
    recto_end = fold
    verso_start = fold + 1

    len_recto = fold
    len_verso = len_edge - verso_start

    if len_recto >= len_verso:
        out = a[index(slice(0, recto_end), axis)].copy()
        out[index(slice(-len_verso, None), axis)] |= a[
            index(slice(len_edge, verso_start-1, -1), axis)]
    else:
        out = a[index(slice(verso_start, None), axis)].copy()
        out[index(slice(len_recto), axis)] |= a[
            index(slice(len_recto, -1, -1), axis)]
    return out


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

    out = origami(paper, *arg_list[0])
    answer = np.sum(out)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    out = paper
    for args in arg_list:
        out = origami(out, *args)
    print(paper_str(out))


if __name__ == '__main__':
    main()
