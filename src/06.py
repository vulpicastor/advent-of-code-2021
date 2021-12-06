#/usr/bin/env python3

import collections

import aocd

YEAR = 2021
DAY = 6


def evolve(counts, days):
    new_counts = collections.deque(counts)
    for _ in range(days):
        new_counts.append(new_counts.popleft())
        new_counts[6] += new_counts[8]
    return new_counts


def main():
    data = "3,4,3,1,2"
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = list(map(int, data.split(',')))
    counts = [0] * 9
    for i in inlist:
        counts[i] += 1

    answer = sum(evolve(counts, 80))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(evolve(counts, 256))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
