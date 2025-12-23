#!/usr/bin/env python

import fileinput

def repeat(l, n):
    for _ in range(n):
        yield from l

def int_builder(g):
    x = 0
    for d in g:
        x = x * 10 + d
    return x

def digits(x):
    return [int(y) for y in str(x)]

def dfs(n_pattern, p, lo, hi, ids, repeats):
    if len(p) == n_pattern:
        x = int_builder(repeat(p, repeats))
        if lo <= x <= hi:
            # print(lo, hi, x)
            ids.add(x)
        return 

    for n in range(10):
        if len(p) == 0 and n == 0:
            continue
        p.append(n)
        dfs(n_pattern, p, lo, hi, ids, repeats)
        p.pop()

def get_invalids(lo, hi):
    part1 = set()
    part2 = set()

    for n_d in range(len(digits(lo)), len(digits(hi))+1):
        
        for repeats in range(2, n_d+1):
            if n_d % repeats != 0: continue

            n_pattern = n_d // repeats
            # print(f"Doing dfs with n_d = {n_d}, lo,hi=({lo},{hi})")

            if repeats == 2:
                dfs(n_pattern, [], lo, hi, part1, repeats)
            dfs(n_pattern, [], lo, hi, part2, repeats)

    return part1, part2
    
def main(x):

    part1 = 0
    part2 = 0

    for part in x.strip().split(','):
        x1, x2 = part.split('-')
        x1 = int(x1)
        x2 = int(x2)

        p1, p2 = get_invalids(x1, x2)
        part1 += sum(p1)
        part2 += sum(p2)

    return part1, part2

if __name__=="__main__":
    for x in fileinput.input():
        part1, part2 = main(x)

        print(f"Part 1 = {part1}")
        print(f"Part 2 = {part2}")


