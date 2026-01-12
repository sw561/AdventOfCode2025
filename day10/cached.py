#!/usr/bin/env python

import fileinput
from itertools import combinations
import numpy as np
from functools import reduce
from operator import xor

def read_lights(s):
    assert s[0] == "["
    assert s[-1] == "]"
    ret = 0
    for i in range(1, len(s)-1):
        ret <<= 1
        ret |= 1 if s[i] == '#' else 0
    return ret

def read_button(b, n):
    assert b[0] == "("
    assert b[-1] == ")"
    ret = np.zeros(n, dtype=int)
    for i in map(int, b[1:-1].split(',')):
        ret[i] = 1
    return ret

def read_joltage(s):
    assert s[0] == "{"
    assert s[-1] == "}"
    ret = np.fromiter(
        (int(x) for x in s[1:-1].split(',')),
        dtype=int
        )
    return ret

def str_lights(light, n):
    return "[" + "".join('#' if light & (1 << bit) else '.' for bit in range(n-1, -1, -1)) + "]"

def str_button(button):
    return "(" + ",".join(str(i) for i, x in enumerate(button) if x) + ")"

def str_buttons(bs):
    return " ".join([str_button(b) for b in bs if np.any(b)])

def str_joltage(joltage):
    return "{" + ",".join(str(i) for i in joltage) + "}"

def construct_int(arr):
    return reduce((lambda x, y: (x << 1) | y), arr)

def get_cached_solver(button_map):
    cache = {}
    def cached_solve(light_int):
        if light_int not in cache:
            cache[light_int] = list(
                solve(light_int, button_map)
                )
        return cache[light_int]
    return cached_solve

def solve(light_int, button_map):
    if light_int == 0:
        yield (0, button_map[0])

    for n_buttons in range(1, len(button_map)+1):
        for p in combinations(button_map.keys(), r=n_buttons):
            if reduce(xor, p) == light_int:
                yield (len(p), sum(button_map[pi] for pi in p))

def solve_part1(lights, button_map):
    l, s = next(solve(lights, button_map))
    return l

def solve_part2(target_joltage, button_map):
    # To get lowest bit of joltage correct we press each button either once or zero times
    # Then to get next lowest bit we press each button either twice or zero times.
    # Pressing twice or zero leaves lowest bit unchanged.
    #
    # Hence we can reach the target bit by bit without undoing previous work
    
    # start with lowest bit i.e. 0

    cached_solve = get_cached_solver(button_map)

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

        light_int = construct_int(
            ((y>>bit)&1) for y in np.bitwise_xor(joltage, target_joltage)
            )

        for length, s in cached_solve(light_int):

            new_joltage = joltage + np.bitwise_left_shift(s, bit)
            new_presses = presses + (length << bit)

            yield from dfs(new_joltage, new_presses, bit + 1)
    
    return min(dfs(np.zeros(len(target_joltage), dtype=int), 0, 0))

def main():
    part1 = 0
    part2 = 0
    for line in fileinput.input():
        parts = line.split()

        lights = read_lights(parts[0])
        joltage = read_joltage(next(p for p in parts if p.startswith('{')))
        n = len(joltage)
        buttons = [read_button(p, n) for p in parts if p.startswith('(')]

        button_map = {construct_int(b): b for b in buttons}
        button_map[0] = np.zeros(n, dtype=int)

        part1 += solve_part1(lights, button_map)

        if not parts[-1].startswith('{'):
            check = int(parts[-1])
            assert solve_part2(joltage, button_map) == check
            part2 += check
        else:
            check = solve_part2(joltage, button_map)
            part2 += check

        print(str_lights(lights, n), str_buttons(buttons), str_joltage(joltage), check)

    print(part1)
    print(part2)

if __name__=="__main__":
    main()
