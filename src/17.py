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
DAY = 17


def search_vx_range(x_lower, x_upper):
    vx_lower = np.ceil(0.5 * (np.sqrt(8 * x_lower - 1) - 1))
    vx_upper = np.floor(0.5 * (np.sqrt(8 * x_upper - 1) - 1))
    return int(vx_lower), int(vx_upper)

def search_ymax(vx, y_lower, y_upper):
    last_y_max = 0
    last_vy_initial = 0
    last_y_final_lower = 0
    last_y_final_upper = 0
    for vy_initial in itertools.count(1):
        y_max = vy_initial * (vy_initial + 1) / 2
        dy_lower = y_max - y_upper
        dy_upper = y_max - y_lower
        vy_final_lower = np.ceil(0.5 * (np.sqrt(8 * dy_lower - 1) - 1))
        vy_final_upper = np.floor(0.5 * (np.sqrt(8 * dy_upper - 1) - 1))
        # if vy_initial + vy_final_lower + 1 < vx:
            # pass
        # if vy_final_upper < y_upper or vy_final_lower
        y_final_upper = y_max - vy_final_lower * (vy_final_lower + 1) / 2
        y_final_lower = y_max - vy_final_upper * (vy_final_upper + 1) / 2
        if y_final_upper < y_lower: # y_lower and y_final_lower > y_upper:
            break
        last_y_max = y_max
        last_vy_initial = vy_initial
        last_y_final_upper = y_final_upper
        last_y_final_lower = y_final_lower
        # if vy_final_upper < vy_final_lower:
            # break
    return last_y_max, last_vy_initial, last_y_final_lower, last_y_final_upper, y_final_upper, y_final_lower

def x_end(vx):
    return vx * (vx + 1) // 2

def step(pos, vel):
    pos += vel
    vel += np.array([-np.sign(vel[0]), -1.])

def search_ymax_2(y_lower, y_upper):
    last_y_max = 0
    last_vy_initial = 0
    count = 0
    for vy_initial in range(1, abs(y_lower) + 1):
        y_max = vy_initial * (vy_initial + 1) // 2
        vy_final = (np.sqrt(8 * (y_max - y_upper) - 1) - 1) // 2 - 1
        while True:
            y_final = y_max - vy_final * (vy_final + 1) // 2
            if y_final <= y_upper:
                break
            vy_final += 1
        print(vy_initial, y_max, vy_final, y_final)
        if y_final < y_lower:
            continue
        last_vy_initial = vy_initial
        last_y_max = y_max
        # count += 
        print(last_vy_initial, last_y_max)
    return last_y_max, last_vy_initial

        # vy_final
        # vy_final = vy_final_lower
        # last_y_final = y_max - vy_final_lower * (vy_final_lower + 1) // 2
        # y_final = last_y_final
        # while y_final > y_upper:
            # vy_final += 1
            # last_y_final = y_max - vy_final_lower * (vy_final_lower + 1) // 2
        # last_y_max = v_max


def main():
    # data = aocd.get_data(day=DAY, year=YEAR)
    # inlist = data.split('\n')
    lol = "target area: x=79..137, y=-176..-117"
    x_lower = 79
    x_upper = 137
    y_lower = -176
    y_upper = -117

    vx_lower, vx_upper = search_vx_range(x_lower, x_upper)
    print(vx_lower, vx_upper)
    print(x_end(vx_lower-1), x_end(vx_upper))
    # y_maxes = []
    # for vx in range(vx_lower, vx_upper+1):
    #     y_max, _, _, _, _, _ = search_ymax(vx, y_lower, y_upper)
    #     print(search_ymax(vx, y_lower, y_upper))
    #     y_maxes.append(y_max)
    for vx in range(6, 7+1):
        print(search_ymax_2(vx, -10, -5))
    for vx in range(vx_lower, vx_upper+1):
        print(search_ymax_2(vx, y_lower, y_upper))
    # print(search_ymax(6, -10, -5))
    # print(search_ymax(7, -10, -5))

    # answer = int(max(y_maxes))
    vy_initial = abs(y_lower) - 1
    answer = vy_initial * (vy_initial + 1) // 2
    print(answer)
    # print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
