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
DAY = 14


def sub(s, rule_dict):
    out = []
    for a, b in zip(s[:-1], s[1:]):
        out.append(a)
        key = a + b
        if key in rule_dict:
            out.append(rule_dict[key])
    out.append(s[-1])
    return out

def step(digraphs, rule_dict):
    for d, n in list(digraphs.items()):
        if digraphs[d] <= 0:
            continue
        if d in rule_dict:
            digraphs[d] -= n
            a, b = d
            k = rule_dict[d]
            digraphs[a + k] += n
            digraphs[k + b] += n


def main():
    data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
    data = aocd.get_data(day=DAY, year=YEAR)
    template, rules_str = data.split('\n\n')
    rules = [l.split(' -> ') for l in rules_str.split('\n')]
    rule_dict = dict(rules)
    # print(rule_dict)

    result = list(template)
    for _ in range(10):
        result = sub(result, rule_dict)
        # print(''.join(result))
    ctr = collections.Counter(result)
    print(ctr.most_common())
    cnt = ctr.most_common()
    answer = cnt[0][1] - cnt[-1][1]
    print(answer)
    # for c in result:
        # ctr[c] += 1
    # print(Counter)

    digraph_ctr = collections.Counter([a + b for a, b in zip(template[:-1], template[1:])])
    digraph_ctr[' ' + template[0]] = 1
    digraph_ctr[template[-1] + ' '] = 1
    print(digraph_ctr)
    # digraphs = collections.defaultdict(int)
    # digraphs.update(digraph_ctr)
    for _ in range(40):
        step(digraph_ctr, rule_dict)
    print(digraph_ctr)
    ungraphs = collections.Counter()
    for d, n in digraph_ctr.items():
        a, b = d
        ungraphs[a] += n
        ungraphs[b] += n
    result = ungraphs.most_common()
    answer = result[0][1] // 2 - result[-2][1] // 2
    print(answer)


    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
