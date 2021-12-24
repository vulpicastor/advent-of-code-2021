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
import tqdm
import aocd

YEAR = 2021
DAY = 24



def run(instlist, inputs):
    regs = {k: 0 for k in 'wxyz'}
    input_iter = iter(inputs)
    for inst in instlist:
        tokens = inst.split()
        if len(tokens) == 2:
            regs[tokens[1]] = next(input_iter)
            continue
        cmd, a, b = tokens
        match b:
            case 'w' | 'x' | 'y' | 'z':
                val_b = regs[b]
            case _:
                val_b = int(b)
        match cmd:
            case 'add':
                func = op.add
            case 'mul':
                func = op.mul
            case 'div':
                func = op.floordiv
            case 'mod':
                func = op.mod
            case 'eql':
                func = lambda x, y: int(x == y)
        regs[a] = func(regs[a], val_b)
    return regs

REG_MAP = {
    'w': 0,
    'x': 1,
    'y': 2,
    'z': 3,
}
def compile(instlist):
    funclist = []
    for inst in instlist:
        tokens = inst.split()
        if len(tokens) == 2:
            funclist.append((0, REG_MAP[tokens[1]]))
            continue
        cmd, a, b = tokens
        match cmd:
            case 'add':
                func = op.add
            case 'mul':
                func = op.mul
            case 'div':
                func = op.floordiv
            case 'mod':
                func = op.mod
            case 'eql':
                func = lambda x, y: int(x == y)
        if b in 'wxyz':
            def step(regs, myfunc=func, reg_a=REG_MAP[a], reg_b=REG_MAP[b]):
                regs[reg_a] = myfunc(regs[reg_a], regs[reg_b])
        else:
            def step(regs, myfunc=func, reg_a=REG_MAP[a], val_b=int(b)):
                regs[reg_a] = myfunc(regs[reg_a], val_b)
        funclist.append((1, step))
    return funclist

def run_funclist(funclist, inputs):
    input_iter = iter(inputs)
    regs = [0] * 4
    for code, func in funclist:
        if code:
            func(regs)
            continue
        regs[func] = next(input_iter)
    return regs

def compile_simple(instlist):
    funclist = []
    for inst in instlist:
        if not inst:
            continue
        cmd, a, b = inst.split()
        match cmd:
            case 'add':
                func = op.add
            case 'mul':
                func = op.mul
            case 'div':
                func = op.floordiv
            case 'mod':
                func = op.mod
            case 'eql':
                func = lambda x, y: int(x == y)
        if b in 'wxyz':
            def step(regs, myfunc=func, reg_a=REG_MAP[a], reg_b=REG_MAP[b]):
                regs[reg_a] = myfunc(regs[reg_a], regs[reg_b])
        else:
            def step(regs, myfunc=func, reg_a=REG_MAP[a], val_b=int(b)):
                regs[reg_a] = myfunc(regs[reg_a], val_b)
        funclist.append(step)
    return funclist

def run_simple(funclist, n):
    regs = [n, 0, 0, 0]
    for step in funclist:
        step(regs)
    return regs

def main():
    data = aocd.get_data(day=DAY, year=YEAR)
    inblocks = data.split('inp w\n')
    print(inblocks)
    blocks = [compile_simple(l.split('\n')) for l in inblocks if l]
    max_digits = []
    for funclist in blocks:
        next_digit = None
        for i in range(9, 0, -1):
            print(funclist)
            outregs = run_simple(funclist, i)
            if outregs[3] == 0:
                next_digit = i
                break
        if next_digit is None:
            raise ValueError()
        max_digits.append(next_digit)
    print(max_digits)

    return
    inlist = data.split('\n')

    funclist = compile(inlist)
    print(funclist)

    for i in tqdm.tqdm(range(99999999999999, 9999999999999, -1)):
        digits = list(map(int, str(i)))
        if any(d == 0 for d in digits):
            continue
        outregs = run_funclist(funclist, list(map(int, str(i))))
        if outregs[3] == 0:
            answer = i
            break
        # if outregs['z'] == 0:
            # break
    # answer = i
    print(answer)

    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
