#!/usr/bin/env python3

import collections

import aocd

import tulun

YEAR = 2021
DAY = 12


def recursive_walk(node, dest, visited=None):
    if node is dest:
        return 1
    if visited is None:
        visited = {node}
    path_list = []
    for neighbor in node:
        if neighbor in visited:
            continue
        if neighbor.k.islower():
            visited.add(neighbor)
        num_child_path = recursive_walk(neighbor, dest, visited)
        if neighbor.k.islower():
            visited.remove(neighbor)
        if num_child_path > 0:
            path_list.append(num_child_path)
    if path_list:
        return sum(path_list)
    return 0

def recursive_walk_2(node, dest, visited=None, can_visit_twice=True):
    if node is dest:
        return 1
    if visited is None:
        visited = collections.defaultdict(int)
        visited[node] = 1000
    path_list = []
    for neighbor in node:
        twice = can_visit_twice
        if neighbor.k.islower():
            if visited[neighbor] >= 2:
                continue
            if visited[neighbor] >= 1:
                if not twice:
                    continue
                twice = False
        visited[neighbor] += 1
        num_child_path = recursive_walk_2(neighbor, dest, visited, twice)
        visited[neighbor] -= 1
        if can_visit_twice:
            twice = None
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

    answer = recursive_walk(cave_graph['start'], cave_graph['end'])
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = recursive_walk_2(cave_graph['start'], cave_graph['end'])
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
