#!/usr/bin/env python

import fileinput
from itertools import combinations
from collections import defaultdict

def distance2(c1, c2):
    return sum((c1i-c2i)**2 for c1i, c2i in zip(c1, c2))

def build_groups(n, edges, edge_n, part1=False):

    # Build the groups.
    # If part1 get product of three largest group sizes
    # If part2 just return boolean:
    #   True : only one large group,
    #   False: more than one group

    # Now build groups using the edges
    groups = []
    visited = set()
    for i in range(n):
        if i in visited: continue

        group_size = 1
        visited.add(i)
        neighbours = [i]

        while neighbours:
            neighbour = neighbours.pop()
            for (edge_i, j) in edges[neighbour]:
                if j in visited: continue
                if edge_i >= edge_n: continue

                group_size += 1
                visited.add(j)
                neighbours.append(j)

        if not part1:
            return group_size == n
        groups.append(group_size)

    groups.sort(reverse=True)

    part1 = groups[0] * groups[1] * groups[2]
    return part1

def solve(coords, n_edges=10):
    n = len(coords)

    es = sorted(
        combinations(range(n), 2),
        key=lambda c: distance2(coords[c[0]], coords[c[1]])
        )

    edges = defaultdict(list)
    for ei, (i, j) in enumerate(es):
        edges[i].append((ei, j))
        edges[j].append((ei, i))

    # edges[i] includes (ei, j) means i and j are connected iff number of edges > ei

    # Now build groups using the edges
    part1 = build_groups(n, edges, n_edges, part1=True)

    def objective(m):
        return build_groups(n, edges, m)

    # Expect one big group for right, not left
    # i.e. build_groups returns True for right not left
    left = 0
    right = len(es)

    assert objective(right) == True
    assert objective(left) == False

    # for m in range(0, right):
    #     print(m, objective(m), coords[es[m][0]], coords[es[m][1]])
    while right - left > 1:
        m = (left + right) // 2
        if objective(m):
            right = m
        else:
            left = m

    i, j = es[right-1]
    # print(coords[i], coords[j])
    part2 = coords[i][0] * coords[j][0]

    return part1, part2

if __name__=="__main__":
    
    coords = []
    for line in fileinput.input():
        coords.append(tuple(int(x) for x in line.split(',')))

    # for i, c in enumerate(coords):
    #     print(i, c)

    part1, part2 = solve(coords, n_edges=10 if len(coords) < 100 else 1000)

    print(part1)
    print(part2)
