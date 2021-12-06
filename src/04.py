#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2021
DAY = 4

SHAPE = (5, 5)


def make_board(block):
    lines = block.split('\n')
    b = np.zeros(SHAPE, dtype=int)
    for i, l in enumerate(lines):
        b[i, :] = np.array(list(map(int, l.split())))
    return b


def check_win(board):
    return (
        np.any(np.sum(board, axis=0) == SHAPE[1]) or
        np.any(np.sum(board, axis=1) == SHAPE[0])
    )


def advance_board(n, bingo, board):
    board[:] = np.logical_or(bingo==n, board)


def calc_score(n, bingo, board):
    return np.sum(bingo[np.logical_not(board)]) * n


def part_a(draws, bingos, boards):
    for n in draws:
        for bingo, board in zip(bingos, boards):
            advance_board(n, bingo, board)
            if check_win(board):
                return calc_score(n, bingo, board)


def part_b(draws, bingos, boards):
    last_win_bingo = None
    last_win_board = None
    last_draw = 0
    won = [False] * len(bingos)
    for n in draws:
        for i, (bingo, board) in enumerate(zip(bingos, boards)):
            if won[i]:
                continue
            advance_board(n, bingo, board)
            if check_win(board):
                last_win_bingo = bingo
                last_win_board = board
                last_draw = n
                won[i] = True
    return calc_score(last_draw, last_win_bingo, last_win_board)


def main():
    test_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = data.split('\n\n')
    draws = list(map(int, inlist[0].split(',')))
    bingos = list(map(make_board, inlist[1:]))
    boards = [np.zeros(SHAPE, dtype=bool) for _ in bingos]

    answer = part_a(draws, bingos, boards)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = part_b(draws, bingos, boards)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
