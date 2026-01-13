#!/usr/bin/env python

import fileinput
from collections import defaultdict

def dfs_wrapper(paths, start, destination):
    def dfs(seen, node):
        if node == destination:
            yield 1
            return

        for n in paths[node]:
            if n in seen:
                raise Exception("Circular paths!?!")

            seen.add(n)
            yield from dfs(seen, n)
            seen.remove(n)

    seen = set()
    yield from dfs(seen, start)
        

def main():
    paths = defaultdict(list)
    for line in fileinput.input():
        origin, rest = line.split(': ')
        for d in rest.strip().split(' '):
            paths[origin].append(d)

    part1 = sum(dfs_wrapper(paths, "you", "out"))

    print(part1)


if __name__=="__main__":
    main()
