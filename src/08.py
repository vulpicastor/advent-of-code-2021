#!/usr/bin/env python3

import aocd

YEAR = 2021
DAY = 8

DIGIT_SEGS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}
SEG_DIGITS = {v: k for k, v in DIGIT_SEGS.items()}


def part_a(inlist):
    count = 0
    for _, b in inlist:
        for i in b:
            n = len(i)
            if n in (2, 3, 4, 7):
                count += 1
    return count


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
        list(a)[0]: 'a',
        list(b)[0]: 'b',
        list(c)[0]: 'c',
        list(d)[0]: 'd',
        list(e)[0]: 'e',
        list(f)[0]: 'f',
        list(g)[0]: 'g',
    }
    return sum(
        10**i * SEG_DIGITS[''.join(sorted(map(lambda x: mapping[x], s)))]
        for i, s in enumerate(reversed(outhalf))
    )


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

    answer = part_a(inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(map(decode_output, inlist))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
