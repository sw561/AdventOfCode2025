#!/usr/bin/env python

import fileinput
from itertools import permutations

def read_lights(s):
    assert s[0] == "["
    assert s[-1] == "]"
    ret = 0
    for i in range(1, len(s)-1):
        if s[i] == '#':
            ret |= 1 << (i-1)
    return ret

def read_button(b):
    assert b[0] == "("
    assert b[-1] == ")"
    ret = 0
    for i in map(int, b[1:-1].split(',')):
        ret |= (1 << i)
    return ret

def xor_reduce(g):
    ret = 0
    for gi in g:
        ret ^= gi
    return ret

def solve(lights, buttons):
    for n_buttons in range(1, len(buttons)):
        for p in permutations(buttons, r=n_buttons):
            if xor_reduce(p) == lights:
                # print(", ".join(map(bin, p)))
                return n_buttons

if __name__=="__main__":
    part1 = 0
    for line in fileinput.input():
        parts = line.split()

        lights = read_lights(parts[0])

        buttons = [read_button(b) for b in parts[1:-1]]

        # print(f"{bin(lights)} : " + ", ".join(map(bin, buttons)))

        part1 += solve(lights, buttons)

    print(part1)

