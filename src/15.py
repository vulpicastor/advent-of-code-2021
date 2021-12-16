#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import heapq
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

import tulun

YEAR = 2021
DAY = 15

# def dijkstra(graph, start, dest):
#     parents = collections.defaultdict(lambda: None)
#     i = [0, start]
#     distances = {start: i}
#     queue = [i]
#     for v in graph.values():
#         if v is start:
#             continue
#         else:
#             i = [np.inf, start]
#             distances
#             distances.append((np.inf, s))


#     queue = [(0, source)]
#     while queue:
#         visit = heapq.heappop(queue)
#         for neighbor in visit:



def graphy(grid):
    x, y = grid.shape
    out = tulun.Digraph()
    for i, j in itertools.product(range(x), range(y)):
        if i + 1 < x:
            last = f'{i}, {j}'
            for k in range(grid[i+1, j]-1):
                new_node = f'{i+1}, {j}, i, {k}'
                out[last, new_node] = 1
                last = new_node
            out[last, f'{i+1}, {j}'] = 1
        if j + 1 < y:
            last = f'{i}, {j}'
            for k in range(grid[i, j+1]-1):
                new_node = f'{i}, {j+1}, j, {k}'
                out[last, new_node] = 1
                last = new_node
            out[last, f'{i}, {j+1}'] = 1
            # out[f'{i}, {j}', f'{i}, {j+1}'] = grid[i, j+1]
            # out[(i, j), (i, j+1)] = grid[(i, j+1)]
    return out


def grid_inc(grid, inc):
    grids = [grid]
    new_grid = grid
    for i in range(inc):
        new_grid = (new_grid % 9) + 1
        grids.append(new_grid)
    return grids

def block_grid(grid, nrow=5, ncol=5):
    grids = grid_inc(grid, (nrow-1)*(ncol-1))
    blocks = []
    for i in range(nrow):
        row = []
        for j in range(ncol):
            row.append(grids[i + j])
        blocks.append(row)
    return np.block(blocks)

def parse_key(k):
    parts = k.split(', ')
    if len(parts) == 4:
        return None
    else:
        return int(parts[0]), int(parts[1])

def trace(grid, parents, start, end):
    # dist = [grid[parse_key(end.k)]]
    dist = []
    visit = end
    while visit is not start:
        k = parse_key(visit.k)
        if k is not None:
            dist.append(grid[k])
        visit = parents[visit]
    return dist

def main():
    data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([list(map(int, l)) for l in data.split('\n')])
    
    print(inlist)

    mygraph = graphy(inlist)
    x, y = inlist.shape
    start = mygraph['0, 0']
    end = mygraph[f'{x-1}, {y-1}']
    print(start)
    print(end)
    dist, parents = start.bfs(end)
    # print(dist)
    # print(parents)
    answer = dist[end]
    print(answer)
    # print([k for k in mygraph['8, 8']])

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    big_grid = block_grid(inlist)
    print(big_grid[489:, 489:])
    print('\n'.join(''.join(str(c) for c in r) for  r in big_grid))
    biggraph = graphy(big_grid)
    x, y = big_grid.shape
    start = biggraph['0, 0']
    end = biggraph[f'{x-1}, {y-1}']
    print(start)
    print(end)
    dist, parents = start.bfs(end)
    answer = dist[end]

    trace_dist = trace(big_grid, parents, start, end)
    # print(trace_dist)
    print(trace_dist)
    print(answer)
    print(sum(trace_dist))
    print(trace(big_grid, parents, start, end))


    # aocd.submit(answer, part='b', day=DAY, year=YEAR)
    return big_grid, biggraph, trace_dist


if __name__ == '__main__':
    big_grid, biggraph, trace_dist = main()
