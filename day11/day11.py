#!/usr/bin/env python

import fileinput
from collections import defaultdict

def dfs_wrapper(paths, start, destination, part2=False):
    cache = {}

    def dfs(node, var=0, depth=0):
        # print("-"*depth, node, bin(var))
        if node == destination:
            if part2:
                return 1 if var == 0b11 else 0
            else:
                return 1

        if (node, var) in cache:
            return cache[(node, var)]

        if node == "dac": var |= 0b01
        if node == "fft": var |= 0b10

        ret = sum(dfs(n, var, depth+1) for n in paths[node])
        cache[(node, var)] = ret
        return ret

    return dfs(start)

def main():
    paths = defaultdict(list)
    for line in fileinput.input():
        origin, rest = line.split(': ')
        for d in rest.strip().split(' '):
            paths[origin].append(d)

    part1 = dfs_wrapper(paths, "you", "out")
    print(part1)

    part2 = dfs_wrapper(paths, "svr", "out", part2=True)
    print(part2)

if __name__=="__main__":
    main()
