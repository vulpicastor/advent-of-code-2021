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
DAY = 9


def find_low(grid):
    new_grid = np.zeros((grid.shape[0]+2, grid.shape[1]+2), dtype=np.float64)
    new_grid[1:-1, 1:-1] = grid
    center = new_grid[1:-1, 1:-1]
    new_grid[ 0,  :] = np.inf
    new_grid[-1,  :] = np.inf
    new_grid[ :,  0] = np.inf
    new_grid[ :, -1] = np.inf
    mask = np.ones_like(grid, dtype=bool)
    mask = np.logical_and(mask, center < new_grid[1:-1, 0:-2])
    mask = np.logical_and(mask, center < new_grid[1:-1, 2:])
    mask = np.logical_and(mask, center < new_grid[0:-2, 1:-1])
    mask = np.logical_and(mask, center < new_grid[2:, 1:-1])
    return grid[mask], mask

def flood_map(grid, mask):
    basins = []
    visited = grid >= 9
    # print(grid.shape)
    # print(*np.where(mask))
    for i, j in zip(*np.where(mask)):
        # print()
        # print(i, j)
        if visited[i, j]:
            visited[(i, j)] += 1
            continue
        area = []
        bfs_queue = collections.deque([(i, j)])
        while bfs_queue:
            here = bfs_queue.popleft()
            if visited[here]:
                visited[here] += 1
                continue
            # print(here)
            visited[here] += 1
            area.append(here)
            for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            # for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if dx == 0 and dy == 0:
                    continue
                x = here[0] + dx
                y = here[1] + dy
                # print(x, y)
                # print('ha')
                # print(x < 0 , x >= grid.shape[0] , y < 0 , y >= grid.shape[1])
                if (x < 0 or x >= grid.shape[0]) or (y < 0 or y >= grid.shape[1]):
                    continue
                # print('oh')
                # if visited[x, y]:
                    # continue
                if grid[x, y] >= 9:
                    continue
                # print('kk')
                bfs_queue.append((x, y))
        basins.append(area)
    return basins


def main():
    data = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([list(map(int, l)) for l in data.split()])
    print(inlist)
    scores, mask = find_low(inlist)
    answer = np.sum(scores) + len(scores)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    basins = flood_map(inlist, mask)
    basin_size = sorted(map(len, basins))
    print(basin_size)
    answer = np.prod(basin_size[-3:])
    print(answer)


    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
