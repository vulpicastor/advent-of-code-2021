#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2021
DAY = 10

OPEN_PAREN = '(<[{'
CLOSE_PAREN = ')>]}'
MAP_PAREN = {k: v for k, v in zip(CLOSE_PAREN, OPEN_PAREN)}
REMAP_PAREN = {v: k for k, v in zip(CLOSE_PAREN, OPEN_PAREN)}

SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
    None: 0,
}

RESCORE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
    None: 0,
}

def paren(s):
    stack = []
    sucess = True
    for c in s:
        if c in OPEN_PAREN:
            stack.append(c)
        if c in CLOSE_PAREN:
            p = stack.pop()
            if p != MAP_PAREN[c]:
                sucess = False
                break
    if sucess:
        c = None
        score = 0
        for k in reversed(stack):
            score *= 5
            score += RESCORE[k]
    else:
        score = None
    return c, score

def main():
    data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = data.split('\n')
    bad, answer_b = list(zip(*map(paren, inlist)))
    answer = sum(SCORE[b] for b in bad)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = int(np.median([x for x in answer_b if x is not None]))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
