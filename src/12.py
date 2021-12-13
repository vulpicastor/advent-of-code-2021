#!/usr/bin/env python3

import collections

import aocd

import tulun

YEAR = 2021
DAY = 12


def recursive_walk(node, dest, visit_limit=1, visited=None):
    if node is dest:
        return 1
    if visited is None:
        visited = collections.defaultdict(int)
        visited[node] = 1000
    path_list = []
    for neighbor in node:
        new_visit_limit = visit_limit
        if neighbor.k.islower():
            if visited[neighbor] >= visit_limit:
                continue
            if visited[neighbor] == visit_limit - 1:
                new_visit_limit = max(visit_limit - 1, 1)
        visited[neighbor] += 1
        num_child_path = recursive_walk(neighbor, dest, new_visit_limit, visited)
        visited[neighbor] -= 1
        path_list.append(num_child_path)
    return sum(path_list)


def main():
    data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    data = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    data = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    data = aocd.get_data(day=DAY, year=YEAR)
    edges = [l.split('-') for l in data.split('\n')]

    cave_graph = tulun.Graph(edges)

    answer = recursive_walk(cave_graph['start'], cave_graph['end'], visit_limit=1)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = recursive_walk(cave_graph['start'], cave_graph['end'], visit_limit=2)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
