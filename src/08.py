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
DAY = 8

DIGIT_SEGS = {
    0: str('abcefg'),
    1: str('cf'),
    2: str('acdeg'),
    3: str('acdfg'),
    4: str('bcdf'),
    5: str('abdfg'),
    6: str('abdefg'),
    7: str('acf'),
    8: str('abcdefg'),
    9: str('abcdfg'),
}
SEG_DIGITS = {v: k for k, v in DIGIT_SEGS.items()}

# print(DIGIT_SEGS[2] & DIGIT_SEGS[3] & DIGIT_SEGS[5])

def decode_output(pair):
    inhalf, outhalf = pair
    fives = []  # 2, 3, 5
    sixes = []  # 0, 6, 9
    for s in inhalf:
        match len(s):
            case 2:
                one = set(s)
            case 3:
                seven = set(s)
            case 4:
                four = set(s)
            case 5:
                fives.append(set(s))
            case 6:
                sixes.append(set(s))
            case 7:
                eight = set(s)
    mapping = {}
    a = seven - one
    bd = four - one
    adg = fives[0].intersection(*fives[1:])
    g = adg - bd - a
    d = adg - a - g
    b = bd - d
    abgf = sixes[0].intersection(*sixes[1:])
    f = abgf - a - b - g
    c = one - f
    e = eight - a - b - c - d - f - g
    mapping = {
        'a': list(a)[0],
        'b': list(b)[0],
        'c': list(c)[0],
        'd': list(d)[0],
        'e': list(e)[0],
        'f': list(f)[0],
        'g': list(g)[0],
    }
    rev_mapping = {v: k for k, v in mapping.items()}
    outlist = [SEG_DIGITS[''.join(sorted(map(lambda x: rev_mapping[x], s)))] for s in outhalf]
    print(outlist)
    return int(''.join(map(str, outlist)))


def main():
    data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [[a.split() for a in l.split(' | ')] for l in data.split('\n')]
    # print(inlist)
    count = 0
    for _, b in inlist:
        for i in b:
            n = len(i)
            if n == 2 or n == 4 or n == 3 or n == 7:
                count += 1
    print(count)
    answer = count
    # inlist = []
    # for l in inlines:
        # a, b = l.split(' | ')
        # inlist.append()
    answer = sum(map(decode_output, inlist))
    print(answer)

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
