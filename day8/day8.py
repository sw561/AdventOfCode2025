#!/usr/bin/env python

import fileinput
import heapq
from itertools import combinations
from collections import defaultdict

def distance2(c1, c2):
    return sum((c1i-c2i)**2 for c1i, c2i in zip(c1, c2))

def solve(coords, n_edges=10):
    n = len(coords)

    es = heapq.nsmallest(
        n_edges,
        combinations(range(n), 2),
        key=lambda c: distance2(coords[c[0]], coords[c[1]])
        )

    edges = defaultdict(list)
    for i, j in es:
        edges[i].append(j)
        edges[j].append(i)

    # print(edges)

    # Now build groups using the edges
    groups = []
    visited = set()
    for i in range(n):
        if i in visited: continue

        group = [i]
        visited.add(i)
        neighbours = [i]

        while neighbours:
            neighbour = neighbours.pop()
            for j in edges[neighbour]:
                if j in visited: continue

                group.append(j)
                visited.add(j)
                neighbours.append(j)

        groups.append(group)

    groups.sort(key=len, reverse=True)
    # print(groups)

    part1 = len(groups[0]) * len(groups[1]) * len(groups[2])

    return part1

if __name__=="__main__":
    
    coords = []
    for line in fileinput.input():
        coords.append(tuple(int(x) for x in line.split(',')))

    # for i, c in enumerate(coords):
    #     print(i, c)

    part1 = solve(coords, n_edges=10 if len(coords) < 100 else 1000)

    print(part1)
