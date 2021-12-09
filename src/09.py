#!/usr/bin/env python3

import collections

import numpy as np
import aocd

YEAR = 2021
DAY = 9


def find_low(grid):
    new_grid = np.full((grid.shape[0]+2, grid.shape[1]+2), 99999)
    new_grid[1:-1, 1:-1] = grid
    center = new_grid[1:-1, 1:-1]
    mask = np.ones_like(grid, dtype=bool)
    slices = [slice(1, -1), slice(1, -1), slice(2, None), slice(-2)]
    for i, j in zip(slices, reversed(slices)):
        mask = np.logical_and(mask, center < new_grid[i, j])
    return grid[mask], mask


def flood_map(grid, mask):
    basins = []
    visited = grid >= 9
    neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for i, j in zip(*np.where(mask)):
        if visited[i, j]:
            visited[(i, j)] += 1
            continue
        area = []
        bfs_queue = collections.deque([(i, j)])
        while bfs_queue:
            here = bfs_queue.popleft()
            if visited[here]:
                continue
            visited[here] = True
            area.append(here)
            for dx, dy in neighbors:
                x = here[0] + dx
                y = here[1] + dy
                if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
                    continue
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

    scores, mask = find_low(inlist)
    answer = np.sum(scores) + len(scores)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    basins = flood_map(inlist, mask)
    basin_size = sorted(map(len, basins))
    answer = np.prod(basin_size[-3:])
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
