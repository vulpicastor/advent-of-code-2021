#!/usr/bin/env python3

import numpy as np


DIRECTION = {
    "forward":  np.array([ 1,  0]),
    "down":     np.array([ 0,  1]),
    "up":       np.array([ 0, -1]),
}

def move(inlist):
    state = np.array([0, 0])
    for where, n in inlist:
        m = int(n)
        state += DIRECTION[where] * m
    return state

def move2(inlist):
    pos = np.array([0, 0])
    aim = 0
    for where, n in inlist:
        m = int(n)
        match where:
            case "forward":
                pos[0] += m
                pos[1] += m * aim
            case "down":
                aim += m
            case "up":
                aim -= m
    return pos


def main():
    with open("input/02.txt") as f:
        inlist = [x.split() for x in f.readlines()]
    x, y = move(inlist)
    print(x, y, x*y)
    x, y = move2(inlist)
    print(x, y, x*y)


if __name__ == '__main__':
    main()
