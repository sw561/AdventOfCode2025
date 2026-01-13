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

def construct_int_9(arr):
    mask = (1 << 9) - 1
    assert all(arri & mask == arri for arri in arr)
    return tuple(arr) # reduce((lambda x, y: (x << 9) | y), arr, 0)

def all_combinations(button_map):
    for n_buttons in range(1, len(button_map)+1):
        for p in combinations(button_map.keys(), r=n_buttons):
            light = reduce(xor, p)
            yield light, p

def get_cached_solver(cache_size, button_map):
    data = [[] for _ in range(cache_size)]

    data[0].append((0, button_map[0]))

    for light, p in all_combinations(button_map):
        data[light].append((len(p), sum(button_map[pi] for pi in p)))

    return data

def solve_part1(lights, button_map):
    for l, p in all_combinations(button_map):
        if l == lights:
            return len(p)

def solve_part2_uncached(target_joltage, button_map):
    # To get lowest bit of joltage correct we press each button either once or zero times
    # Then to get next lowest bit we press each button either twice or zero times.
    # Pressing twice or zero leaves lowest bit unchanged.
    #
    # Hence we can reach the target bit by bit without undoing previous work
    
    # start with lowest bit i.e. 0

    n = len(target_joltage)
    cache_size = 1 << n

    cached_solve = get_cached_solver(cache_size, button_map)

    dfs_cache = dict()

    def dfs(joltage, bit):
        # Check all lower bits are matching already
        # mask = (1 << bit) - 1
        # assert all(j & mask == t & mask for j, t in zip(joltage, target_joltage))

        # Yield number of presses for each successful path found
        if np.array_equal(joltage, target_joltage):
            ret = 0

        elif np.any(np.greater(joltage, target_joltage)):
            # No route from here
            ret = None

        else:
            light_int = construct_int(
                ((y>>bit)&1) for y in np.bitwise_xor(joltage, target_joltage)
                )

            ret = None

            for length, s in cached_solve[light_int]:

                new_joltage = joltage + np.bitwise_left_shift(s, bit)

                r = cached_dfs(new_joltage, bit + 1)
                if r is None: continue
                r += (length << bit)
                if ret is None:
                    ret = r
                else:
                    ret = min(ret, r)

        return ret

    def cached_dfs(joltage, bit):
        if np.any(np.greater(joltage, target_joltage)):
            return None

        j_int = construct_int_9(joltage)
        key = (j_int, bit)
        if key in dfs_cache:
            return dfs_cache[key]

        r = dfs(joltage, bit)
        dfs_cache[key] = r
        return r
    
    return cached_dfs(np.zeros(len(target_joltage), dtype=int), 0)

def solve_part2(target_joltage, button_map):
    # To get lowest bit of joltage correct we press each button either once or zero times
    # Then to get next lowest bit we press each button either twice or zero times.
    # Pressing twice or zero leaves lowest bit unchanged.
    #
    # Hence we can reach the target bit by bit without undoing previous work
    
    # start with lowest bit i.e. 0

    n = len(target_joltage)
    cache_size = 1 << n

    cached_solve = get_cached_solver(cache_size, button_map)

    dfs_cache = {}

    def dfs(joltage, bit):
        # Return min number of presses required when starting from given joltage
        #
        # Check all lower bits are matching already
        # mask = (1 << bit) - 1
        # assert all(j & mask == t & mask for j, t in zip(joltage, target_joltage))

        # Yield number of presses for each successful path found
        if np.array_equal(joltage, target_joltage):
            return 0

        if np.any(np.greater(joltage, target_joltage)):
            # No route from here
            return None

        j_int = construct_int_9(joltage)
        if (j_int, bit) in dfs_cache:
            return dfs_cache[(j_int, bit)]

        light_int = construct_int(
            ((y>>bit)&1) for y in np.bitwise_xor(joltage, target_joltage)
            )

        ret = None

        for length, s in cached_solve[light_int]:

            new_joltage = joltage + np.bitwise_left_shift(s, bit)
            n_presses = length << bit

            p = dfs(new_joltage, bit + 1)
            if p == None: continue
            
            if ret is None:
                ret = n_presses + p
            else:
                ret = min(ret, n_presses + p)

        dfs_cache[(j_int, bit)] = ret
        return ret

    
    return dfs(np.zeros(len(target_joltage), dtype=int), 0)

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
            assert solve_part2_uncached(joltage, button_map) == check
            assert solve_part2(joltage, button_map) == check
            part2 += check
        else:
            check = solve_part2_uncached(joltage, button_map)
            part2 += check

        print(str_lights(lights, n), str_buttons(buttons), str_joltage(joltage), check)

    print(part1)
    print(part2)

if __name__=="__main__":
    main()
