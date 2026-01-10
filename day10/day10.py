#!/usr/bin/env python

import fileinput
from itertools import combinations
import numpy as np
from functools import reduce

def read_lights(s):
    assert s[0] == "["
    assert s[-1] == "]"
    ret = np.zeros(len(s)-2, dtype=int)
    for i in range(1, len(s)-1):
        if s[i] == '#':
            ret[i-1] = 1
    return ret

def read_button(b, n):
    assert b[0] == "("
    assert b[-1] == ")"
    ret = np.zeros(n, dtype=int)
    for i in map(int, b[1:-1].split(',')):
        ret[i] = 1
    return ret

def read_joltage(s, n):
    assert s[0] == "{"
    assert s[-1] == "}"
    ret = np.fromiter(
        (int(x) for x in s[1:-1].split(',')),
        dtype=int
        )
    assert len(ret) == n
    return ret

def str_lights(light):
    return "[" + "".join('#' if x else '.' for x in light) + "]"

def str_button(button):
    return "(" + ", ".join(str(i) for i, x in enumerate(button) if x) + ")"

def str_buttons(p):
    return list(map(str_button, p))

def solve(lights, buttons):
    if np.all(lights == 0):
        yield []
        # return

    for n_buttons in range(1, len(buttons)+1):
        for p in combinations(buttons, r=n_buttons):
            if np.array_equal(reduce(np.logical_xor, p), lights):
                # print(str_buttons(p))
                yield p

def solve_part1(lights, buttons):
    return len(next(solve(lights, buttons)))

def solve_part2(target_joltage, buttons):
    # To get lowest bit of joltage correct we press each button either once or zero times
    # Then to get next lowest bit we press each button either twice or zero times.
    # Pressing twice or zero leaves lowest bit unchanged.
    #
    # Hence we can reach the target bit by bit without undoing previous work
    
    # start with lowest bit i.e. 0

    def dfs(joltage, presses, bit):
        # Check all lower bits are matching already
        mask = (1 << bit) - 1
        assert all(j & mask == t & mask for j, t in zip(joltage, target_joltage))

        # Yield number of presses for each successful path found
        if np.array_equal(joltage, target_joltage):
            yield presses
            return

        if np.any(np.greater(joltage, target_joltage)):
            # No route from here
            return

        lights = np.bitwise_and(
            np.bitwise_right_shift(
                np.bitwise_xor(joltage, target_joltage),
                bit),
            1)

        for p in solve(lights, buttons):

            new_joltage = joltage + np.bitwise_left_shift(sum(p), bit)
            new_presses = presses + (len(p) << bit)

            yield from dfs(new_joltage, new_presses, bit + 1)
    
    return min(dfs(np.zeros(len(target_joltage), dtype=int), 0, 0))

def main():
    part1 = 0
    part2 = 0
    for line in fileinput.input():
        parts = line.split()

        lights = read_lights(parts[0])

        buttons = [read_button(b, len(lights)) for b in parts[1:-1]]

        joltage = read_joltage(parts[-1], len(lights))

        print(str_lights(lights), str_buttons(buttons), parts[-1])

        part1 += solve_part1(lights, buttons)
        part2 += solve_part2(joltage, buttons)

    print(part1)
    print(part2)

if __name__=="__main__":
    main()
