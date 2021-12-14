#!/usr/bin/env python3

import collections

import aocd

YEAR = 2021
DAY = 14


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


def count(digraphs):
    out = collections.Counter()
    for d, n in digraphs.items():
        a, b = d
        out[a] += n
        out[b] += n
    return out


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

    digraph_ctr = collections.Counter([a + b for a, b in zip(template[:-1], template[1:])])
    # Digraphs double count each character... except the head and tail.
    # Append a space at the start and end of the string to get the count right.
    digraph_ctr[' ' + template[0]] = 1
    digraph_ctr[template[-1] + ' '] = 1

    for _ in range(10):
        step(digraph_ctr, rule_dict)
    result = count(digraph_ctr).most_common()
    # Un-double count individual characters.
    # The second term is result[-2] because the last one is always (' ', 2).
    answer = result[0][1] // 2 - result[-2][1] // 2
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    for _ in range(30):
        step(digraph_ctr, rule_dict)
    result = count(digraph_ctr).most_common()
    answer = result[0][1] // 2 - result[-2][1] // 2
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
