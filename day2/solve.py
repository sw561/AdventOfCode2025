#!/usr/bin/env python

import fileinput
import pytest

def repeat_twice(l):
    yield from l
    yield from l

def int_builder(g):
    x = 0
    for d in g:
        x = x * 10 + d
    return x

def digits(x):
    return [int(y) for y in str(x)]

def dfs(n_pattern, p, lo, hi, ids):
    if len(p) == n_pattern:
        x = int_builder(repeat_twice(p))
        if lo <= x <= hi:
            print(lo, hi, x)
            ids.append(x)
        return 

    for n in range(10):
        if len(p) == 0 and n == 0:
            continue
        p.append(n)
        dfs(n_pattern, p, lo, hi, ids)
        p.pop()

    return


def get_invalids(lo, hi):

    lo_d = digits(lo)
    hi_d = digits(hi)

    ids = []

    for n_d in range(len(lo_d), len(hi_d)+1):
        
        if n_d % 2 != 0:
            continue

        n_pattern = n_d // 2
        print(f"Doing dfs with n_d = {n_d}, lo,hi=({lo},{hi})")

        dfs(n_pattern, [], lo, hi, ids)

    return ids
    
@pytest.mark.parametrize("lo, hi, expected", 
    [(11, 22, 2),
     (98, 115, 1),
     (998, 1012, 1),
     (1188511880, 1188511890, 1),
     (222220, 222224, 1),
     (1698522, 1698528, 0),
     (446443, 446449, 1),
     (38593856, 38593862, 1)
    ])
def test_invalids(lo, hi, expected):
    assert len(get_invalids(lo, hi)) == expected

def main():
    for x in fileinput.input():

        part1 = 0

        for part in x.strip().split(','):
            x1, x2 = part.split('-')
            x1 = int(x1)
            x2 = int(x2)

            part1 += sum(get_invalids(x1, x2))

        print(f"Part 1 = {part1}")

if __name__=="__main__":
    main()
