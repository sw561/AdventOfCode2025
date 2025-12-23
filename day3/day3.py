#!/usr/bin/env python

import fileinput

def int_builder(g):
    x = 0
    for d in g:
        x = x * 10 + d
    return x

def max_joltage(*args, **kwargs):
    return int_builder(max_joltage_(*args, **kwargs))

def max_joltage_(s, n=2, start=0):
    if n == 1:
        yield max(s[start:])
        return

    # Prioritise early occurences
    choice = max((s[i],-i) for i in range(start, len(s)-(n-1)))
    choice_index = -choice[1]

    yield choice[0]
    yield from max_joltage_(s, n-1, choice_index+1)

if __name__=="__main__":
    part1 = 0
    part2 = 0
    for line in fileinput.input():
        s = [int(x) for x in line.strip()]
        part1 += max_joltage(s)
        part2 += max_joltage(s, n=12)

    print(part1)
    print(part2)
